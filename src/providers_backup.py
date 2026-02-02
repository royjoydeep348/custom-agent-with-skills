"""Enhanced provider support with direct integrations for OpenRouter, OpenAI, Ollama, and Bedrock."""

import os
import importlib
import inspect
from typing import Any

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider

# Bedrock via Anthropic (async for streaming)
from anthropic import AsyncAnthropicBedrock

from src.settings import load_settings, Settings


def get_llm_model() -> Any:
    """
    Get model with proper provider integration.

    Returns the appropriate model based on the configured provider.
    Supports OpenRouter, OpenAI, Bedrock, and Ollama.
    """
    settings = load_settings()
    provider = (settings.llm_provider or "").lower()

    if provider == "openrouter":
        return _create_openrouter_model(settings)
    elif provider == "openai":
        return _create_openai_model(settings)
    elif provider == "ollama":
        return _create_ollama_model(settings)
    elif provider == "bedrock":
        return _create_bedrock_model(settings)
    else:
        raise ValueError(f"Unsupported provider: {provider!r}")


def _create_openrouter_model(settings: Settings) -> OpenRouterModel:
    """Create OpenRouter model with direct integration and app attribution."""
    provider = OpenRouterProvider(
        api_key=settings.llm_api_key,
        app_url=settings.openrouter_app_url,
        app_title=settings.openrouter_app_title,
    )
    return OpenRouterModel(settings.llm_model, provider=provider)


def _create_openai_model(settings: Settings) -> OpenAIChatModel:
    """Create OpenAI model with direct integration."""
    provider = OpenAIProvider(api_key=settings.llm_api_key)
    return OpenAIChatModel(settings.llm_model, provider=provider)


def _create_ollama_model(settings: Settings) -> OpenAIChatModel:
    """
    Create Ollama model via OpenAI-compatible API.

    Ollama provides an OpenAI-compatible API endpoint.
    """
    provider = OpenAIProvider(
        base_url=settings.llm_base_url or "http://localhost:11434/v1",
        api_key="ollama",  # Required but unused by Ollama
    )
    return OpenAIChatModel(settings.llm_model, provider=provider)


