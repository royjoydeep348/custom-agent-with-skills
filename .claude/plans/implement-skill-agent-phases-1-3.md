# Feature: Custom Skill-Based Pydantic AI Agent - Phases 1-3

The following plan should be complete, but it's important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils, types, and models. Import from the right files etc.

## Feature Description

Implement Phases 1-3 of the Custom Skill-Based Pydantic AI Agent:

1. **Phase 1 - Skill Infrastructure**: Build `SkillLoader` class for skill discovery, `SkillMetadata` Pydantic model, YAML frontmatter parsing, and `AgentDependencies` dataclass
2. **Phase 2 - Progressive Disclosure Tools**: Implement `load_skill()`, `read_skill_file()`, and `list_skill_files()` tools for three-level progressive disclosure
3. **Phase 3 - Agent Integration**: Create Pydantic AI agent with skill tools, dynamic system prompts, and CLI integration

This implements the core progressive disclosure pattern that enables AI agents to scale beyond context window limitations by loading skills on-demand.

## User Story

As a **Python AI developer**
I want to **build an agent with modular, reusable skills that load on-demand**
So that **I can include comprehensive documentation and capabilities without consuming context upfront**

## Problem Statement

AI agents face context window limitations when including large reference documentation. Claude Skills solve this through progressive disclosure but are locked to Claude's ecosystem. This project extracts that pattern and makes it framework-agnostic, available to any Pydantic AI agent.

## Solution Statement

Implement a three-level progressive disclosure system:
- **Level 1**: Minimal skill metadata in system prompt (~100 tokens/skill)
- **Level 2**: Full instructions loaded via `load_skill()` tool when needed
- **Level 3**: Specific resources loaded via `read_skill_file()` only when referenced

The system uses YAML frontmatter in `SKILL.md` files for metadata, with Pydantic models for type safety and validation.

## Feature Metadata

**Feature Type**: New Capability
**Estimated Complexity**: Medium-High
**Primary Systems Affected**: src/skill_loader.py, src/skill_tools.py, src/dependencies.py, src/agent.py, src/cli.py
**Dependencies**: pydantic-ai, pydantic, pydantic-settings, rich, python-dotenv, pyyaml

---

## CONTEXT REFERENCES

### Relevant Codebase Files IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

- `examples/dependencies.py` (lines 14-127) - **Why**: AgentDependencies pattern with dataclass, Optional fields, initialize/cleanup lifecycle
- `examples/agent.py` (lines 1-97) - **Why**: Agent creation, tool registration with @agent.tool, RunContext usage
- `examples/tools.py` (lines 15-45, 242-313) - **Why**: Pydantic BaseModel for SearchResult, async function patterns, error handling
- `examples/settings.py` (lines 12-90) - **Why**: BaseSettings pattern with ConfigDict, Field descriptors
- `examples/providers.py` (lines 9-29) - **Why**: get_llm_model() function pattern
- `examples/cli.py` (lines 25-157, 178-252) - **Why**: Streaming patterns with agent.iter(), Rich console output
- `examples/prompts.py` (lines 1-31) - **Why**: System prompt structure
- `src/settings.py` (lines 1-58) - **Why**: Already adapted Settings with skills_dir field
- `src/providers.py` (lines 1-62) - **Why**: Already adapted providers (reuse as-is)
- `src/prompts.py` (lines 1-49) - **Why**: Already adapted prompts with `{skill_metadata}` placeholder
- `src/cli.py` (lines 1-254) - **Why**: Already adapted CLI (needs agent import uncommented)
- `.claude/PRD.md` (lines 603-680) - **Why**: Complete build order and task specifications

### New Files to Create

- `src/skill_loader.py` - SkillLoader class and SkillMetadata Pydantic model
- `src/skill_tools.py` - Progressive disclosure tool functions
- `src/dependencies.py` - AgentDependencies dataclass (simpler than examples, no MongoDB)
- `src/agent.py` - Pydantic AI agent with skill tools
- `tests/test_skill_loader.py` - Unit tests for skill discovery
- `tests/test_skill_tools.py` - Unit tests for progressive disclosure tools
- `pyproject.toml` - Project configuration with uv
- `skills/weather/SKILL.md` - Demo skill for validation
- `.python-version` - Pin Python version for uv

