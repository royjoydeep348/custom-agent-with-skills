"""Settings configuration for Skill-Based Agent (with AWS Bedrock support)."""

from pathlib import Path
from typing import Optional, Literal

from dotenv import load_dotenv
from pydantic import Field, ConfigDict, model_validator
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,   # allows LLM_PROVIDER or llm_provider
        extra="ignore",
    )

    # ---------------------
    # Skills Configuration
    # ---------------------
    skills_dir: Path = Field(
        default=Path("skills"),
        description="Directory containing skill definitions",
    )

    # ---------------------------------
    # LLM Configuration (multi-provider)
    # ---------------------------------
    llm_provider: Literal["openrouter", "openai", "ollama", "bedrock"] = Field(
        default="openrouter",
        description="LLM provider to use",
    )

    # API key: required for OpenAI/OpenRouter, optional for Ollama/Bedrock
    llm_api_key: Optional[str] = Field(
        default=None,
        description="API key for the LLM provider (required for openai/openrouter)",
    )

    llm_model: str = Field(
        # Default kept from your original file
        default="anthropic/claude-sonnet-4.5",
        description="Model to use for agent",
    )

    llm_base_url: Optional[str] = Field(
        default="https://openrouter.ai/api/v1",
        description="Base URL for the LLM API (for OpenAI-compatible providers)",
    )

    # -------------------------
    # OpenRouter-Specific (Opt)
    # -------------------------
    openrouter_app_url: Optional[str] = Field(
        default=None,
        description="App URL for OpenRouter analytics (optional)",
    )
    openrouter_app_title: Optional[str] = Field(
        default=None,
        description="App title for OpenRouter tracking (optional)",
    )

    # ---------------
    # AWS / Bedrock
    # ---------------
    aws_region: Optional[str] = Field(
        default=None,
        description="AWS region for Bedrock (e.g., ap-southeast-1). Required for provider=bedrock.",
    )
    aws_profile: Optional[str] = Field(
        default=None,
        description="AWS profile name (optional). If set, AWS SDK will use this profile.",
    )

    # ---------------------
    # Application Settings
    # ---------------------
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")

    # --------------
    # Logfire (Opt)
    # --------------
    logfire_token: Optional[str] = Field(
        default=None,
        description="Logfire API token from 'logfire auth' (optional)",
    )
    logfire_service_name: str = Field(
        default="skill-agent",
        description="Service name in Logfire",
    )
    logfire_environment: str = Field(
        default="development",
        description="Environment (development, production, etc.)",
    )

    # -----------------------------
    # Provider-specific validation
    # -----------------------------
    @model_validator(mode="after")
    def _validate_provider_requirements(self):
        provider = (self.llm_provider or "").lower()

        if provider in ("openai", "openrouter"):
            if not self.llm_api_key:
                raise ValueError(
                    f"llm_api_key is required when llm_provider={provider}. "
                    "Set LLM_API_KEY in your .env."
                )

        if provider == "bedrock":
            if not self.aws_region:
                raise ValueError(
                    "aws_region is required when llm_provider=bedrock. "
                    "Set AWS_REGION in your .env (e.g., ap-southeast-1)."
                )
            # For Bedrock, ensure model id looks like a Bedrock Anthropic model
            # e.g., 'anthropic.claude-3-5-sonnet-20241022-v2:0'
            if not self.llm_model or "anthropic." not in self.llm_model:
                # Relax/change this if you support other Bedrock providers
                raise ValueError(
                    "llm_model should be a valid Bedrock model id for Anthropic, "
                    "e.g., 'anthropic.claude-3-5-sonnet-20241022-v2:0'. "
                    "Update LLM_MODEL in your .env."
                )

        return self


def load_settings() -> Settings:
    """Load settings with proper error handling."""
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        # Helpful hints for common misconfigurations
        lower = str(e).lower()
        if "llm_api_key" in lower:
            error_msg += "\nMake sure to set LLM_API_KEY in your .env file (required for OpenAI/OpenRouter)."
        if "aws_region" in lower or "bedrock" in lower:
            error_msg += "\nFor Bedrock, set AWS_REGION and a valid Bedrock LLM_MODEL in your .env."
        raise ValueError(error_msg) from e