def _create_bedrock_model(settings: Settings) -> Any:
    """
    Create an Anthropic model via AWS Bedrock.

    Version-agnostic strategy:
      1) Ensure AWS_REGION (and optionally AWS_PROFILE) are set (older SDKs read env).
      2) Construct AsyncAnthropicBedrock() (async client required for streaming).
      3) Import the Anthropic model wrapper from pydantic_ai (class name varies).
      4) Try to pass the Bedrock client via constructor kwargs (client/async_client/anthropic_client).
      5) If the wrapper requires a `provider=...`, attempt to construct an AnthropicProvider
         *bound to the Bedrock client* (so it will NOT require ANTHROPIC_API_KEY).
      6) If constructor refuses all client/provider options, attach the client attribute post-construction.
    """
    # --- Guard rails
    if not settings.aws_region:
        raise ValueError("aws_region is required when using llm_provider=bedrock")

    # --- 1) Env for older anthropic SDKs
    os.environ.setdefault("AWS_REGION", settings.aws_region)
    if getattr(settings, "aws_profile", None):
        os.environ.setdefault("AWS_PROFILE", settings.aws_profile)

    # --- 2) Async Bedrock client (pydantic_ai streams await responses)
    anthropic_client = AsyncAnthropicBedrock()

    # --- 3) Import Anthropic model wrapper from pydantic_ai
    try:
        mod = importlib.import_module("pydantic_ai.models.anthropic")
    except Exception as e:
        raise ImportError(
            "Failed to import `pydantic_ai.models.anthropic`. "
            "Upgrade `pydantic-ai` or directly use the `anthropic` async Bedrock client in your agent. "
            f"(original error: {e})"
        ) from e

    # Pick a model class that exists in your version
    ModelClass = None
    for name in ("AnthropicMessagesModel", "AnthropicModel", "AnthropicChatModel"):
        if hasattr(mod, name) and inspect.isclass(getattr(mod, name)):
            ModelClass = getattr(mod, name)
            break
    if ModelClass is None:
        for n, o in vars(mod).items():
            if inspect.isclass(o) and "Anthropic" in n and n.endswith("Model"):
                ModelClass = o
                break
    if ModelClass is None:
        available = [n for n, o in vars(mod).items() if inspect.isclass(o)]
        raise ImportError(
            "No compatible Anthropic model class found in `pydantic_ai.models.anthropic`.\n"
            "Tried: AnthropicMessagesModel, AnthropicModel, AnthropicChatModel.\n"
            f"Available classes: {available}\n"
            "Options:\n"
            "  - Upgrade `pydantic-ai` to a version that includes an Anthropic model wrapper, or\n"
            "  - Use the `anthropic` async Bedrock client directly in your agent code path."
        )

    # --- 4) Prepare constructor kwargs
    init_params = set(inspect.signature(ModelClass.__init__).parameters.keys())

    # model arg varies (model/model_name/name)
    model_arg_name = None
    for cand in ("model", "model_name", "name"):
        if cand in init_params:
            model_arg_name = cand
            break
    if not model_arg_name:
        raise TypeError(
            f"{ModelClass.__name__}.__init__ does not accept a model name "
            "(expected one of: model, model_name, name)"
        )
    kwargs = {model_arg_name: settings.llm_model}

    # Try to pass the async client directly
    for client_kw in ("client", "async_client", "anthropic_client"):
        if client_kw in init_params:
            try:
                return ModelClass(**kwargs, **{client_kw: anthropic_client})
            except TypeError:
                pass  # try next option

    # --- 5) Some versions require a provider=...; try to create AnthropicProvider bound to Bedrock client
    if "provider" in init_params:
        try:
            prov_mod = importlib.import_module("pydantic_ai.providers.anthropic")
            AnthropicProvider = getattr(prov_mod, "AnthropicProvider", None)
        except Exception:
            AnthropicProvider = None

        provider = None
        if AnthropicProvider is not None:
            prov_params = set(inspect.signature(AnthropicProvider.__init__).parameters.keys())
            prov_kwargs = {}

            # Try to bind our Bedrock client to the provider if supported by your version
            for cand in ("client", "async_client", "anthropic_client"):
                if cand in prov_params:
                    prov_kwargs[cand] = anthropic_client
                    break

            try:
                provider = AnthropicProvider(**prov_kwargs)
                # If it still throws about ANTHROPIC_API_KEY here, your provider doesn't accept client injection
            except Exception as e:
                # Could not inject client; do NOT fallback to AnthropicProvider() with no args (would require API key)
                provider = None

        if provider is not None:
            kwargs["provider"] = provider
            try:
                return ModelClass(**kwargs)
            except TypeError:
                # fall-through to attribute injection
                pass
        else:
            # Explain why we can't use provider on this version
            sig = None
            try:
                sig = str(inspect.signature(AnthropicProvider.__init__)) if AnthropicProvider else "N/A"
            except Exception:
                sig = "N/A"
            raise RuntimeError(
                "Your installed `pydantic_ai` Anthropic model appears to require `provider=...`, "
                "but `AnthropicProvider` in this version does not accept a Bedrock client and "
                "demands ANTHROPIC_API_KEY for the public API.\n"
                "Options:\n"
                "  • Upgrade `pydantic-ai` to a version whose Anthropic provider accepts a client, or\n"
                "  • Use the `anthropic` async Bedrock client directly in your agent code (bypassing the wrapper).\n"
                f"AnthropicProvider.__init__ signature: {sig}"
            )

    # --- 6) Last attempt: construct then attach async client attribute
    instance = ModelClass(**kwargs)
    for attr in ("client", "async_client", "anthropic_client", "_client"):
        try:
            setattr(instance, attr, anthropic_client)
            if getattr(instance, attr, None) is anthropic_client:
                return instance
        except Exception:
            continue

    sig = str(inspect.signature(ModelClass.__init__))
    raise RuntimeError(
        "Could not attach AsyncAnthropicBedrock client to the Anthropic model wrapper.\n"
        f"Model class: {ModelClass.__name__}\n"
        f"__init__ signature: {sig}\n"
        f"Tried kwargs: {kwargs}\n"
        "This `pydantic_ai` version likely requires a different integration.\n"
        "Options:\n"
        "  - Share the signature above so we can map the exact parameter names, or\n"
        "  - Upgrade `pydantic-ai` to a Bedrock-friendly version, or\n"
        "  - Call the `anthropic` async Bedrock client directly in your agent."
    )


def get_model_info() -> dict:
    """Get information about current model configuration."""
    settings = load_settings()
    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "llm_base_url": settings.llm_base_url,
        "aws_region": getattr(settings, "aws_region", None),
    }


def validate_llm_configuration() -> bool:
    """Validate that LLM configuration is properly set."""
    try:
        get_llm_model()
        return True
    except Exception as e:
        print(f"LLM configuration validation failed: {e}")
        return False