### Relevant Documentation YOU SHOULD READ THESE BEFORE IMPLEMENTING!

- [Pydantic AI Agents](https://ai.pydantic.dev/agents/)
  - Section: Creating agents with dynamic system prompts
  - **Why**: Core pattern for @agent.system_prompt decorator
- [Pydantic AI Tools](https://ai.pydantic.dev/tools/)
  - Section: @agent.tool decorator and RunContext
  - **Why**: Tool registration pattern with typed context
- [Pydantic AI Dependencies](https://ai.pydantic.dev/dependencies/)
  - Section: Dependency injection with RunContext
  - **Why**: Pattern for injecting SkillLoader into tools
- [Pydantic AI Message History](https://ai.pydantic.dev/message-history/)
  - Section: Maintaining conversation context
  - **Why**: Pattern for message_history in agent.iter()
- [UV Project Guide](https://docs.astral.sh/uv/guides/projects/)
  - Section: pyproject.toml structure
  - **Why**: Project initialization with uv

### Patterns to Follow

**Naming Conventions:**
- Classes: PascalCase (`SkillLoader`, `SkillMetadata`, `AgentDependencies`)
- Functions: snake_case (`load_skill`, `read_skill_file`, `discover_skills`)
- Variables: snake_case (`skill_loader`, `skill_metadata`, `skill_path`)
- Constants: UPPER_SNAKE_CASE (`MAIN_SYSTEM_PROMPT`)

**Error Handling (from examples/tools.py:119-128):**
```python
try:
    # Operation
except SpecificException as e:
    logger.error(f"operation_failed: context={value}, error={str(e)}")
    return []  # Graceful degradation
except Exception as e:
    logger.exception(f"operation_error: context={value}, error={str(e)}")
    return []
```

**Pydantic Model Pattern (from examples/tools.py:15-24):**
```python
class SkillMetadata(BaseModel):
    """Model description."""

    field_name: str = Field(..., description="Field description")
    optional_field: str = Field(default="default", description="Description")
```

**Dataclass Pattern (from examples/dependencies.py:14-27):**
```python
@dataclass
class AgentDependencies:
    """Dependencies injected into agent context."""

    optional_dep: Optional[Type] = None
    mutable_field: Dict[str, Any] = field(default_factory=dict)
```

**Async Tool Pattern (from examples/agent.py:28-46):**
```python
@agent.tool
async def tool_name(
    ctx: RunContext[AgentDependencies],
    param: str
) -> str:
    """
    Tool description.

    Args:
        ctx: Agent runtime context with dependencies
        param: Parameter description

    Returns:
        String result formatted for LLM
    """
    # Implementation
```

**Logging Pattern:**
```python
logger = logging.getLogger(__name__)
logger.info(f"operation_completed: key={value}")
logger.error(f"operation_failed: error={str(e)}")
logger.exception(f"operation_error: error={str(e)}")  # Includes traceback
```

---

## IMPLEMENTATION PLAN

### Phase 1: Project Foundation & Skill Infrastructure

**Tasks:**
- Initialize project with uv and pyproject.toml
- Create SkillMetadata Pydantic model with YAML frontmatter fields
- Implement SkillLoader class for skill discovery and metadata parsing
- Create simplified AgentDependencies dataclass with SkillLoader
- Add unit tests for skill loader

### Phase 2: Progressive Disclosure Tools

**Tasks:**
- Implement `load_skill()` for Level 2 disclosure (full instructions)
- Implement `read_skill_file()` for Level 3 disclosure (resources)
- Implement `list_skill_files()` for resource discovery
- Add file path security validation (prevent directory traversal)
- Add unit tests for all tools

### Phase 3: Agent Integration

**Tasks:**
- Create skill_agent with dynamic system prompt
- Register all skill tools with agent
- Update CLI to use agent
- Create demo weather skill for validation
- Run full validation suite

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

---

### Task 1: CREATE pyproject.toml

- **IMPLEMENT**: Complete pyproject.toml with all dependencies for skill-based agent
- **PATTERN**: UV best practices from research
- **DEPENDENCIES**: pydantic-ai, pydantic>=2.0.0, pydantic-settings>=2.0.0, rich>=13.0.0, python-dotenv>=1.0.0, pyyaml>=6.0.0
- **DEV DEPENDENCIES**: pytest>=7.4.0, pytest-asyncio>=0.21.0, ruff>=0.1.0, mypy>=1.5.0
- **GOTCHA**: Use `requires-python = ">=3.11"` for modern async/type hint support
- **VALIDATE**: `uv sync`

```toml
[project]
name = "custom-skill-agent"
version = "0.1.0"
description = "Framework-agnostic skill system for AI agents with progressive disclosure"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pydantic-ai>=0.0.30",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "rich>=13.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0.0",
    "openai>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
asyncio_mode = "auto"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
```

---

### Task 2: CREATE .python-version

- **IMPLEMENT**: Pin Python version for uv
- **CONTENT**: `3.11`
- **VALIDATE**: `uv python pin 3.11`

---

### Task 3: UPDATE .gitignore

- **IMPLEMENT**: Add standard Python ignores plus uv.lock
- **PATTERN**: Standard Python .gitignore
- **VALIDATE**: File exists and contains required entries

Add these entries:
```
# Virtual environments
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Distribution
build/
dist/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment
.env

# UV
.uv/

# Type checking
.mypy_cache/
```

---

### Task 4: RUN uv sync to create environment

- **IMPLEMENT**: Initialize uv environment and install dependencies
- **COMMAND**: `uv sync`
- **VALIDATE**: `uv run python -c "import pydantic_ai; print('OK')"`
- **GOTCHA**: Must have valid pyproject.toml first

---

### Task 5: CREATE src/skill_loader.py

- **IMPLEMENT**: SkillMetadata Pydantic model and SkillLoader class
- **PATTERN**: Pydantic BaseModel from examples/tools.py:15-24
- **IMPORTS**: `from pathlib import Path`, `from typing import Dict, List, Optional`, `from pydantic import BaseModel, Field`, `import yaml`, `import logging`
- **GOTCHA**: YAML frontmatter is delimited by `---` at start and end
- **VALIDATE**: `uv run python -c "from src.skill_loader import SkillLoader, SkillMetadata; print('OK')"`

**SkillMetadata Model:**
```python
class SkillMetadata(BaseModel):
    """Skill metadata from YAML frontmatter."""

    name: str = Field(..., description="Unique skill identifier")
    description: str = Field(..., description="Brief description for agent discovery")
    version: str = Field(default="1.0.0", description="Skill version")
    author: str = Field(default="", description="Skill author")
    skill_path: Path = Field(..., description="Path to skill directory")
```

**SkillLoader Class:**
```python
class SkillLoader:
    """Loads and manages skills from filesystem."""

    def __init__(self, skills_dir: Path) -> None:
        self.skills_dir = skills_dir
        self.skills: Dict[str, SkillMetadata] = {}

    def discover_skills(self) -> List[SkillMetadata]:
        """Scan skills directory and extract metadata."""

    def get_skill_metadata_prompt(self) -> str:
        """Generate system prompt section with skill metadata."""

    def _parse_skill_metadata(self, skill_md: Path, skill_dir: Path) -> Optional[SkillMetadata]:
        """Extract YAML frontmatter from SKILL.md."""
```

---

### Task 6: CREATE src/dependencies.py

- **IMPLEMENT**: AgentDependencies dataclass with SkillLoader (simpler than examples, no MongoDB)
- **PATTERN**: Dataclass pattern from examples/dependencies.py:14-82
- **IMPORTS**: `from dataclasses import dataclass, field`, `from typing import Optional, Dict, Any`, `from pathlib import Path`, `from src.skill_loader import SkillLoader`, `from src.settings import load_settings`
- **GOTCHA**: No async database connections needed - much simpler than examples
- **VALIDATE**: `uv run python -c "from src.dependencies import AgentDependencies; print('OK')"`

```python
@dataclass
class AgentDependencies:
    """Dependencies injected into agent context."""

    skill_loader: Optional[SkillLoader] = None
    settings: Optional[Any] = None
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    async def initialize(self) -> None:
        """Initialize skill loader and settings."""

    # No cleanup needed - no database connections
```

---

### Task 7: CREATE tests/test_skill_loader.py

- **IMPLEMENT**: Unit tests for SkillLoader and SkillMetadata
- **PATTERN**: pytest with tmp_path fixtures
- **IMPORTS**: `import pytest`, `from pathlib import Path`, `from src.skill_loader import SkillLoader, SkillMetadata`
- **GOTCHA**: Use `tmp_path` fixture to create test skill directories
- **VALIDATE**: `uv run pytest tests/test_skill_loader.py -v`

**Test Cases:**
1. `test_skill_metadata_model_validation` - Valid SkillMetadata creation
2. `test_skill_metadata_missing_required_fields` - ValidationError for missing name/description
3. `test_skill_loader_discovers_skills` - Discover skills from directory
4. `test_skill_loader_empty_directory` - Empty skills directory returns empty list
5. `test_skill_loader_parses_frontmatter` - YAML frontmatter extraction
6. `test_skill_loader_generates_metadata_prompt` - System prompt generation
7. `test_skill_loader_handles_malformed_frontmatter` - Graceful handling of bad YAML

---

### Task 8: CREATE src/skill_tools.py

- **IMPLEMENT**: Progressive disclosure tool functions
- **PATTERN**: Async tool functions from examples/tools.py:27-128
- **IMPORTS**: `from typing import Optional`, `from pydantic_ai import RunContext`, `from src.dependencies import AgentDependencies`, `import logging`
- **GOTCHA**: Security validation - files must be within skill directory (use Path.resolve().is_relative_to())
- **VALIDATE**: `uv run python -c "from src.skill_tools import load_skill, read_skill_file, list_skill_files; print('OK')"`

**Tool Functions:**

```python
async def load_skill(
    ctx: RunContext[AgentDependencies],
    skill_name: str
) -> str:
    """Load full instructions for a skill (Level 2 progressive disclosure)."""

async def read_skill_file(
    ctx: RunContext[AgentDependencies],
    skill_name: str,
    file_path: str
) -> str:
    """Read a file from skill directory (Level 3 progressive disclosure)."""

async def list_skill_files(
    ctx: RunContext[AgentDependencies],
    skill_name: str,
    directory: str = ""
) -> str:
    """List files available in skill directory."""
```

---

### Task 9: CREATE tests/test_skill_tools.py

- **IMPLEMENT**: Unit tests for skill tools
- **PATTERN**: pytest-asyncio for async tests
- **IMPORTS**: `import pytest`, `from unittest.mock import Mock, AsyncMock`, `from src.skill_tools import load_skill, read_skill_file, list_skill_files`
- **GOTCHA**: Mock RunContext and AgentDependencies for isolated testing
- **VALIDATE**: `uv run pytest tests/test_skill_tools.py -v`

**Test Cases:**
1. `test_load_skill_returns_instructions` - Load valid skill content
2. `test_load_skill_not_found` - Error message for missing skill
3. `test_read_skill_file_valid` - Read file from skill directory
4. `test_read_skill_file_not_found` - Error for missing file
5. `test_read_skill_file_security_traversal` - Block directory traversal attacks
6. `test_list_skill_files_returns_files` - List all files in skill
7. `test_list_skill_files_empty_skill` - Handle skill with no extra files

---

### Task 10: CREATE src/agent.py

- **IMPLEMENT**: Pydantic AI agent with skill tools and dynamic system prompt
- **PATTERN**: Agent creation from examples/agent.py:15-46
- **IMPORTS**: `from pydantic_ai import Agent, RunContext`, `from pydantic import BaseModel`, `from src.providers import get_llm_model`, `from src.dependencies import AgentDependencies`, `from src.prompts import MAIN_SYSTEM_PROMPT`, `from src.skill_tools import load_skill, read_skill_file, list_skill_files`
- **GOTCHA**: Dynamic system prompt needs to call `ctx.deps.initialize()` and inject skill metadata
- **VALIDATE**: `uv run python -c "from src.agent import skill_agent; print('OK')"`

**Agent Structure:**
```python
class AgentState(BaseModel):
    """Minimal shared state for skill agent."""
    pass

skill_agent = Agent(
    get_llm_model(),
    deps_type=AgentDependencies,
    system_prompt=""  # Will be set dynamically
)

@skill_agent.system_prompt
async def get_system_prompt(ctx: RunContext[AgentDependencies]) -> str:
    """Generate system prompt with skill metadata."""

@skill_agent.tool
async def load_skill_tool(...): ...

@skill_agent.tool
async def read_skill_file_tool(...): ...

@skill_agent.tool
async def list_skill_files_tool(...): ...
```

---

### Task 11: CREATE skills/weather/SKILL.md (Demo Skill)

- **IMPLEMENT**: Simple weather skill for testing progressive disclosure
- **PATTERN**: SKILL.md template from PRD
- **LOCATION**: `skills/weather/SKILL.md`
- **GOTCHA**: Frontmatter must start at line 1 with `---`
- **VALIDATE**: `uv run python -c "from src.skill_loader import SkillLoader; from pathlib import Path; sl = SkillLoader(Path('skills')); sl.discover_skills(); print(sl.skills)"`

```markdown
---
name: weather
description: Get weather information for locations. Use when user asks about weather, temperature, or forecasts.
version: 1.0.0
author: Workshop Team
---

# Weather Skill

Provides weather information for locations around the world.

## When to Use

- User asks about current weather
- User asks about temperature
- User asks about weather forecasts
- User mentions weather-related queries

## Available Operations

1. **Get Current Weather**: Retrieve current conditions for a location
2. **Format Weather Data**: Present weather in a user-friendly format

## Instructions

When a user asks about weather:

1. Identify the location from the user's query
2. Provide helpful weather information based on the location
3. If no specific location is mentioned, ask the user for one

## Resources

- `references/api_reference.md` - API documentation (if available)

## Examples

### Example 1: Simple Query
User asks: "What's the weather in New York?"
Response: Provide current weather conditions for New York City.

### Example 2: Temperature Query
User asks: "How hot is it in Miami?"
Response: Provide temperature information for Miami.

## Notes

This is a demonstration skill showing the progressive disclosure pattern.
For a full implementation, integrate with a weather API like OpenWeatherMap.
```

---

### Task 12: CREATE skills/weather/references/api_reference.md

- **IMPLEMENT**: Reference documentation for Level 3 disclosure demo
- **LOCATION**: `skills/weather/references/api_reference.md`
- **VALIDATE**: File exists at path

```markdown
# Weather API Reference

This document provides API documentation for weather data retrieval.

## Overview

The weather skill can integrate with weather APIs to provide real-time data.

## Recommended APIs

### OpenWeatherMap API

- **Endpoint**: `https://api.openweathermap.org/data/2.5/weather`
- **Parameters**:
  - `q`: City name (e.g., "London", "New York")
  - `appid`: API key
  - `units`: Temperature units ("metric" or "imperial")

### Example Response

```json
{
  "main": {
    "temp": 72.5,
    "humidity": 65
  },
  "weather": [
    {
      "main": "Clear",
      "description": "clear sky"
    }
  ]
}
```

## Error Handling

- **404**: City not found
- **401**: Invalid API key
- **429**: Rate limit exceeded
```

---

### Task 13: UPDATE src/cli.py - Uncomment Agent Integration

- **IMPLEMENT**: Enable agent import and main conversation loop
- **PATTERN**: Existing commented code in cli.py
- **CHANGES**:
  1. Uncomment agent import (line 16-17 area)
  2. Remove placeholder message (line 185-186)
  3. Uncomment main conversation loop (lines 188-250)
- **GOTCHA**: The agent import path is `from src.agent import skill_agent`
- **VALIDATE**: `uv run python -m src.cli` (will need .env)

---

### Task 14: CREATE tests/__init__.py

- **IMPLEMENT**: Empty init file for tests package
- **VALIDATE**: File exists

---

### Task 15: RUN Full Test Suite

- **IMPLEMENT**: Execute all tests
- **COMMAND**: `uv run pytest tests/ -v`
- **VALIDATE**: All tests pass

---

### Task 16: NOTIFY User to Create .env

**STOP HERE AND ASK USER TO FILL IN .env**

Before validation can proceed, the user needs to:
1. Copy `.env.example` to `.env`
2. Fill in `LLM_API_KEY` with a valid API key (OpenRouter recommended)
3. Optionally adjust `LLM_MODEL` and `LLM_BASE_URL`

**Required .env content:**
```bash
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-v1-YOUR-KEY-HERE
LLM_MODEL=anthropic/claude-sonnet-4.5
LLM_BASE_URL=https://openrouter.ai/api/v1
SKILLS_DIR=skills
APP_ENV=development
LOG_LEVEL=INFO
```

---

### Task 17: VALIDATE Manual - Run CLI Agent

- **IMPLEMENT**: Manual validation of complete agent
- **COMMAND**: `uv run python -m src.cli`
- **TEST STEPS**:
  1. Agent starts and shows welcome message
  2. Agent lists available skills (weather should appear)
  3. Ask: "What's the weather in New York?"
  4. Agent should call `load_skill("weather")` tool
  5. Agent provides weather-related response
  6. Ask: "Can you show me the API reference?"
  7. Agent should call `read_skill_file("weather", "references/api_reference.md")`
  8. Type `exit` to quit cleanly
- **VALIDATE**: All interactions work as expected

---

## TESTING STRATEGY

### Unit Tests

**test_skill_loader.py** - SkillLoader functionality:
- Model validation (SkillMetadata)
- Skill discovery from filesystem
- YAML frontmatter parsing
- System prompt generation
- Error handling for malformed files

**test_skill_tools.py** - Progressive disclosure tools:
- load_skill with valid/invalid skills
- read_skill_file with valid paths
- read_skill_file security (directory traversal prevention)
- list_skill_files output format
- Error message formatting

### Integration Tests

Manual validation via CLI:
- Full conversation flow with skill loading
- Level 2 disclosure (load_skill)
- Level 3 disclosure (read_skill_file)
- Message history maintenance

### Edge Cases

1. Empty skills directory - should work with empty skill list
2. Malformed SKILL.md - should skip and log warning
3. Missing frontmatter fields - should use defaults or skip
4. Directory traversal attempt - should return error message
5. Non-existent skill - should return helpful error
6. Non-existent file in skill - should return helpful error

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Level 1: Environment & Dependencies

```bash
# Verify uv environment
uv sync

# Verify Python version
uv run python --version  # Should be 3.11+

# Verify core imports
uv run python -c "import pydantic_ai; import pydantic; import yaml; import rich; print('All imports OK')"
```

### Level 2: Module Imports

```bash
# Test all new modules import correctly
uv run python -c "from src.skill_loader import SkillLoader, SkillMetadata; print('skill_loader OK')"
uv run python -c "from src.dependencies import AgentDependencies; print('dependencies OK')"
uv run python -c "from src.skill_tools import load_skill, read_skill_file, list_skill_files; print('skill_tools OK')"
uv run python -c "from src.agent import skill_agent; print('agent OK')"
```

### Level 3: Unit Tests

```bash
# Run all tests with verbose output
uv run pytest tests/ -v

# Run with coverage (optional)
uv run pytest tests/ -v --cov=src
```

### Level 4: Skill Discovery Validation

```bash
# Verify skill discovery works
uv run python -c "
from pathlib import Path
from src.skill_loader import SkillLoader

loader = SkillLoader(Path('skills'))
skills = loader.discover_skills()
print(f'Discovered {len(skills)} skills')
for skill in skills:
    print(f'  - {skill.name}: {skill.description}')

prompt = loader.get_skill_metadata_prompt()
print(f'\\nMetadata prompt ({len(prompt)} chars):\\n{prompt[:500]}...')
"
```

### Level 5: Manual Validation (Requires .env)

```bash
# Run CLI and test interaction
uv run python -m src.cli
```

**Manual Test Script:**
1. Verify welcome message appears
2. Type: "hi" - Agent should respond conversationally
3. Type: "What skills do you have?" - Agent should list weather skill
4. Type: "What's the weather in Tokyo?" - Agent should load weather skill
5. Type: "Show me the API reference" - Agent should load reference file
6. Type: "exit" - Clean exit

---

## ACCEPTANCE CRITERIA

- [ ] uv sync completes without errors
- [ ] All module imports work (`src.skill_loader`, `src.dependencies`, `src.skill_tools`, `src.agent`)
- [ ] SkillLoader discovers weather skill from skills/ directory
- [ ] SkillMetadata validates YAML frontmatter correctly
- [ ] load_skill returns full SKILL.md body (without frontmatter)
- [ ] read_skill_file loads referenced files from skill directory
- [ ] read_skill_file blocks directory traversal (../ paths)
- [ ] list_skill_files shows available resources
- [ ] Agent system prompt includes skill metadata dynamically
- [ ] Agent can call skill tools during conversation
- [ ] CLI runs with streaming responses
- [ ] All unit tests pass (`uv run pytest tests/ -v`)
- [ ] Manual CLI validation passes all test steps

---

## COMPLETION CHECKLIST

- [ ] pyproject.toml created with all dependencies
- [ ] .python-version set to 3.11
- [ ] .gitignore updated with Python/uv entries
- [ ] uv sync completed successfully
- [ ] src/skill_loader.py implemented with SkillLoader and SkillMetadata
- [ ] src/dependencies.py implemented with AgentDependencies
- [ ] src/skill_tools.py implemented with all three tools
- [ ] src/agent.py implemented with skill_agent and tools
- [ ] tests/test_skill_loader.py created with all test cases
- [ ] tests/test_skill_tools.py created with all test cases
- [ ] tests/__init__.py created
- [ ] skills/weather/SKILL.md created
- [ ] skills/weather/references/api_reference.md created
- [ ] src/cli.py updated with agent integration
- [ ] All unit tests pass
- [ ] Manual validation completed
- [ ] User notified to fill .env before final validation

---

## NOTES

### Design Decisions

1. **No StateDeps wrapper**: Unlike examples/agent.py which uses `StateDeps[RAGState]`, we use `AgentDependencies` directly as deps_type since we don't need AGUI state management. This simplifies the pattern.

2. **Simplified AgentDependencies**: No MongoDB or OpenAI embedding client needed - just SkillLoader and Settings. This is intentionally simpler than the examples reference.

3. **YAML Frontmatter Parsing**: Using PyYAML directly rather than a frontmatter library to minimize dependencies. The parsing logic handles the `---` delimiters manually.

4. **Security First**: Path traversal prevention is critical in read_skill_file. Using `Path.resolve().is_relative_to()` to validate all file paths are within the skill directory.

5. **Graceful Degradation**: If skill discovery fails or a skill is malformed, log a warning and continue rather than crashing. The agent should work with available skills.

### Key Files Reference

| File | Purpose | Lines of Interest |
|------|---------|-------------------|
| examples/dependencies.py | AgentDependencies pattern | 14-82 |
| examples/agent.py | Agent + tool registration | 21-46 |
| examples/tools.py | Async tool functions | 27-128 |
| examples/cli.py | Streaming + Rich UI | 61-157 |
| .claude/PRD.md | Complete build order | 603-780 |

### Estimated Confidence Score: 9/10

High confidence due to:
- Clear patterns from examples/ reference code
- Well-documented PRD with complete specifications
- Simpler implementation than reference (no database)
- Comprehensive validation commands at each step

Risk factors:
- Pydantic AI version compatibility (use >=0.0.30)
- Agent.iter() API may vary slightly between versions
- User environment setup (API keys, Python version)
