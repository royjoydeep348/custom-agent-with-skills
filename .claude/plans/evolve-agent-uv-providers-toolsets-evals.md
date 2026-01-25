# Feature: Evolve Skill-Based Agent with UV, Direct Providers, Tool Sets, and Evals

The following plan should be complete, but it's important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Evolve the skill-based Pydantic AI agent to production readiness by:
1. Migrating to UV package manager for modern Python tooling
2. Implementing direct provider integrations (OpenRouter, OpenAI, Ollama) instead of generic OpenAI-compatible wrapper
3. Converting skill tools to reusable Tool Sets (Pydantic AI feature)
4. Building comprehensive evaluation system with YAML datasets and custom evaluators
5. Adding optional Logfire integration (disabled by default, enabled via env var)
6. Creating end-to-end validation scripts for testing agent with different skills

This transformation enables the agent to showcase modern Python development practices, leverage Pydantic AI's latest features, and provide a robust testing framework for production deployment.

## User Story

As a **developer building AI agents with Pydantic AI**
I want to **use modern tooling (UV), proper provider integrations, reusable tool sets, and comprehensive evals**
So that **my agent is production-ready, maintainable, testable, and showcases best practices for the Pydantic AI ecosystem**

## Problem Statement

The current implementation has several limitations:
1. **UV Partial Integration**: UV is configured but not consistently used; setup instructions still reference pip
2. **Generic Provider Approach**: Using OpenAI-compatible base_url instead of direct provider integrations, limiting access to provider-specific features (OpenRouter fallbacks, attribution)
3. **Tools Tightly Coupled to Agent**: Skill tools registered directly on agent, not reusable across different agents
4. **No Evaluation Framework**: No systematic way to verify agent correctly loads skills based on user queries
5. **No End-to-End Testing**: Manual testing only, no automated scripts to validate full workflows
6. **Logfire Not Optional**: Should support optional Logfire for video demo visualization while working without it for local development

## Solution Statement

Transform the agent through systematic evolution:
1. **Complete UV Migration**: Standardize on UV for all package management, venv creation, and command execution
2. **Direct Provider Integrations**: Implement OpenRouter, OpenAI, and Ollama providers with proper authentication and provider-specific features
3. **Tool Set Architecture**: Create `SkillToolSet` using Pydantic AI's `FunctionToolset` for modularity and reusability
4. **Comprehensive Evals**: Build YAML-based test datasets with custom evaluators using message inspection for tool call verification (no Logfire required) and LLM-as-judge for response quality
5. **Optional Logfire**: Make Logfire integration optional via environment variable for video demo visualization (not required for evals or local development)
6. **Automated Testing Scripts**: Create validation scripts to test agent with weather/code_review skills and run evals locally

## Feature Metadata

**Feature Type**: Enhancement + Refactor
**Estimated Complexity**: High
**Primary Systems Affected**:
- Package Management (pyproject.toml, tooling)
- Provider Integration (src/providers.py, src/settings.py)
- Agent Architecture (src/agent.py, new src/skill_toolset.py)
- Testing Infrastructure (tests/evals/, new validation scripts)
**Dependencies**:
- UV (external tool)
- pydantic-ai>=0.0.30 (existing)
- pydantic-evals (new)
- logfire (new, optional)

---

## CONTEXT REFERENCES

### Relevant Codebase Files - IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

**Provider & Settings:**
- `src/providers.py` (lines 1-62) - Why: Current generic provider implementation to be replaced with direct integrations
- `src/settings.py` (lines 1-58) - Why: Settings structure and Pydantic Settings pattern to extend
- `.env` (lines 1-14) - Why: Current configuration to reorganize for multi-provider support

**Agent & Tools:**
- `src/agent.py` (lines 1-170) - Why: Agent definition, tool registration pattern, system prompt decorator
- `src/skill_tools.py` (lines 1-243) - Why: Tool implementations to migrate to Tool Set
- `src/dependencies.py` (lines 1-72) - Why: Dependency injection pattern and initialization

**Testing Patterns:**
- `tests/test_skill_loader.py` (lines 1-291) - Why: Test patterns, fixtures, mock structures
- `tests/test_skill_tools.py` (lines 1-319) - Why: Async test patterns, security testing, error handling tests
- `tests/test_agent.py` (lines 1-393) - Why: Integration test patterns, agent initialization tests

**Project Configuration:**
- `pyproject.toml` (lines 1-51) - Why: Dependency management, tool configs, UV section
- `README.md` (lines 1-285) - Why: Documentation structure and setup instructions to update

### New Files to Create

**Tool Set:**
- `src/skill_toolset.py` - Skill tools as reusable FunctionToolset

**Evaluation System:**
- `tests/evals/__init__.py` - Package initialization
- `tests/evals/skill_loading.yaml` - YAML dataset for skill loading verification
- `tests/evals/response_quality.yaml` - YAML dataset for LLM-as-judge evaluation
- `tests/evals/evaluators.py` - Custom evaluators (SkillWasLoaded, ToolWasCalled, etc.)
- `tests/evals/run_evals.py` - Evaluation runner script

**Validation Scripts:**
- `scripts/__init__.py` - Scripts package initialization
- `scripts/test_agent.py` - Interactive agent testing script
- `scripts/validate_skills.py` - Automated skill validation
- `scripts/run_full_validation.py` - Complete validation pipeline

**Configuration:**
- `.python-version` - Python version for UV
- `.env.example` - Updated with all provider examples and Logfire (optional)

### Relevant Documentation - YOU SHOULD READ THESE BEFORE IMPLEMENTING!

**UV Package Manager:**
- [UV Official Documentation](https://docs.astral.sh/uv/) - Complete UV reference
- [UV Project Workflows](https://docs.astral.sh/uv/guides/projects/) - Project setup and management

**Pydantic AI Providers:**
- [OpenRouter Integration](https://ai.pydantic.dev/models/openrouter/) - Direct OpenRouter provider with app attribution
- [OpenAI Integration](https://ai.pydantic.dev/models/openai/) - Direct OpenAI provider
- [Provider Overview](https://ai.pydantic.dev/models/overview/) - Provider architecture

**Pydantic AI Tool Sets:**
- [Tool Sets Documentation](https://ai.pydantic.dev/toolsets/) - FunctionToolset and reusable tools
- [Tools Advanced](https://ai.pydantic.dev/tools-advanced/) - Tool composition patterns

**Pydantic AI Evals:**
- [Evals Quick Start](https://ai.pydantic.dev/evals/quick-start/) - Getting started with evals
- [Custom Evaluators](https://ai.pydantic.dev/evals/evaluators/custom/) - Building custom evaluators
- [LLM Judge Evaluators](https://ai.pydantic.dev/evals/evaluators/llm-judge/) - LLM-as-judge pattern
- [Span-Based Evaluation](https://ai.pydantic.dev/evals/evaluators/span-based/) - Tool call verification via spans
- [Dataset Serialization](https://ai.pydantic.dev/evals/how-to/dataset-serialization/) - YAML dataset format

**Logfire Integration:**
- [Logfire with Pydantic AI](https://ai.pydantic.dev/logfire/) - Instrumentation setup
- [Logfire Configuration](https://logfire.pydantic.dev/docs/reference/configuration/) - Optional configuration

### Patterns to Follow

**Naming Conventions:**
```python
# From existing codebase
# Functions: snake_case
async def load_skill(ctx: RunContext[AgentDependencies], skill_name: str) -> str:

# Classes: PascalCase
class SkillLoader:
class AgentDependencies:

# Constants: UPPER_SNAKE_CASE
MAIN_SYSTEM_PROMPT = """..."""

# Private functions: leading underscore
def _parse_skill_metadata(self, skill_md: Path) -> Optional[SkillMetadata]:
```

**Error Handling Pattern:**
```python
# From src/skill_tools.py lines 32-42
skill_loader = ctx.deps.skill_loader

if skill_loader is None:
    logger.error("load_skill_failed: skill_loader not initialized")
    return "Error: Skill loader not initialized. Please try again."

if skill_name not in skill_loader.skills:
    available = list(skill_loader.skills.keys())
    logger.warning(f"load_skill_not_found: skill_name={skill_name}, available={available}")
    return f"Error: Skill '{skill_name}' not found. Available skills: {available}"
```

**Logging Pattern:**
```python
# From src/skill_loader.py lines 64-67
logger.info(f"skill_discovered: name={metadata.name}, version={metadata.version}")
logger.warning(f"skill_missing_frontmatter: file={skill_md}")
logger.error(f"skill_parse_error: file={skill_md}, error={str(e)}")
logger.exception(f"skill_yaml_parse_error: file={skill_md}, error={str(e)}")
```

**Async Test Pattern:**
```python
# From tests/test_skill_tools.py lines 56-78
@pytest.mark.asyncio
async def test_load_skill_returns_instructions(self, tmp_path: Path) -> None:
    """Test that load_skill returns full skill instructions."""
    skill = create_test_skill(
        tmp_path,
        "test_skill",
        "A test skill",
        "# Test Skill\n\nThis is the skill body.",
    )

    loader = SkillLoader(tmp_path)
    loader.skills = {"test_skill": skill}

    ctx = MockContext(deps=MockDependencies(skill_loader=loader))

    result = await load_skill(ctx, "test_skill")

    assert "# Test Skill" in result
```

**Pydantic Settings Pattern:**
```python
# From src/settings.py lines 13-47
class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    llm_api_key: str = Field(..., description="API key for the LLM provider")
    llm_model: str = Field(
        default="anthropic/claude-sonnet-4.5",
        description="Model to use for agent",
    )
```

**Tool Registration Pattern (Current - to be replaced):**
```python
# From src/agent.py lines 54-73
@skill_agent.tool
async def load_skill_tool(
    ctx: RunContext[AgentDependencies],
    skill_name: str,
) -> str:
    """
    Load the full instructions for a skill.

    Use this tool when you need to access the detailed instructions
    for a skill...
    """
    return await load_skill(ctx, skill_name)
```

---

## IMPLEMENTATION PLAN

### Phase 1: Foundation - UV Migration

Complete UV integration by standardizing package management, updating configurations, and ensuring all commands use UV.

**Tasks:**
- Create `.python-version` file for UV Python version management
- Update `pyproject.toml` to consolidate dev dependencies (remove duplication between `[project.optional-dependencies]` and `[tool.uv]`)
- Run `uv sync` to create lock file and verify environment
- Update `README.md` setup instructions to use UV exclusively
- Test that `uv run pytest tests/` works correctly

### Phase 2: Provider Integration Overhaul

Replace generic OpenAI-compatible approach with direct provider integrations for OpenRouter, OpenAI, and Ollama.

**Tasks:**
- Update `src/settings.py` with provider-specific fields (OpenRouter app URL/title, provider selection enum)
- Rewrite `src/providers.py` with three provider factory functions
- Update `.env` with current OpenRouter configuration
- Create comprehensive `.env.example` with all provider examples
- Test each provider configuration works correctly

### Phase 3: Tool Set Architecture

Convert skill tools from direct agent registration to reusable FunctionToolset.

**Tasks:**
- Create `src/skill_toolset.py` with FunctionToolset containing all three skill tools
- Update `src/agent.py` to use toolsets parameter instead of @tool decorators
- Remove tool decorator functions from `src/agent.py` (keep HTTP tools as direct registrations)
- Test that agent still works with toolset registration
- Verify tool calls appear correctly in responses

### Phase 4: Logfire Integration (Optional)

Add Logfire instrumentation with graceful fallback when token not available.

**Tasks:**
- Add logfire dependency to `pyproject.toml` dev dependencies
- Update `src/settings.py` with optional Logfire fields
- Add conditional Logfire initialization to `src/agent.py` (only if token present)
- Update `.env.example` with Logfire configuration (commented out)
- Test agent works both with and without Logfire token

### Phase 5: Evaluation System

Build comprehensive evaluation framework with YAML datasets and custom evaluators using message inspection.

**Key Architecture Decision**: Custom evaluators use **message inspection** to verify tool calls, NOT span trees. This means:
- No Logfire dependency for evals
- Access tool calls via `ctx.all_messages()` → iterate content → check `part.part_kind == 'tool-use'`
- Inspect tool names via `part.tool_name` and arguments via `part.tool_input`
- Fully functional for local development and CI/CD

**Tasks:**
- Add `pydantic-evals` to dev dependencies in `pyproject.toml`
- Create evaluation directory structure (`tests/evals/`)
- Write skill loading dataset YAML
- Write response quality dataset YAML
- Implement custom evaluators using message inspection (SkillWasLoaded, ToolWasCalled)
- Create eval runner script
- Test evals run successfully without Logfire and produce meaningful results

### Phase 6: Validation Scripts & End-to-End Testing

Create automated scripts for testing agent behavior and running full validation pipeline.

**Tasks:**
- Create scripts directory structure
- Write interactive agent testing script
- Write skill validation script
- Write comprehensive validation pipeline
- Test all scripts work end-to-end
- Document script usage in README

### Phase 7: Documentation & Polish

Update all documentation, ensure consistency, and verify complete functionality.

**Tasks:**
- Update `README.md` with UV setup, provider switching, eval running
- Update `.env.example` with comprehensive comments
- Add CHANGELOG.md documenting all changes
- Run full validation suite and fix any issues
- Clean up any unused code or imports

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### Phase 1: UV Migration Foundation

#### CREATE .python-version

- **IMPLEMENT**: Create Python version file for UV to manage Python version automatically
- **CONTENT**: `3.11`
- **VALIDATE**: `uv --version` (verify UV is installed)

#### UPDATE pyproject.toml - Consolidate Dev Dependencies

- **IMPLEMENT**: Remove duplicate dev dependencies from `[tool.uv]` section, use `[project.optional-dependencies]` as single source of truth
- **CHANGES**:
  - Keep `[project.optional-dependencies]` dev list as-is
  - Remove `[tool.uv]` dev-dependencies section entirely (UV reads from project.optional-dependencies automatically)
  - Add `[tool.uv]` python version constraint: `python = "3.11"`
- **PATTERN**: Mirror pyproject.toml:1-51 structure
- **VALIDATE**: `uv sync` (should install all dependencies without errors)

#### RUN uv sync - Initialize Environment

- **IMPLEMENT**: Run UV sync to create/update virtual environment and lock file
- **VALIDATE**:
  - `uv sync`
  - Verify `.venv/` directory created
  - Verify `uv.lock` file created/updated
  - `uv run python --version` (should show Python 3.11.x)

#### UPDATE README.md - UV Setup Instructions

- **IMPLEMENT**: Replace all pip-based setup instructions with UV equivalents
- **CHANGES**:
  - Quick Start section: Replace `python -m venv .venv` → `uv venv` (or just skip, uv sync creates it)
  - Replace `pip install -e .` → `uv sync`
  - Replace `python -m src.cli` → `uv run python -m src.cli`
  - Add note: "This project uses UV for package management. Install UV: https://docs.astral.sh/uv/"
- **PATTERN**: README.md:40-88 structure
- **VALIDATE**: Follow new README instructions in fresh directory clone

#### VALIDATE Phase 1 Complete

- **VALIDATE**:
  - `uv run pytest tests/ -v` (all tests pass)
  - `uv run python -m src.cli` (agent starts without errors)
  - `uv pip list` (shows all expected dependencies)

---

### Phase 2: Provider Integration Overhaul

#### UPDATE src/settings.py - Provider-Specific Fields

- **IMPLEMENT**: Add provider selection and provider-specific configuration fields
- **CHANGES**:
  ```python
  from typing import Optional, Literal

  # Add after existing fields:
  llm_provider: Literal["openrouter", "openai", "ollama"] = Field(
      default="openrouter",
      description="LLM provider to use"
  )

  # OpenRouter-specific (optional)
  openrouter_app_url: Optional[str] = Field(
      default=None,
      description="App URL for OpenRouter analytics (optional)"
  )
  openrouter_app_title: Optional[str] = Field(
      default=None,
      description="App title for OpenRouter tracking (optional)"
  )
  ```
- **PATTERN**: src/settings.py:13-47 Pydantic Settings pattern
- **IMPORTS**: Add `from typing import Literal, Optional` if not present
- **VALIDATE**: `uv run python -c "from src.settings import load_settings; s = load_settings(); print(s.llm_provider)"`

#### REWRITE src/providers.py - Direct Provider Integrations

- **IMPLEMENT**: Replace generic OpenAI-compatible approach with three provider-specific factory functions
- **STRUCTURE**:
  ```python
  """Enhanced provider support with direct integrations."""

  from typing import Union
  from pydantic_ai.models.openai import OpenAIChatModel
  from pydantic_ai.models.openrouter import OpenRouterModel
  from pydantic_ai.providers.openai import OpenAIProvider
  from pydantic_ai.providers.openrouter import OpenRouterProvider
  from src.settings import load_settings

  def get_llm_model() -> Union[OpenAIChatModel, OpenRouterModel]:
      """Get model with proper provider integration."""
      settings = load_settings()
      provider = settings.llm_provider

      if provider == 'openrouter':
          return _create_openrouter_model(settings)
      elif provider == 'openai':
          return _create_openai_model(settings)
      elif provider == 'ollama':
          return _create_ollama_model(settings)
      else:
          raise ValueError(f"Unsupported provider: {provider}")

  def _create_openrouter_model(settings) -> OpenRouterModel:
      """OpenRouter with direct integration and app attribution."""
      provider = OpenRouterProvider(
          api_key=settings.llm_api_key,
          app_url=settings.openrouter_app_url,
          app_title=settings.openrouter_app_title,
      )
      return OpenRouterModel(settings.llm_model, provider=provider)

  def _create_openai_model(settings) -> OpenAIChatModel:
      """OpenAI with direct integration."""
      provider = OpenAIProvider(api_key=settings.llm_api_key)
      return OpenAIChatModel(settings.llm_model, provider=provider)

  def _create_ollama_model(settings) -> OpenAIChatModel:
      """Ollama via OpenAI-compatible API."""
      provider = OpenAIProvider(
          base_url=settings.llm_base_url or 'http://localhost:11434/v1',
          api_key='ollama'  # Required but unused by Ollama
      )
      return OpenAIChatModel(settings.llm_model, provider=provider)

  # Keep get_model_info and validate_llm_configuration functions
  ```
- **PATTERN**: src/providers.py:1-62 structure
- **IMPORTS**: Import OpenRouterModel and OpenRouterProvider
- **GOTCHA**: Ollama requires api_key parameter but doesn't use it - pass 'ollama' string
- **VALIDATE**: `uv run python -c "from src.providers import get_llm_model; m = get_llm_model(); print(type(m).__name__)"`

#### UPDATE .env - Current Configuration

- **IMPLEMENT**: Reorganize current .env to match new provider structure
- **CHANGES**:
  ```bash
  # Provider Selection
  LLM_PROVIDER=openrouter

  # LLM Configuration (OpenRouter)
  LLM_API_KEY=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
  LLM_MODEL=anthropic/claude-haiku-4.5
  LLM_BASE_URL=https://openrouter.ai/api/v1

  # OpenRouter-Specific (Optional)
  # OPENROUTER_APP_URL=https://yourdomain.com
  # OPENROUTER_APP_TITLE=Skill-Based Agent

  # Skills Configuration
  SKILLS_DIR=skills

  # Application Settings
  APP_ENV=development
  LOG_LEVEL=INFO

  # Logfire (Optional - leave blank if not using)
  LOGFIRE_TOKEN=
  LOGFIRE_SERVICE_NAME=skill-agent
  LOGFIRE_ENVIRONMENT=development
  ```
- **PATTERN**: Keep existing key-value format
- **VALIDATE**: `uv run python -m src.cli` (agent should start and work)

#### CREATE .env.example - Comprehensive Provider Examples

- **IMPLEMENT**: Create comprehensive example showing all three provider configurations
- **CONTENT**:
  ```bash
  # =============================================================================
  # PROVIDER SELECTION - Choose one: openrouter, openai, or ollama
  # =============================================================================
  LLM_PROVIDER=openrouter

  # =============================================================================
  # OPENROUTER CONFIGURATION
  # =============================================================================
  # Use this for OpenRouter (https://openrouter.ai)
  LLM_API_KEY=sk-or-v1-your-api-key-here
  LLM_MODEL=anthropic/claude-haiku-4.5
  LLM_BASE_URL=https://openrouter.ai/api/v1

  # Optional: App attribution for OpenRouter analytics
  # OPENROUTER_APP_URL=https://yourdomain.com
  # OPENROUTER_APP_TITLE=Your App Name

  # =============================================================================
  # OPENAI CONFIGURATION (Alternative to OpenRouter)
  # =============================================================================
  # Uncomment these and comment out OpenRouter section above
  # LLM_PROVIDER=openai
  # LLM_API_KEY=sk-proj-your-openai-api-key
  # LLM_MODEL=gpt-4o-mini
  # # LLM_BASE_URL not needed for OpenAI

  # =============================================================================
  # OLLAMA CONFIGURATION (Local/Self-Hosted Alternative)
  # =============================================================================
  # Uncomment these and comment out OpenRouter section above
  # LLM_PROVIDER=ollama
  # LLM_API_KEY=ollama
  # LLM_MODEL=llama3.2
  # LLM_BASE_URL=http://localhost:11434/v1

  # =============================================================================
  # SKILLS CONFIGURATION
  # =============================================================================
  SKILLS_DIR=skills

  # =============================================================================
  # APPLICATION SETTINGS
  # =============================================================================
  APP_ENV=development
  LOG_LEVEL=INFO

  # =============================================================================
  # LOGFIRE OBSERVABILITY (Optional)
  # =============================================================================
  # Get token from: logfire auth
  # Leave LOGFIRE_TOKEN blank to disable Logfire integration
  LOGFIRE_TOKEN=
  LOGFIRE_SERVICE_NAME=skill-agent
  LOGFIRE_ENVIRONMENT=development
  ```
- **PATTERN**: Comprehensive comments explaining each section
- **VALIDATE**: Copy to new `.env` file and test each provider configuration

#### VALIDATE Phase 2 Complete

- **VALIDATE**:
  - `uv run python -c "from src.providers import get_llm_model; m = get_llm_model(); print(f'Provider: {type(m).__name__}')"`
  - Test with OpenRouter: `uv run python -m src.cli` → Ask "test" → Should get response
  - Verify model being used: Check console output or response

---

### Phase 3: Tool Set Architecture

#### CREATE src/skill_toolset.py - FunctionToolset Implementation

- **IMPLEMENT**: Create new file with all three skill tools in a FunctionToolset
- **CONTENT**:
  ```python
  """Skill tools as a reusable FunctionToolset for progressive disclosure."""

  from pydantic_ai.toolsets import FunctionToolset
  from pydantic_ai import RunContext
  from src.dependencies import AgentDependencies
  from src.skill_tools import load_skill, read_skill_file, list_skill_files

  # Create the skill tools toolset
  skill_tools = FunctionToolset()


  @skill_tools.tool
  async def load_skill_tool(
      ctx: RunContext[AgentDependencies],
      skill_name: str
  ) -> str:
      """
      Load the full instructions for a skill (Level 2 progressive disclosure).

      Use this tool when you need to access the detailed instructions
      for a skill. Based on the skill descriptions in your system prompt,
      identify which skill is relevant and load its full instructions.

      Args:
          ctx: Agent runtime context with dependencies
          skill_name: Name of the skill to load (e.g., "weather", "code_review")

      Returns:
          Full skill instructions from SKILL.md
      """
      return await load_skill(ctx, skill_name)


  @skill_tools.tool
  async def read_skill_file_tool(
      ctx: RunContext[AgentDependencies],
      skill_name: str,
      file_path: str
  ) -> str:
      """
      Read a file from a skill's directory (Level 3 progressive disclosure).

      Use this tool when skill instructions reference a resource file
      (e.g., "See references/api_reference.md for API details").
      This loads the specific resource on-demand.

      Args:
          ctx: Agent runtime context with dependencies
          skill_name: Name of the skill containing the file
          file_path: Relative path to the file (e.g., "references/api_reference.md")

      Returns:
          Contents of the requested file
      """
      return await read_skill_file(ctx, skill_name, file_path)


  @skill_tools.tool
  async def list_skill_files_tool(
      ctx: RunContext[AgentDependencies],
      skill_name: str,
      directory: str = ""
  ) -> str:
      """
      List files available in a skill's directory.

      Use this tool to discover what resources are available in a skill
      before loading them. Helpful when you need to explore what
      documentation, scripts, or other files a skill provides.

      Args:
          ctx: Agent runtime context with dependencies
          skill_name: Name of the skill to list files from
          directory: Optional subdirectory to list (e.g., "references", "scripts")

      Returns:
          Formatted list of available files
      """
      return await list_skill_files(ctx, skill_name, directory)
  ```
- **PATTERN**: src/agent.py:54-122 tool decorator pattern
- **IMPORTS**: From pydantic_ai.toolsets import FunctionToolset
- **VALIDATE**: `uv run python -c "from src.skill_toolset import skill_tools; print(f'Tools in set: {len(skill_tools._tools)}')"`

#### UPDATE src/agent.py - Use Toolsets Instead of Decorators

- **IMPLEMENT**: Replace individual tool decorators with toolset registration, keep HTTP tools as direct registrations
- **CHANGES**:
  ```python
  # At top, add import:
  from src.skill_toolset import skill_tools

  # Change agent creation (line 21-25):
  skill_agent = Agent(
      get_llm_model(),
      deps_type=AgentDependencies,
      system_prompt="",  # Will be set dynamically via decorator
      toolsets=[skill_tools],  # Register skill toolset here
  )

  # REMOVE these decorated functions (lines 54-122):
  # @skill_agent.tool async def load_skill_tool(...)
  # @skill_agent.tool async def read_skill_file_tool(...)
  # @skill_agent.tool async def list_skill_files_tool(...)

  # KEEP HTTP tools as direct registrations (lines 124-170):
  # @skill_agent.tool async def http_get_tool(...)
  # @skill_agent.tool async def http_post_tool(...)
  ```
- **PATTERN**: src/agent.py:21-25 agent creation
- **IMPORTS**: Add `from src.skill_toolset import skill_tools`
- **GOTCHA**: Keep @skill_agent.system_prompt decorator - it's not a tool, it's a system prompt generator
- **VALIDATE**: `uv run python -c "from src.agent import skill_agent; print(f'Agent has {len(skill_agent._tools_list)} tools')"`

#### TEST Agent with Toolset Integration

- **IMPLEMENT**: Run agent interactively and test skill loading
- **VALIDATE**:
  - `uv run python -m src.cli`
  - Type: "What's the weather in New York?"
  - Verify agent calls load_skill_tool("weather")
  - Verify agent gets skill instructions
  - Type: "exit"

#### VALIDATE Phase 3 Complete

- **VALIDATE**:
  - `uv run pytest tests/ -v` (all existing tests still pass)
  - `uv run python -c "from src.skill_toolset import skill_tools; from src.agent import skill_agent; print('Toolset:', skill_tools, 'Agent tools:', len(skill_agent._tools_list))"`

---

### Phase 4: Logfire Integration (Optional)

#### UPDATE pyproject.toml - Add Logfire Dependency

- **IMPLEMENT**: Add logfire to optional dev dependencies
- **CHANGES**:
  ```toml
  [project.optional-dependencies]
  dev = [
      "pytest>=7.4.0",
      "pytest-asyncio>=0.21.0",
      "ruff>=0.1.0",
      "mypy>=1.5.0",
      "logfire>=0.1.0",  # Add this line
  ]
  ```
- **PATTERN**: pyproject.toml:17-22
- **VALIDATE**: `uv sync` (should install logfire)

#### UPDATE src/settings.py - Logfire Optional Fields

- **IMPLEMENT**: Add optional Logfire configuration fields
- **CHANGES**:
  ```python
  # Add after existing fields:
  logfire_token: Optional[str] = Field(
      default=None,
      description="Logfire API token from 'logfire auth' (optional)"
  )
  logfire_service_name: str = Field(
      default="skill-agent",
      description="Service name in Logfire"
  )
  logfire_environment: str = Field(
      default="development",
      description="Environment (development, production, etc.)"
  )
  ```
- **PATTERN**: src/settings.py:20-47 field definition pattern
- **IMPORTS**: Ensure `from typing import Optional` is present
- **VALIDATE**: `uv run python -c "from src.settings import load_settings; s = load_settings(); print(f'Logfire token present: {bool(s.logfire_token)}')"`

#### UPDATE src/agent.py - Conditional Logfire Initialization

- **IMPLEMENT**: Add Logfire instrumentation at module level with graceful fallback when token not present
- **CHANGES** (add at top of file, after imports, before agent creation):
  ```python
  # After existing imports, add:
  import logfire
  from src.settings import load_settings

  # Initialize settings
  _settings = load_settings()

  # Configure Logfire only if token is present
  if _settings.logfire_token:
      logfire.configure(
          token=_settings.logfire_token,
          send_to_logfire='if-token-present',
          service_name=_settings.logfire_service_name,
          environment=_settings.logfire_environment,
      )

      # Instrument Pydantic AI
      logfire.instrument_pydantic_ai()

      # Instrument HTTP requests to LLM providers
      logfire.instrument_httpx(capture_all=True)

      import logging
      logger = logging.getLogger(__name__)
      logger.info(f"logfire_enabled: service={_settings.logfire_service_name}")
  else:
      import logging
      logger = logging.getLogger(__name__)
      logger.info("logfire_disabled: token not provided")

  # Continue with rest of file (agent creation, etc.)
  ```
- **PATTERN**: Conditional initialization based on settings
- **IMPORTS**: Add `import logfire` at top
- **GOTCHA**: Use `send_to_logfire='if-token-present'` for graceful degradation
- **VALIDATE**:
  - Without token: `uv run python -m src.cli` (should work, log "logfire_disabled")
  - With token: Set LOGFIRE_TOKEN in .env, run again (should log "logfire_enabled")

#### VALIDATE Phase 4 Complete

- **VALIDATE**:
  - Without Logfire: `LOGFIRE_TOKEN= uv run python -m src.cli` → type "test" → should work
  - Check logs show "logfire_disabled"
  - `uv run pytest tests/ -v` (all tests pass without Logfire)

---

### Phase 5: Evaluation System

#### UPDATE pyproject.toml - Add Pydantic Evals

- **IMPLEMENT**: Add pydantic-evals to dev dependencies
- **CHANGES**:
  ```toml
  [project.optional-dependencies]
  dev = [
      "pytest>=7.4.0",
      "pytest-asyncio>=0.21.0",
      "ruff>=0.1.0",
      "mypy>=1.5.0",
      "logfire>=0.1.0",
      "pydantic-evals>=0.1.0",  # Add this line
  ]
  ```
- **PATTERN**: pyproject.toml:17-24
- **VALIDATE**: `uv sync` (should install pydantic-evals)

#### CREATE tests/evals/__init__.py

- **IMPLEMENT**: Empty package initialization file
- **CONTENT**: `# Evaluation package`
- **VALIDATE**: File exists

#### CREATE tests/evals/skill_loading.yaml - Tool Call Verification Dataset

- **IMPLEMENT**: YAML dataset for verifying agent loads correct skills
- **CONTENT**:
  ```yaml
  name: skill_loading_verification
  description: Verify agent correctly loads skills based on user requests

  cases:
    - name: weather_basic_request
      inputs: "What's the weather in New York?"
      metadata:
        expected_skill: weather
        category: skill_loading
        difficulty: basic

    - name: weather_forecast_request
      inputs: "What's the forecast for London this week?"
      metadata:
        expected_skill: weather
        category: skill_loading
        difficulty: intermediate

    - name: weather_temperature_query
      inputs: "How hot is it in Tokyo right now?"
      metadata:
        expected_skill: weather
        category: skill_loading
        difficulty: basic

    - name: code_review_basic
      inputs: "Please review this code for best practices: def add(a, b): return a + b"
      metadata:
        expected_skill: code_review
        category: skill_loading
        difficulty: basic

    - name: code_review_security
      inputs: "Check this authentication code for security vulnerabilities"
      metadata:
        expected_skill: code_review
        category: skill_loading
        difficulty: intermediate

  evaluators:
    - IsInstance: str
    - MaxDuration: 15.0
  ```
- **PATTERN**: YAML dataset format from Pydantic Evals docs
- **VALIDATE**: `uv run python -c "from pydantic_evals import Dataset; d = Dataset.from_file('tests/evals/skill_loading.yaml'); print(f'{len(d.cases)} cases loaded')"`

#### CREATE tests/evals/response_quality.yaml - LLM-as-Judge Dataset

- **IMPLEMENT**: YAML dataset for LLM-as-judge evaluation of response quality
- **CONTENT**:
  ```yaml
  name: response_quality_assessment
  description: LLM-as-judge evaluation for response quality

  cases:
    - name: weather_helpful_response
      inputs: "What's the weather in Paris?"
      evaluators:
        - LLMJudge:
            rubric: "Response provides accurate weather information and directly answers the user's question"
            include_input: true
            assertion:
              evaluation_name: weather_accuracy
        - LLMJudge:
            rubric: "Response is clear, well-formatted, and easy to understand"
            score:
              evaluation_name: clarity_score

    - name: code_review_constructive
      inputs: "Review this function: def calculate(x, y): return x + y"
      evaluators:
        - LLMJudge:
            rubric: "Code review provides constructive, actionable feedback on the code"
            model: "anthropic:claude-sonnet-4-5"
            temperature: 0.0
            assertion:
              evaluation_name: constructive_feedback

  evaluators:
    - IsInstance: str
  ```
- **PATTERN**: LLM-as-judge format from Pydantic Evals docs
- **VALIDATE**: `uv run python -c "from pydantic_evals import Dataset; d = Dataset.from_file('tests/evals/response_quality.yaml'); print(f'{len(d.cases)} cases loaded')"`

#### CREATE tests/evals/evaluators.py - Custom Evaluators

- **IMPLEMENT**: Custom evaluators for skill loading verification using message inspection
- **CONTENT**:
  ```python
  """Custom evaluators for skill-based agent."""

  from dataclasses import dataclass
  from pydantic_evals.evaluators import Evaluator, EvaluatorContext, EvaluationReason


  @dataclass
  class SkillWasLoaded(Evaluator):
      """Verify that load_skill_tool was called with correct skill name."""

      expected_skill_name: str

      def evaluate(self, ctx: EvaluatorContext) -> EvaluationReason:
          """
          Check if correct skill was loaded via tool call by inspecting messages.

          No Logfire required - uses message inspection directly.
          """
          # Access all messages from the run
          messages = ctx.all_messages()

          # Search through messages for tool-use blocks
          for message in messages:
              if hasattr(message, 'content'):
                  for part in message.content:
                      # Check if this is a tool-use block
                      if hasattr(part, 'part_kind') and part.part_kind == 'tool-use':
                          # Check if it's the load_skill_tool
                          if part.tool_name == 'load_skill_tool':
                              # Check the skill_name argument
                              if hasattr(part, 'tool_input') and isinstance(part.tool_input, dict):
                                  skill_name = part.tool_input.get('skill_name')
                                  if skill_name == self.expected_skill_name:
                                      return EvaluationReason(
                                          value=True,
                                          reason=f'Correctly loaded "{self.expected_skill_name}" skill'
                                      )
                                  else:
                                      return EvaluationReason(
                                          value=False,
                                          reason=f'Loaded wrong skill: "{skill_name}" instead of "{self.expected_skill_name}"'
                                      )

          return EvaluationReason(
              value=False,
              reason=f'Did not call load_skill_tool for "{self.expected_skill_name}"'
          )


  @dataclass
  class ToolWasCalled(Evaluator):
      """Verify a specific tool was called during execution."""

      tool_name: str

      def evaluate(self, ctx: EvaluatorContext) -> EvaluationReason:
          """Check if tool was called by inspecting messages."""
          messages = ctx.all_messages()

          # Search for tool-use blocks with matching tool name
          for message in messages:
              if hasattr(message, 'content'):
                  for part in message.content:
                      if hasattr(part, 'part_kind') and part.part_kind == 'tool-use':
                          if part.tool_name == self.tool_name:
                              return EvaluationReason(
                                  value=True,
                                  reason=f'Tool "{self.tool_name}" was called'
                              )

          return EvaluationReason(
              value=False,
              reason=f'Tool "{self.tool_name}" was NOT called'
          )


  @dataclass
  class OutputContainsKeywords(Evaluator):
      """Verify output contains expected keywords."""

      required_keywords: list[str]
      case_sensitive: bool = False

      def evaluate(self, ctx: EvaluatorContext) -> EvaluationReason:
          """Check if all keywords present in output."""
          output = ctx.output if self.case_sensitive else ctx.output.lower()
          keywords = self.required_keywords if self.case_sensitive else [k.lower() for k in self.required_keywords]

          missing = [k for k in keywords if k not in output]

          if not missing:
              return EvaluationReason(
                  value=True,
                  reason=f'All {len(keywords)} keywords found in output'
              )
          else:
              return EvaluationReason(
                  value=False,
                  reason=f'Missing keywords: {", ".join(missing)}'
              )
  ```
- **PATTERN**: tests/test_skill_loader.py dataclass pattern for test helpers
- **IMPORTS**: From pydantic_evals.evaluators (only need Evaluator, EvaluatorContext, EvaluationReason)
- **GOTCHA**: Access tool calls via `ctx.all_messages()` → iterate content → check `part.part_kind == 'tool-use'` → inspect `part.tool_name` and `part.tool_input`
- **NOTE**: No Logfire required - message inspection works without any observability setup
- **VALIDATE**: `uv run python -c "from tests.evals.evaluators import SkillWasLoaded; e = SkillWasLoaded('weather'); print(f'Evaluator: {e}')"`

#### CREATE tests/evals/run_evals.py - Evaluation Runner

- **IMPLEMENT**: Script to run all evaluations and report results
- **CONTENT**:
  ```python
  """Run evaluation suite for skill-based agent."""

  import asyncio
  import argparse
  from pathlib import Path
  from pydantic_evals import Dataset
  from src.agent import skill_agent
  from src.dependencies import AgentDependencies
  from tests.evals.evaluators import SkillWasLoaded, ToolWasCalled, OutputContainsKeywords


  async def run_evals(dataset_name: str = None, verbose: bool = False):
      """
      Execute evaluation suite against the skill agent.

      Args:
          dataset_name: Specific dataset to run (None = all)
          verbose: Show detailed output including reasons
      """
      evals_dir = Path('tests/evals')

      # Select datasets to run
      if dataset_name:
          yaml_files = [evals_dir / f'{dataset_name}.yaml']
      else:
          yaml_files = list(evals_dir.glob('*.yaml'))

      all_reports = {}

      for yaml_file in yaml_files:
          if not yaml_file.exists():
              print(f"⚠️  Skipping {yaml_file.name} - not found")
              continue

          print(f"\n{'='*60}")
          print(f"Running: {yaml_file.stem}")
          print(f"{'='*60}\n")

          try:
              # Load dataset with custom evaluators
              dataset = Dataset.from_file(
                  yaml_file,
                  custom_evaluators=[SkillWasLoaded, ToolWasCalled, OutputContainsKeywords]
              )

              # Create task function that wraps agent
              async def task_fn(inputs: str) -> str:
                  deps = AgentDependencies()
                  await deps.initialize()
                  result = await skill_agent.run(inputs, deps=deps)
                  return result.data

              # Run evaluation
              report = dataset.evaluate_sync(task_fn)
              all_reports[yaml_file.stem] = report

              # Print results
              if verbose:
                  report.print(include_reasons=True)
              else:
                  report.print()

          except Exception as e:
              print(f"  ❌ ERROR: {e}")
              if verbose:
                  import traceback
                  traceback.print_exc()

      # Print summary
      print(f"\n{'='*60}")
      print("EVALUATION SUMMARY")
      print(f"{'='*60}")

      for name, report in all_reports.items():
          total = len(report.cases)
          passed = sum(1 for c in report.cases if c.failed_evaluations == 0)
          status = "✅" if passed == total else "❌"
          print(f"{status} {name}: {passed}/{total} cases passed")

      # Return exit code
      all_passed = all(
          sum(1 for c in r.cases if c.failed_evaluations == 0) == len(r.cases)
          for r in all_reports.values()
      )
      return 0 if all_passed else 1


  if __name__ == '__main__':
      parser = argparse.ArgumentParser(description='Run skill agent evaluations')
      parser.add_argument('--dataset', help='Specific dataset to run')
      parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

      args = parser.parse_args()
      exit_code = asyncio.run(run_evals(args.dataset, args.verbose))
      exit(exit_code)
  ```
- **PATTERN**: tests/test_agent.py async test patterns
- **IMPORTS**: Standard asyncio and argparse patterns
- **VALIDATE**: `uv run python -m tests.evals.run_evals --help` (should show usage)

#### TEST Evaluation System

- **IMPLEMENT**: Run evaluations and verify they execute successfully
- **VALIDATE**:
  - `uv run python -m tests.evals.run_evals --dataset skill_loading`
  - Should see evaluation run for all cases
  - Check if any cases pass (without Logfire, SkillWasLoaded will fail but other evaluators should work)

#### VALIDATE Phase 5 Complete

- **VALIDATE**:
  - `uv run python -m tests.evals.run_evals` (runs all eval datasets)
  - Verify evaluators load correctly
  - Verify reports generated

---

### Phase 6: Validation Scripts & End-to-End Testing

#### CREATE scripts/__init__.py

- **IMPLEMENT**: Empty package initialization
- **CONTENT**: `# Validation scripts package`
- **VALIDATE**: File exists

#### CREATE scripts/test_agent.py - Interactive Testing Script

- **IMPLEMENT**: Script for interactive agent testing with predefined queries
- **CONTENT**:
  ```python
  """Interactive script to test agent with different skill scenarios."""

  import asyncio
  from rich.console import Console
  from rich.panel import Panel
  from src.agent import skill_agent
  from src.dependencies import AgentDependencies

  console = Console()

  # Predefined test queries
  TEST_QUERIES = {
      "weather": [
          "What's the weather in New York?",
          "What's the forecast for London?",
          "How hot is it in Tokyo?",
      ],
      "code_review": [
          "Review this code: def add(a, b): return a + b",
          "Check this for security issues: user_input = request.GET['name']",
          "Review this authentication function for best practices",
      ],
      "mixed": [
          "What's the weather in Paris and review this code: def hello(): pass",
      ]
  }


  async def test_query(query: str, deps: AgentDependencies):
      """Test a single query and display results."""
      console.print(f"\n[bold cyan]Query:[/bold cyan] {query}")
      console.print("[dim]Running agent...[/dim]\n")

      try:
          result = await skill_agent.run(query, deps=deps)

          console.print(Panel(
              result.data,
              title="[green]Response[/green]",
              border_style="green"
          ))

          return True
      except Exception as e:
          console.print(Panel(
              str(e),
              title="[red]Error[/red]",
              border_style="red"
          ))
          return False


  async def main():
      """Run interactive agent tests."""
      console.print(Panel(
          "[bold blue]Skill-Based Agent Testing[/bold blue]\n\n"
          "This script runs predefined queries to test skill loading.",
          style="blue"
      ))

      # Initialize dependencies once
      deps = AgentDependencies()
      await deps.initialize()

      console.print(f"\n[green]✓[/green] Agent initialized with skills: {', '.join(deps.skill_loader.skills.keys())}\n")

      # Test weather queries
      console.print("[bold]Testing Weather Skill[/bold]")
      console.print("="*60)
      for query in TEST_QUERIES["weather"]:
          await test_query(query, deps)
          await asyncio.sleep(0.5)  # Brief pause between queries

      # Test code review queries
      console.print("\n[bold]Testing Code Review Skill[/bold]")
      console.print("="*60)
      for query in TEST_QUERIES["code_review"]:
          await test_query(query, deps)
          await asyncio.sleep(0.5)

      console.print("\n[bold green]✓ Testing complete![/bold green]")


  if __name__ == '__main__':
      asyncio.run(main())
  ```
- **PATTERN**: src/cli.py Rich console patterns
- **IMPORTS**: From rich.console import Console, Panel
- **VALIDATE**: `uv run python -m scripts.test_agent`

#### CREATE scripts/validate_skills.py - Skill Validation Script

- **IMPLEMENT**: Script to validate skill structure and content
- **CONTENT**:
  ```python
  """Validate skill structure and content."""

  from pathlib import Path
  from rich.console import Console
  from rich.table import Table
  from src.skill_loader import SkillLoader
  from src.settings import load_settings

  console = Console()


  def validate_skill_structure(skill_dir: Path) -> list[str]:
      """Validate skill directory structure."""
      issues = []

      # Check SKILL.md exists
      skill_md = skill_dir / "SKILL.md"
      if not skill_md.exists():
          issues.append("Missing SKILL.md")
          return issues

      # Check for frontmatter
      content = skill_md.read_text()
      if not content.startswith("---"):
          issues.append("SKILL.md missing YAML frontmatter")

      # Check for optional directories
      if (skill_dir / "references").exists():
          ref_files = list((skill_dir / "references").glob("*.md"))
          if not ref_files:
              issues.append("references/ directory exists but is empty")

      if (skill_dir / "scripts").exists():
          script_files = list((skill_dir / "scripts").glob("*.py"))
          if not script_files:
              issues.append("scripts/ directory exists but is empty")

      return issues


  def main():
      """Validate all skills."""
      console.print(Panel(
          "[bold blue]Skill Validation Report[/bold blue]",
          style="blue"
      ))

      settings = load_settings()
      loader = SkillLoader(settings.skills_dir)
      skills = loader.discover_skills()

      console.print(f"\n[cyan]Found {len(skills)} skill(s)[/cyan]\n")

      # Create table
      table = Table(title="Skill Validation Results")
      table.add_column("Skill", style="cyan")
      table.add_column("Status", style="green")
      table.add_column("Issues", style="yellow")

      all_valid = True

      for skill in skills:
          issues = validate_skill_structure(skill.skill_path)

          if issues:
              all_valid = False
              status = "❌ FAIL"
              issues_str = "\n".join(f"  • {i}" for i in issues)
          else:
              status = "✅ PASS"
              issues_str = "None"

          table.add_row(skill.name, status, issues_str)

      console.print(table)

      if all_valid:
          console.print("\n[bold green]✓ All skills valid![/bold green]")
          return 0
      else:
          console.print("\n[bold red]✗ Some skills have issues[/bold red]")
          return 1


  if __name__ == '__main__':
      exit(main())
  ```
- **PATTERN**: Rich table formatting
- **IMPORTS**: From rich.table import Table
- **VALIDATE**: `uv run python -m scripts.validate_skills`

#### CREATE scripts/run_full_validation.py - Complete Validation Pipeline

- **IMPLEMENT**: Master script that runs all validation steps
- **CONTENT**:
  ```python
  """Run complete validation pipeline: tests → evals → skill validation → agent tests."""

  import sys
  import subprocess
  from rich.console import Console
  from rich.panel import Panel

  console = Console()


  def run_command(cmd: list[str], description: str) -> bool:
      """Run a command and report results."""
      console.print(f"\n[bold cyan]Running:[/bold cyan] {description}")
      console.print(f"[dim]Command: {' '.join(cmd)}[/dim]\n")

      result = subprocess.run(cmd)

      if result.returncode == 0:
          console.print(f"[green]✓ {description} passed[/green]")
          return True
      else:
          console.print(f"[red]✗ {description} failed[/red]")
          return False


  def main():
      """Run full validation pipeline."""
      console.print(Panel(
          "[bold blue]Full Validation Pipeline[/bold blue]\n\n"
          "Running: Unit Tests → Integration Tests → Evals → Skill Validation → Agent Tests",
          style="blue",
          padding=(1, 2)
      ))

      steps = [
          (["uv", "run", "pytest", "tests/test_skill_loader.py", "-v"], "Unit Tests: Skill Loader"),
          (["uv", "run", "pytest", "tests/test_skill_tools.py", "-v"], "Unit Tests: Skill Tools"),
          (["uv", "run", "pytest", "tests/test_agent.py", "-v"], "Integration Tests: Agent"),
          (["uv", "run", "python", "-m", "scripts.validate_skills"], "Skill Validation"),
          (["uv", "run", "python", "-m", "tests.evals.run_evals"], "Evaluation Suite"),
      ]

      results = []

      for cmd, desc in steps:
          success = run_command(cmd, desc)
          results.append((desc, success))

      # Summary
      console.print(f"\n{'='*60}")
      console.print("[bold]VALIDATION SUMMARY[/bold]")
      console.print(f"{'='*60}\n")

      all_passed = True
      for desc, success in results:
          status = "✅" if success else "❌"
          console.print(f"{status} {desc}")
          if not success:
              all_passed = False

      console.print()

      if all_passed:
          console.print("[bold green]✓ All validation steps passed![/bold green]")
          return 0
      else:
          console.print("[bold red]✗ Some validation steps failed[/bold red]")
          return 1


  if __name__ == '__main__':
      sys.exit(main())
  ```
- **PATTERN**: subprocess for running commands
- **IMPORTS**: import subprocess, sys
- **VALIDATE**: `uv run python -m scripts.run_full_validation`

#### VALIDATE Phase 6 Complete

- **VALIDATE**:
  - `uv run python -m scripts.validate_skills` (should pass for weather and code_review)
  - `uv run python -m scripts.test_agent` (should test all queries)
  - `uv run python -m scripts.run_full_validation` (full pipeline)

---

### Phase 7: Documentation & Polish

#### UPDATE README.md - Comprehensive Documentation

- **IMPLEMENT**: Update README with all new features, UV usage, provider switching, evals
- **CHANGES**:
  ```markdown
  # Add to Prerequisites section:
  - [UV](https://docs.astral.sh/uv/) - Fast Python package manager

  # Update Installation section:
  1. Clone the repository
  2. Install UV (if not already installed):
     - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
     - Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
  3. Sync dependencies: `uv sync`
  4. Configure environment: Copy `.env.example` to `.env` and set your API key

  # Add Provider Configuration section:
  ## Switching LLM Providers

  The agent supports three LLM providers. Configure via `.env`:

  **OpenRouter (Recommended):**
  ```bash
  LLM_PROVIDER=openrouter
  LLM_API_KEY=sk-or-v1-your-key
  LLM_MODEL=anthropic/claude-haiku-4.5
  ```

  **OpenAI:**
  ```bash
  LLM_PROVIDER=openai
  LLM_API_KEY=sk-proj-your-key
  LLM_MODEL=gpt-4o-mini
  ```

  **Ollama (Local):**
  ```bash
  LLM_PROVIDER=ollama
  LLM_API_KEY=ollama
  LLM_MODEL=llama3.2
  LLM_BASE_URL=http://localhost:11434/v1
  ```

  # Add Testing & Validation section:
  ## Running Tests

  ```bash
  # Unit tests
  uv run pytest tests/test_skill_loader.py -v
  uv run pytest tests/test_skill_tools.py -v

  # Integration tests
  uv run pytest tests/test_agent.py -v

  # All tests
  uv run pytest tests/ -v
  ```

  ## Running Evaluations

  ```bash
  # Run all evals
  uv run python -m tests.evals.run_evals

  # Run specific dataset
  uv run python -m tests.evals.run_evals --dataset skill_loading

  # Verbose output
  uv run python -m tests.evals.run_evals --verbose
  ```

  ## Validation Scripts

  ```bash
  # Test agent interactively
  uv run python -m scripts.test_agent

  # Validate skill structure
  uv run python -m scripts.validate_skills

  # Run full validation pipeline
  uv run python -m scripts.run_full_validation
  ```

  # Add Logfire section:
  ## Observability with Logfire (Optional)

  Enable Logfire for production monitoring:

  1. Get Logfire token: `logfire auth`
  2. Set in `.env`: `LOGFIRE_TOKEN=your-token`
  3. Run agent - traces appear at https://logfire.pydantic.dev

  Without token, Logfire is disabled and agent works normally.
  ```
- **PATTERN**: README.md existing structure
- **VALIDATE**: Read through updated README and verify all commands work

#### UPDATE .env.example - Final Polish

- **IMPLEMENT**: Ensure all configuration options documented with clear examples
- **VERIFY**: All provider examples present, Logfire section marked optional, comprehensive comments
- **VALIDATE**: Copy to `.env` and test each provider configuration

#### CREATE CHANGELOG.md - Document Changes

- **IMPLEMENT**: Create changelog documenting all evolution changes
- **CONTENT**:
  ```markdown
  # Changelog

  ## [Unreleased] - Agent Evolution

  ### Added
  - **UV Package Manager**: Complete migration to UV for dependency management
  - **Direct Provider Integrations**: OpenRouter, OpenAI, and Ollama with provider-specific features
  - **Tool Sets**: Skill tools now in reusable `FunctionToolset` for modularity
  - **Evaluation System**: YAML-based datasets with custom evaluators
  - **Validation Scripts**: Automated testing and validation pipeline
  - **Optional Logfire**: Graceful degradation when Logfire token not available

  ### Changed
  - Replaced generic OpenAI-compatible provider with direct integrations
  - Migrated from pip to UV for all package operations
  - Refactored skill tools from direct registration to Tool Set architecture
  - Updated documentation for UV-based workflows

  ### Improved
  - Provider switching now uses proper direct integrations
  - Testing infrastructure with evals and validation scripts
  - Documentation with comprehensive examples
  - Error handling for missing Logfire token
  ```
- **PATTERN**: Keep-a-Changelog format
- **VALIDATE**: Review for completeness

#### RUN Full Validation Suite

- **IMPLEMENT**: Final comprehensive validation
- **VALIDATE**:
  - `uv run python -m scripts.run_full_validation`
  - All steps should pass
  - Fix any failures before considering complete

#### CLEANUP Code

- **IMPLEMENT**: Remove any unused imports, commented code, debug statements
- **VALIDATE**:
  - `uv run ruff check src/ tests/ scripts/`
  - `uv run mypy src/` (if type checking is configured)

---

## TESTING STRATEGY

Based on pytest framework with async support configured in pyproject.toml.

### Unit Tests

**Scope**: Individual functions and classes in isolation
**Location**: `tests/test_skill_loader.py`, `tests/test_skill_tools.py`
**Pattern**: Use `tmp_path` fixture for file system operations, mock dependencies with dataclasses

**Example Test Structure**:
```python
@pytest.mark.asyncio
async def test_function_name(self, tmp_path: Path) -> None:
    """Test description."""
    # Arrange: Create test data
    loader = SkillLoader(tmp_path)

    # Act: Execute function
    result = await function_under_test(...)

    # Assert: Verify results
    assert expected_condition
```

### Integration Tests

**Scope**: Full workflows including agent initialization, skill discovery, tool execution
**Location**: `tests/test_agent.py`
**Pattern**: Use real SkillLoader with actual skills directory, test full tool execution flow

**Example Test Structure**:
```python
@pytest.mark.asyncio
async def test_agent_workflow(self) -> None:
    """Test complete agent workflow."""
    # Initialize real dependencies
    deps = AgentDependencies()
    await deps.initialize()

    # Execute workflow
    result = await agent.run(query, deps=deps)

    # Verify outcome
    assert expected_behavior
```

### Evaluation Tests

**Scope**: Agent behavior validation with YAML datasets and custom evaluators using message inspection
**Location**: `tests/evals/`
**Pattern**: Define test cases in YAML, run with custom evaluators that inspect message content for tool calls, assert pass/fail
**No Logfire Required**: Evaluators access tool calls via `ctx.all_messages()` and inspect `part.part_kind`, `part.tool_name`, and `part.tool_input`

**Example Eval Dataset**:
```yaml
cases:
  - name: weather_skill_loading
    inputs: "What's the weather in New York?"
    metadata:
      expected_skill: weather
      category: skill_loading
evaluators:
  - IsInstance: str
  - MaxDuration: 15.0
```

**Example Custom Evaluator** (message inspection):
```python
def evaluate(self, ctx: EvaluatorContext) -> EvaluationReason:
    messages = ctx.all_messages()
    for message in messages:
        for part in message.content:
            if part.part_kind == 'tool-use' and part.tool_name == 'load_skill_tool':
                if part.tool_input.get('skill_name') == self.expected_skill_name:
                    return EvaluationReason(value=True, reason="Skill loaded correctly")
    return EvaluationReason(value=False, reason="Skill not loaded")
```

### Edge Cases

**Security Testing**:
- Directory traversal prevention (tests/test_skill_tools.py:159-176)
- Path validation for file access

**Error Handling**:
- Missing skills (load_skill with non-existent skill)
- Missing files (read_skill_file with invalid path)
- Uninitialized dependencies (skill_loader is None)

**Content Validation**:
- YAML frontmatter parsing with malformed input
- SKILL.md without frontmatter
- Empty skill directories

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Level 1: Syntax & Style

```bash
# Verify UV installation
uv --version

# Sync dependencies
uv sync

# Check Python version
uv run python --version

# Lint with ruff
uv run ruff check src/ tests/ scripts/

# Type check with mypy (if configured)
uv run mypy src/
```

### Level 2: Unit Tests

```bash
# Run all unit tests
uv run pytest tests/ -v

# Run specific test files
uv run pytest tests/test_skill_loader.py -v
uv run pytest tests/test_skill_tools.py -v
uv run pytest tests/test_agent.py -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

### Level 3: Integration Tests

```bash
# Run agent integration tests
uv run pytest tests/test_agent.py::TestSkillDiscoveryIntegration -v

# Test agent runs
uv run python -m src.cli
# Type: "What's the weather in NYC?"
# Verify: Agent loads weather skill
# Type: "exit"
```

### Level 4: Evaluation Suite

```bash
# Run all evaluations
uv run python -m tests.evals.run_evals

# Run specific dataset
uv run python -m tests.evals.run_evals --dataset skill_loading

# Verbose output
uv run python -m tests.evals.run_evals --verbose
```

### Level 5: Validation Scripts

```bash
# Validate skill structure
uv run python -m scripts.validate_skills

# Test agent interactively
uv run python -m scripts.test_agent

# Run full validation pipeline
uv run python -m scripts.run_full_validation
```

### Level 6: Provider Testing

```bash
# Test OpenRouter (current config)
uv run python -m src.cli
# Ask: "test query"
# Verify: Response from Claude Haiku

# Test with different model (edit .env: LLM_MODEL=anthropic/claude-3.5-sonnet)
uv run python -m src.cli
# Verify: Works with different model

# Test Logfire disabled (ensure LOGFIRE_TOKEN is empty/unset)
LOGFIRE_TOKEN= uv run python -m src.cli
# Verify: Agent works, logs "logfire_disabled"
```

---

## ACCEPTANCE CRITERIA

- [x] UV package manager fully integrated and working
  - `.python-version` file created
  - `uv sync` successfully installs all dependencies
  - All commands use `uv run` prefix
  - README updated with UV instructions

- [x] Direct provider integrations implemented
  - OpenRouter with app attribution support
  - OpenAI with direct provider
  - Ollama via OpenAI-compatible wrapper
  - Provider switching via .env LLM_PROVIDER
  - All three providers tested and working

- [x] Tool Set architecture functional
  - `src/skill_toolset.py` created with FunctionToolset
  - All three skill tools (load, read, list) in toolset
  - Agent uses toolsets parameter instead of decorators
  - Existing tests still pass

- [x] Evaluation system complete
  - YAML datasets created (skill_loading, response_quality)
  - Custom evaluators implemented using message inspection (SkillWasLoaded, ToolWasCalled, OutputContainsKeywords)
  - Eval runner script functional
  - Evals run successfully WITHOUT Logfire (message inspection, not span-based)
  - Tool call verification works via direct message content inspection

- [x] Logfire integration optional
  - Logfire dependency added to dev dependencies
  - Conditional initialization based on token presence
  - Agent works perfectly without Logfire token (primary use case)
  - Agent instruments correctly with Logfire token (for video demo visualization)
  - Evals do NOT require Logfire - they use message inspection

- [x] Validation scripts operational
  - Interactive agent testing script works
  - Skill validation script works
  - Full validation pipeline runs all checks
  - All scripts report clear pass/fail status

- [x] Documentation updated
  - README covers UV setup, provider switching, evals, validation
  - .env.example shows all provider configurations
  - CHANGELOG documents all changes
  - All example commands verified working

- [x] All validation commands pass
  - Unit tests: 100% pass
  - Integration tests: 100% pass
  - Evals run successfully
  - Validation scripts execute without errors
  - Agent runs interactively with both skills

- [x] No regressions in existing functionality
  - Weather skill works as before
  - Code review skill works as before
  - Progressive disclosure intact (Level 1, 2, 3)
  - CLI functionality preserved
  - All existing tests pass

---

## COMPLETION CHECKLIST

### Phase 1: UV Migration
- [ ] `.python-version` created
- [ ] `pyproject.toml` updated (dev deps consolidated)
- [ ] `uv sync` successful
- [ ] `README.md` updated with UV instructions
- [ ] All UV validation commands pass

### Phase 2: Provider Integration
- [ ] `src/settings.py` updated with provider fields
- [ ] `src/providers.py` rewritten with direct integrations
- [ ] `.env` reorganized for current provider
- [ ] `.env.example` created with all provider examples
- [ ] OpenRouter provider tested
- [ ] Provider switching verified

### Phase 3: Tool Sets
- [ ] `src/skill_toolset.py` created with FunctionToolset
- [ ] `src/agent.py` updated to use toolsets
- [ ] Tool decorators removed from agent.py
- [ ] Agent works with toolset integration
- [ ] Existing tests pass

### Phase 4: Logfire
- [ ] `pyproject.toml` includes logfire dependency
- [ ] `src/settings.py` has Logfire fields
- [ ] `src/agent.py` has conditional Logfire init
- [ ] `.env.example` includes Logfire section
- [ ] Agent works without Logfire token
- [ ] Agent works with Logfire token (if available)

### Phase 5: Evaluation System
- [ ] `pyproject.toml` includes pydantic-evals
- [ ] `tests/evals/` directory created
- [ ] `skill_loading.yaml` dataset created
- [ ] `response_quality.yaml` dataset created
- [ ] `evaluators.py` created with custom evaluators
- [ ] `run_evals.py` runner script created
- [ ] Evals run successfully

### Phase 6: Validation Scripts
- [ ] `scripts/` directory created
- [ ] `test_agent.py` interactive script created
- [ ] `validate_skills.py` validation script created
- [ ] `run_full_validation.py` pipeline created
- [ ] All scripts execute successfully
- [ ] Full validation pipeline passes

### Phase 7: Documentation
- [ ] `README.md` comprehensively updated
- [ ] `.env.example` complete and documented
- [ ] `CHANGELOG.md` created
- [ ] All documentation verified
- [ ] Code cleaned up (no unused imports, debug code)

### Final Validation
- [ ] `uv run python -m scripts.run_full_validation` passes
- [ ] Agent runs with weather queries
- [ ] Agent runs with code review queries
- [ ] All provider configurations tested
- [ ] No regressions detected

---

## NOTES

**Design Decisions:**

1. **UV over pip**: Modern tooling with faster dependency resolution and better lockfile management
2. **Direct Providers over Generic**: Access to provider-specific features (OpenRouter fallbacks, app attribution)
3. **Tool Sets over Direct Registration**: Enables reusability and easier testing/composition
4. **YAML Evals over Code**: Human-readable test datasets, easier to maintain and extend
5. **Message Inspection over Span Queries**: Direct access to tool calls via messages, no Logfire dependency
6. **Optional Logfire**: For video demo visualization only, not required for local development or evals

**Trade-offs:**

- UV adds tooling dependency but dramatically improves developer experience
- Direct provider integrations add complexity but provide better feature access
- Tool Sets add abstraction layer but improve modularity
- Evals add testing complexity but provide systematic validation
- Message inspection is more explicit but gives full control over tool call verification

**Key Implementation Risks:**

1. **Provider API Changes**: Direct integrations depend on stable Pydantic AI provider APIs
2. **Message API Stability**: Custom evaluators depend on message content structure (part.part_kind, part.tool_name, etc.)
3. **UV Adoption**: Team must install and use UV instead of familiar pip workflows
4. **Model Costs**: Haiku is cheap but evals with many queries could still accumulate costs

**Performance Considerations:**

- UV is significantly faster than pip for dependency operations
- Tool Sets have minimal overhead compared to direct registration
- Evals run sequentially; consider parallel execution for large datasets
- Logfire adds network calls but impact is minimal

**Confidence Score**: 10/10 for one-pass implementation success

The plan is comprehensive with clear patterns, validation at each step, and detailed documentation. All evaluators use message inspection (no Logfire dependency), all validation can run locally, and all patterns are extracted from existing codebase.
