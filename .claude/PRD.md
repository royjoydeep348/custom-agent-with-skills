# Product Requirements Document: Custom Skill-Based Pydantic AI Agent

## Executive Summary

This project delivers a framework-agnostic skill system for AI agents, extracting the progressive disclosure pattern from Claude Skills and implementing it as a native feature in Pydantic AI. The system enables developers to build AI agents with modular, reusable skills that load instructions and resources on-demand, eliminating context window constraints while maintaining type safety and testability.

Unlike Claude Skills which are locked to the Claude ecosystem (Claude Desktop, Claude Code), this implementation makes advanced skill capabilities available to ANY AI agent framework. The system demonstrates how to take successful patterns from proprietary systems and apply them to open frameworks, empowering developers to escape vendor lock-in while maintaining professional-grade capabilities.

The MVP will include a complete skill loader, progressive disclosure tools, a skill-aware Pydantic AI agent, and two demonstration skills (Weather and Code Review) that showcase different complexity levels. This will be delivered as a workshop demonstrating the architecture, implementation, and practical applications.

## Mission

**Enable developers to build production-grade AI agents with modular, reusable skills that scale beyond context window limitations.**

### Core Principles

1. **Framework Agnostic**: Skills work with any AI framework, not just Claude
2. **Progressive Disclosure**: Load information in stages as needed, never consume unnecessary context
3. **Type Safety First**: Full Pydantic validation throughout the system
4. **KISS Over Clever**: Simple, readable solutions that developers can understand and extend
5. **Reusability**: Skills are portable across different agents and projects

## Target Users

### Primary Persona: Python AI Developer

**Technical Level**: Intermediate to Advanced
- Familiar with Python, async/await, type hints
- Experience with LLM APIs and AI agent frameworks
- Understanding of dependency injection patterns
- Interest in building production-grade AI applications

**Key Needs**:
- Modular way to extend AI agent capabilities
- Escape vendor lock-in from proprietary systems
- Type-safe, testable agent architecture
- Ability to include large reference materials without context bloat
- Reusable skills across multiple projects

**Pain Points**:
- Context window limitations when including documentation
- Difficulty managing complex agent prompts
- Lack of modularity in agent systems
- Vendor lock-in with Claude Desktop/Code skills
- Hard to test and version control agent capabilities

### Secondary Persona: Workshop Participant

**Technical Level**: Intermediate Python developer
- Basic understanding of AI/LLMs
- Interest in learning agent development patterns
- May be new to Pydantic AI framework
- Wants practical, working examples

## MVP Scope

### In Scope

#### ✅ Core Functionality
- Skill discovery from filesystem directory structure
- YAML frontmatter parsing for skill metadata
- Progressive disclosure implementation (3 levels)
- Skill metadata injection into system prompts
- On-demand loading of skill instructions
- On-demand loading of skill resources (scripts, references, assets)

#### ✅ Technical Implementation
- SkillLoader class for discovery and management
- Skill tools: `load_skill`, `read_skill_file`, `list_skill_files`
- Enhanced AgentDependencies with skill context
- Dynamic system prompt generation with skill metadata
- Pydantic AI agent with skill awareness
- Type-safe skill metadata models

#### ✅ Demo Skills
- Weather skill (simple API integration)
- Code Review skill (advanced with extensive references)

#### ✅ Integration
- Interactive CLI with Rich formatting
- Complete working example agent
- Integration with Pydantic AI dependency injection
- Settings management with Pydantic Settings

#### ✅ Workshop Materials
- Complete implementation with detailed comments
- Working examples demonstrating each concept
- Clear documentation of progressive disclosure pattern

### Out of Scope

#### ❌ Advanced Features (Post-MVP)
- Skill versioning and updates
- Skill marketplace or registry
- Skill dependencies and composition
- Permission/security model for skills
- Remote skill loading from URLs
- Skill performance metrics and analytics

#### ❌ Production Hardening
- Comprehensive error recovery
- Rate limiting for skill operations
- Caching layer for skill content
- Skill validation and linting tools
- Production deployment guides

#### ❌ Additional Integrations
- Database integration for skill usage tracking
- Multi-agent skill sharing
- Web UI for skill management
- IDE plugins for skill development

#### ❌ Extended Demo Skills
- SQL Query Builder skill
- File Analysis skill
- Calculator skill
- Additional domain-specific skills

## User Stories

### Primary User Stories

1. **As a Python developer**, I want to create modular skills for my AI agent, so that I can organize complex functionality into reusable components.
   - *Example*: Create a "weather" skill once, use it in multiple agent projects

2. **As an AI agent developer**, I want my agent to discover and use skills automatically, so that I don't have to manually manage which capabilities are available.
   - *Example*: Agent sees skill metadata in system prompt and knows when to invoke weather skill

3. **As a developer working with large reference docs**, I want to include comprehensive documentation without consuming context upfront, so that my agent can access details only when needed.
   - *Example*: Code review skill has 50KB of best practices docs, but only loads specific sections when reviewing code

4. **As a workshop participant**, I want to see working examples of progressive disclosure, so that I understand how to implement it in my own projects.
   - *Example*: Run demo agent, see it load skill metadata, then full instructions, then specific reference files

5. **As a developer concerned about vendor lock-in**, I want skills that work with any LLM framework, so that I'm not tied to Claude's ecosystem.
   - *Example*: Same skill works with Pydantic AI, LangChain, or custom agent implementations

6. **As a type-safety advocate**, I want full Pydantic validation for skill structures, so that I catch errors at development time rather than runtime.
   - *Example*: Invalid YAML frontmatter raises validation error with clear message

7. **As an agent builder**, I want skills to be file-based and version-controlled, so that I can track changes and collaborate with teams.
   - *Example*: Skills live in Git repo, changes are reviewed through PRs

8. **As a developer**, I want clear examples of different skill complexity levels, so that I know how to structure simple vs. complex skills.
   - *Example*: Weather skill shows simple pattern, Code Review skill shows advanced pattern

### Technical User Stories

9. **As a Pydantic AI user**, I want skills to integrate seamlessly with dependency injection, so that I can access skill functionality in tools and system prompts.
   - *Example*: `RunContext[AgentDependencies]` provides access to skill loader

10. **As a developer debugging agent behavior**, I want to see which skills are loaded and when, so that I can understand the progressive disclosure flow.
    - *Example*: CLI shows "Loading weather skill..." when agent invokes it

## Core Architecture & Patterns

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Pydantic AI Agent                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          System Prompt (Dynamic)                      │  │
│  │  • Base instructions                                  │  │
│  │  • Skill metadata (Level 1: ~100 tokens/skill)       │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          Agent Tools                                  │  │
│  │  • load_skill(name) → Level 2: Full instructions     │  │
│  │  • read_skill_file(name, path) → Level 3: Resources  │  │
│  │  • list_skill_files(name) → Resource discovery       │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          Dependencies (Injected via RunContext)       │  │
│  │  • SkillLoader                                        │  │
│  │  • Settings                                           │  │
│  │  • Session context                                    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Skill Loader                              │
│  • Scans skills/ directory                                   │
│  • Parses YAML frontmatter                                   │
│  • Maintains skill metadata registry                         │
│  • Generates system prompt section                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Skills Directory                          │
│  skills/                                                     │
│  ├── weather/                                                │
│  │   ├── SKILL.md (frontmatter + instructions)             │
│  │   ├── scripts/fetch_weather.py                          │
│  │   └── references/api_reference.md                       │
│  └── code_review/                                           │
│      ├── SKILL.md                                           │
│      ├── scripts/lint_code.py                              │
│      └── references/                                        │
│          ├── best_practices.md                             │
│          ├── security_checklist.md                         │
│          └── common_antipatterns.md                        │
└─────────────────────────────────────────────────────────────┘
```

### Progressive Disclosure Flow

**Level 1 - Discovery (Always Loaded)**
```
System Prompt contains:
---
name: weather
description: Get weather information for locations. Use when user asks about weather.
---
name: code_review
description: Review code for quality, security, and best practices.
---
```

**Level 2 - Full Instructions (Loaded on Invocation)**
```python
Agent decides: "User asked about weather, I need the weather skill"
→ Calls: load_skill("weather")
→ Returns: Full SKILL.md body (without frontmatter)
→ Agent now has complete instructions for using weather skill
```

**Level 3 - Resources (Loaded on Demand)**
```python
Agent reading weather instructions: "See references/api_reference.md for API docs"
→ Calls: read_skill_file("weather", "references/api_reference.md")
→ Returns: Complete API reference documentation
→ Agent uses docs to make correct API calls
```

### Directory Structure

```
custom-skill-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py              # Main agent with skill tools
│   ├── skill_loader.py       # Skill discovery and metadata
│   ├── skill_tools.py        # Progressive disclosure tools
│   ├── dependencies.py       # AgentDependencies with SkillLoader
│   ├── providers.py          # LLM provider configuration
│   ├── settings.py           # Pydantic settings
│   ├── prompts.py            # Base system prompts
│   └── cli.py                # Interactive CLI
├── skills/
│   ├── weather/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── fetch_weather.py
│   │   └── references/
│   │       └── api_reference.md
│   └── code_review/
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── lint_code.py
│       │   └── check_patterns.py
│       └── references/
│           ├── best_practices.md
│           ├── security_checklist.md
│           └── common_antipatterns.md
├── examples/
│   └── (existing MongoDB RAG agent)
├── tests/
│   ├── test_skill_loader.py
│   ├── test_skill_tools.py
│   └── test_agent.py
├── .env.example
├── pyproject.toml
└── README.md
```

### Key Design Patterns

**1. Dependency Injection Pattern**
- `AgentDependencies` dataclass contains all injectable services
- `RunContext[AgentDependencies]` provides type-safe access in tools
- Dynamic system prompts use deps for runtime information

**2. Progressive Disclosure Pattern**
- Level 1: Metadata in system prompt (minimal tokens)
- Level 2: Full instructions loaded via tool call
- Level 3: Resources loaded via tool call only when referenced

**3. Frontmatter + Body Pattern**
```markdown
---
name: skill-name
description: Brief description for discovery
---

# Full Instructions

Detailed instructions here...
```

**4. Type-Safe Metadata Pattern**
```python
class SkillMetadata(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    skill_path: Path
```

## Skills Specification

### Weather Skill

**Purpose**: Demonstrate simple skill structure with API integration

**Directory Structure**:
```
skills/weather/
├── SKILL.md
├── scripts/
│   └── fetch_weather.py
└── references/
    └── api_reference.md
```

**SKILL.md Frontmatter**:
```yaml
---
name: weather
description: Get weather information for locations. Use when user asks about weather, temperature, or forecasts.
version: 1.0.0
author: Workshop Team
---
```

**Key Features**:
- Current weather retrieval
- Simple API integration example
- Demonstrates Level 2 progressive disclosure (full instructions)
- Shows how to reference scripts in skill instructions

**Operations**:
1. Get current weather for a location
2. Parse and format weather data
3. Handle API errors gracefully

### Code Review Skill

**Purpose**: Demonstrate advanced skill with extensive reference materials

**Directory Structure**:
```
skills/code_review/
├── SKILL.md
├── scripts/
│   ├── lint_code.py
│   └── check_patterns.py
└── references/
    ├── best_practices.md        (10KB+)
    ├── security_checklist.md    (15KB+)
    └── common_antipatterns.md   (20KB+)
```

**SKILL.md Frontmatter**:
```yaml
---
name: code_review
description: Review code for quality, security, and best practices. Use when analyzing code, suggesting improvements, or conducting code reviews.
version: 1.0.0
author: Workshop Team
---
```

**Key Features**:
- Multi-step review workflow
- Extensive reference documentation (45KB+ total)
- Demonstrates Level 3 progressive disclosure (resource loading)
- Shows complex skill organization
- Multiple reference files for different aspects

**Operations**:
1. Analyze code structure
2. Check against best practices
3. Identify security issues
4. Detect common antipatterns
5. Generate review report

**Progressive Disclosure Example**:
- Level 1: Agent sees "code_review" in available skills
- Level 2: User asks for code review → agent loads SKILL.md instructions
- Level 3: Instructions say "Check references/security_checklist.md" → agent loads specific doc

## Technology Stack

### Core Framework
- **Pydantic AI** (latest): Agent framework with type safety
- **Pydantic** v2: Data validation and settings management
- **Python** 3.11+: Modern async/await, type hints

### LLM Integration
- **OpenAI SDK**: For OpenAI-compatible providers
- **Anthropic SDK**: Optional for direct Claude API access
- Support for: OpenRouter, Ollama, Gemini, etc.

### CLI & UI
- **Rich** (latest): Beautiful terminal formatting
- **asyncio**: Async runtime for agent operations

### Development Tools
- **UV**: Fast Python package manager
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support

### Optional Dependencies
- **PyYAML**: YAML frontmatter parsing
- **python-dotenv**: Environment variable management

### Third-Party Integrations (Demo Skills)
- **OpenWeatherMap API**: Weather skill demo (free tier)
- No authentication required for MVP

## Security & Configuration

### Authentication & Authorization

**MVP Scope**:
- ✅ API key management for LLM providers
- ✅ Environment variable configuration for sensitive data
- ✅ Basic file path validation (prevent directory traversal)

**Out of Scope**:
- ❌ User authentication
- ❌ Role-based access to skills
- ❌ Skill execution permissions/sandboxing
- ❌ Audit logging

### Configuration Management

**Environment Variables** (.env):
```bash
# LLM Provider
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-v1-...
LLM_MODEL=anthropic/claude-sonnet-4.5
LLM_BASE_URL=https://openrouter.ai/api/v1

# Weather Skill (optional)
OPENWEATHER_API_KEY=your-key-here

# Application
APP_ENV=development
LOG_LEVEL=INFO
SKILLS_DIR=skills
```

**Pydantic Settings**:
```python
class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    llm_provider: str = "openrouter"
    llm_api_key: str = Field(..., description="LLM API key")
    llm_model: str = "anthropic/claude-sonnet-4.5"
    skills_dir: Path = Field(default=Path("skills"))
```

### Security Considerations

**In Scope**:
- ✅ File path validation to prevent directory traversal
- ✅ Skills must be within designated skills directory
- ✅ API keys stored in environment variables only
- ✅ No arbitrary code execution in MVP

**Out of Scope** (Future):
- ❌ Sandboxed skill execution
- ❌ Skill code signing/verification
- ❌ Rate limiting per skill
- ❌ Encrypted skill storage

### File Path Security

```python
# Security check in read_skill_file
if not target_file.resolve().is_relative_to(skill.skill_path.resolve()):
    return "Error: Access denied - file must be within skill directory"
```

## Success Criteria

### MVP Success Definition

**The MVP is successful when a developer can**:
1. Clone the repository and run the skill-based agent
2. See the agent discover and use existing skills (weather, code_review)
3. Create a new skill by following the pattern
4. Understand progressive disclosure through working examples
5. Recognize how this pattern applies to their own agent projects

### Functional Requirements

#### ✅ Skill Discovery
- [ ] Agent discovers all skills in skills/ directory
- [ ] Skill metadata appears in system prompt
- [ ] Agent can list available skills to user

#### ✅ Progressive Disclosure
- [ ] Level 1: Metadata loaded on agent start (~100 tokens/skill)
- [ ] Level 2: Full instructions loaded via load_skill() tool
- [ ] Level 3: Resources loaded via read_skill_file() tool
- [ ] Agent only loads content when actually needed

#### ✅ Skill Tools
- [ ] load_skill() returns full SKILL.md content
- [ ] read_skill_file() loads specific resource files
- [ ] list_skill_files() shows available resources
- [ ] All tools have proper error handling

#### ✅ Type Safety
- [ ] SkillMetadata validates frontmatter structure
- [ ] All tools use RunContext with typed dependencies
- [ ] Pydantic Settings validates configuration
- [ ] IDE provides autocomplete for skill operations

#### ✅ Demo Skills
- [ ] Weather skill successfully fetches weather data
- [ ] Code review skill loads and uses reference materials
- [ ] Skills demonstrate different complexity levels
- [ ] Skills show progressive disclosure in action

#### ✅ Integration
- [ ] CLI runs and accepts user input
- [ ] Agent responds using skills when appropriate
- [ ] Rich formatting shows skill operations clearly
- [ ] Settings load from .env file correctly

### Quality Indicators

**Code Quality**:
- Type hints on all functions and classes
- Google-style docstrings throughout
- Clear separation of concerns
- No circular dependencies

**User Experience**:
- CLI provides clear feedback during skill loading
- Error messages are helpful and actionable
- Skills work on first try with example .env
- README provides clear setup instructions

**Educational Value** (Workshop Context):
- Code is well-commented explaining the "why"
- Progressive disclosure pattern is clearly demonstrated
- Examples show progression from simple to complex
- Attendees can extend with their own skills

## Complete Build Order

This section lists every file and component that needs to be built, in order of implementation. Use this as a comprehensive checklist.

### Foundation (Already Complete ✅)

1. **`src/__init__.py`** ✅
   - Package initialization
   - Version info

2. **`src/providers.py`** ✅
   - Copied from `examples/providers.py`
   - LLM provider configuration (OpenRouter, OpenAI, etc.)
   - No changes needed

3. **`src/settings.py`** ✅
   - Adapted from `examples/settings.py`
   - Pydantic Settings with skills_dir
   - Removed MongoDB fields

4. **`src/prompts.py`** ✅
   - Adapted from `examples/prompts.py`
   - Skill-aware system prompts
   - Progressive disclosure instructions

5. **`src/cli.py`** ✅
   - Adapted from `examples/cli.py`
   - Rich-based conversational CLI
   - Placeholder for agent integration

6. **`.env.example`** ✅
   - Environment variable template
   - LLM configuration
   - Skills directory setting

7. **`CLAUDE.md`** ✅
   - Development instructions
   - Progressive disclosure patterns
   - Implementation guidelines

### Phase 1: Skill Infrastructure (Next Priority)

8. **`src/skill_loader.py`** ⏳
   - `SkillMetadata(BaseModel)` - Pydantic model for skill metadata
     - Fields: name, description, version, author, skill_path
   - `SkillLoader` class
     - `__init__(skills_dir: Path)`
     - `discover_skills() -> List[SkillMetadata]`
     - `get_skill_metadata_prompt() -> str`
     - `_parse_skill_metadata(skill_md: Path, skill_dir: Path) -> SkillMetadata`
   - YAML frontmatter parsing
   - Error handling for malformed SKILL.md files

9. **`src/dependencies.py`** ⏳
   - Adapt from `examples/dependencies.py` (much simpler, no MongoDB)
   - `AgentDependencies` dataclass
     - `skill_loader: Optional[SkillLoader]`
     - `settings: Optional[Settings]`
     - `session_id: Optional[str]`
     - `user_preferences: Dict[str, Any]`
   - `async def initialize()` - Initialize skill loader
   - No database connection needed

10. **`tests/test_skill_loader.py`** ⏳
    - Test skill discovery
    - Test YAML frontmatter parsing
    - Test metadata validation
    - Test system prompt generation
    - Use tmp_path fixtures for test skills

### Phase 2: Progressive Disclosure Tools

11. **`src/skill_tools.py`** ⏳
    - `async def load_skill(ctx, skill_name) -> str`
      - Level 2 progressive disclosure
      - Load full SKILL.md body (minus frontmatter)
      - Error handling for missing skills
    - `async def read_skill_file(ctx, skill_name, file_path) -> str`
      - Level 3 progressive disclosure
      - Load specific resource files
      - Security: validate file path within skill directory
      - Error handling for missing files
    - `async def list_skill_files(ctx, skill_name, directory) -> str`
      - Resource discovery
      - List available files in skill directory
      - Recursive file listing
    - Full type hints and docstrings

12. **`tests/test_skill_tools.py`** ⏳
    - Test load_skill with valid/invalid skill names
    - Test read_skill_file with various paths
    - Test security validation (directory traversal prevention)
    - Test list_skill_files output format
    - Mock AgentDependencies and SkillLoader

### Phase 3: Agent Integration

13. **`src/agent.py`** ⏳
    - `AgentState(BaseModel)` - Minimal shared state
    - Create agent: `skill_agent = Agent(...)`
    - `@skill_agent.system_prompt` decorator
      - Dynamic prompt with skill metadata
      - Call `ctx.deps.initialize()`
      - Inject skill metadata into MAIN_SYSTEM_PROMPT
    - Tool registration:
      - `@skill_agent.tool async def load_skill_tool(...)`
      - `@skill_agent.tool async def read_skill_file_tool(...)`
      - `@skill_agent.tool async def list_skill_files_tool(...)`
    - Import from skill_tools, dependencies, providers, prompts

14. **Update `src/cli.py`** ⏳
    - Uncomment agent import
    - Uncomment main conversation loop
    - Test with agent integration

15. **`tests/test_agent.py`** ⏳
    - Test agent initialization
    - Test system prompt includes skill metadata
    - Test tool registration
    - Test agent can call skill tools
    - Integration test with mock skills

### Phase 4: Demo Skills

16. **`skills/weather/SKILL.md`** ⏳
    - YAML frontmatter (name, description, version)
    - Instructions for getting weather
    - When to use section
    - Examples of weather queries
    - Reference to api_reference.md

17. **`skills/weather/scripts/fetch_weather.py`** ⏳
    - Python script for weather API calls
    - OpenWeatherMap API integration
    - Error handling and formatting
    - Can be called from skill instructions

18. **`skills/weather/references/api_reference.md`** ⏳
    - OpenWeatherMap API documentation
    - API endpoints and parameters
    - Response format examples
    - Error codes and handling

19. **`skills/code_review/SKILL.md`** ⏳
    - YAML frontmatter
    - Multi-step code review instructions
    - References to multiple documentation files
    - Examples of code review queries
    - Workflow: analyze → check best practices → check security → report

20. **`skills/code_review/scripts/lint_code.py`** ⏳
    - Python script for basic linting
    - Pattern checking helper
    - Can be referenced in instructions

21. **`skills/code_review/scripts/check_patterns.py`** ⏳
    - Check for common antipatterns
    - Pattern detection utilities

22. **`skills/code_review/references/best_practices.md`** ⏳
    - Comprehensive best practices guide (10KB+)
    - Language-agnostic principles
    - Code examples

23. **`skills/code_review/references/security_checklist.md`** ⏳
    - Security review checklist (15KB+)
    - Common vulnerabilities
    - OWASP Top 10 considerations

24. **`skills/code_review/references/common_antipatterns.md`** ⏳
    - Common code antipatterns (20KB+)
    - What to look for
    - How to fix them

### Phase 5: Testing & Documentation

25. **`tests/test_integration.py`** ⏳
    - End-to-end test: user query → skill loading → response
    - Test weather skill workflow
    - Test code review skill workflow
    - Test progressive disclosure in action

26. **`tests/fixtures/`** ⏳
    - Dummy skills for testing
    - Mock SKILL.md files
    - Test reference files

27. **`README.md`** ⏳
    - Project overview
    - Setup instructions
    - Quick start guide
    - Example usage
    - Workshop information
    - Link to PRD and CLAUDE.md

28. **`requirements.txt`** or **`pyproject.toml`** ⏳
    - All dependencies listed:
      - pydantic-ai
      - pydantic
      - pydantic-settings
      - rich
      - python-dotenv
      - pyyaml
      - pytest (dev)
      - pytest-asyncio (dev)

### Optional Enhancements (Post-MVP)

29. **`tests/test_cli.py`** (Optional)
    - Test CLI special commands
    - Test streaming display
    - Mock agent interactions

30. **`.gitignore`** (If not exists)
    - .env
    - .venv/
    - __pycache__/
    - *.pyc
    - .pytest_cache/

31. **`LICENSE`** (Optional)
    - MIT or Apache 2.0

32. **GitHub Actions CI/CD** (Optional)
    - `.github/workflows/test.yml`
    - Run tests on push
    - Lint checks

---

## Implementation Phases

### Phase 1: Skill Infrastructure (Days 1-2)

**Goal**: Build the core skill loading and discovery system

**Deliverables**:
- ✅ SkillLoader class with discovery logic
- ✅ SkillMetadata Pydantic model
- ✅ YAML frontmatter parsing
- ✅ System prompt metadata generation
- ✅ Unit tests for skill loader
- ✅ Basic AgentDependencies with SkillLoader

**Validation**:
- Create dummy skill directory, verify discovery
- Check metadata extraction is accurate
- Confirm system prompt includes skill descriptions

**Estimated Effort**: 6-8 hours

### Phase 2: Progressive Disclosure Tools (Days 2-3)

**Goal**: Implement the three skill tools for progressive disclosure

**Deliverables**:
- ✅ load_skill() tool (Level 2 disclosure)
- ✅ read_skill_file() tool (Level 3 disclosure)
- ✅ list_skill_files() tool (resource discovery)
- ✅ File path security validation
- ✅ Error handling for missing skills/files
- ✅ Integration with RunContext[AgentDependencies]
- ✅ Unit tests for all tools

**Validation**:
- Tools correctly load skill content
- Security validation prevents directory traversal
- Error messages are clear and helpful

**Estimated Effort**: 6-8 hours

### Phase 3: Agent Integration (Day 3)

**Goal**: Build Pydantic AI agent with skill awareness

**Deliverables**:
- ✅ Agent definition with dynamic system prompt
- ✅ @agent.system_prompt decorator implementation
- ✅ Tool registration (@agent.tool decorators)
- ✅ Providers configuration for LLM
- ✅ Settings with Pydantic Settings
- ✅ Base system prompt with skill instructions
- ✅ Integration tests with agent

**Validation**:
- Agent system prompt contains skill metadata
- Agent can invoke skill tools successfully
- Dynamic prompt updates when skills change

**Estimated Effort**: 4-6 hours

### Phase 4: Demo Skills & CLI (Days 4-5)

**Goal**: Create working demo skills and interactive CLI

**Deliverables**:
- ✅ Weather skill (complete with SKILL.md, scripts, references)
- ✅ Code review skill (with extensive reference materials)
- ✅ Interactive CLI with Rich formatting
- ✅ Streaming response display
- ✅ Skill operation visibility in CLI
- ✅ README with setup instructions
- ✅ .env.example file
- ✅ End-to-end tests

**Validation**:
- Run CLI, ask weather question, agent uses weather skill
- Ask for code review, agent loads and uses references
- CLI shows progressive disclosure happening
- Workshop participant can follow README to get running

**Estimated Effort**: 8-10 hours

### Total Timeline

**Total Estimated Effort**: 24-32 hours
**Recommended Schedule**: 5 days with buffer for polish and documentation

## Future Considerations

### Post-MVP Enhancements

**Skill Management**:
- Skill versioning (semantic versioning in frontmatter)
- Skill update notifications
- Skill dependency declarations
- Skill composition (skills using other skills)

**Performance & Optimization**:
- Caching layer for frequently accessed skill content
- Lazy loading optimization
- Parallel skill discovery
- Skill usage analytics

**Developer Experience**:
- CLI tool for scaffolding new skills
- Skill validation and linting
- IDE extension for skill development
- Skill testing framework

**Advanced Features**:
- Remote skill loading from URLs/Git repos
- Skill marketplace/registry
- Encrypted skills for proprietary knowledge
- Skill execution sandboxing

### Integration Opportunities

**Multi-Agent Systems**:
- Skill sharing between agents
- Agent-specific skill permissions
- Skill handoff protocols

**Framework Extensions**:
- LangChain skill adapter
- LlamaIndex skill integration
- Haystack skill connector

**Production Deployment**:
- Skill hot-reloading in production
- Skill A/B testing framework
- Skill performance monitoring
- Skill rollback mechanisms

### Advanced Demo Skills

**SQL Query Builder**:
- Complete SQL reference documentation
- Query optimization guides
- Database-specific patterns

**File Analysis**:
- Multi-format support (CSV, JSON, XML, etc.)
- Analysis templates
- Report generation

**API Integration Generator**:
- OpenAPI/Swagger spec parsing
- Client code generation
- API documentation loading

## Risks & Mitigations

### Risk 1: Skill Discovery Performance with Many Skills

**Impact**: High (affects agent startup time)
**Likelihood**: Medium

**Mitigation**:
- Implement skill caching after first discovery
- Use lazy loading for skill metadata
- Add async skill discovery for parallel processing
- Set reasonable limit on number of skills (warn if >50)

### Risk 2: LLM Fails to Use Skills Appropriately

**Impact**: High (core functionality)
**Likelihood**: Medium

**Mitigation**:
- Provide clear, actionable skill descriptions in frontmatter
- Include usage examples in SKILL.md
- Test with multiple LLM providers to ensure compatibility
- Add skill selection guidance to base system prompt
- Include "when to use this skill" section in instructions

### Risk 3: File Path Security Vulnerabilities

**Impact**: High (security issue)
**Likelihood**: Low

**Mitigation**:
- Implement strict path validation using Path.resolve()
- Whitelist approach: only skills/ directory accessible
- Add comprehensive security tests
- Document security considerations for skill authors
- Consider read-only file access in MVP

### Risk 4: Workshop Time Constraints

**Impact**: Medium (affects learning outcomes)
**Likelihood**: Medium

**Mitigation**:
- Pre-build all components, focus workshop on demonstration
- Provide complete working code in repository
- Create modular sections that can be skipped if needed
- Record workshop for asynchronous learning
- Prepare 60-minute and 90-minute versions

### Risk 5: Dependency on External APIs (Weather Skill)

**Impact**: Low (demo only)
**Likelihood**: High

**Mitigation**:
- Provide fallback mock data for weather skill
- Document API key acquisition clearly
- Make weather API optional (skill works without it)
- Consider using free tier API with generous limits
- Add error handling for API failures

## Appendix

### Related Documentation

**Research Sources**:
- [Claude Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Anthropic: Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Pydantic AI Official Documentation](https://ai.pydantic.dev/)
- [Progressive Disclosure Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

**Technical References**:
- [Pydantic AI Dependencies](https://ai.pydantic.dev/dependencies/)
- [Pydantic AI Tools](https://ai.pydantic.dev/tools/)
- [Claude Code Skills Architecture](https://mikhail.io/2025/10/claude-code-skills/)

### Key Dependencies

**Required**:
- `pydantic-ai` - Agent framework
- `pydantic` v2 - Data validation
- `pydantic-settings` - Configuration management
- `rich` - Terminal formatting
- `python-dotenv` - Environment variables
- `pyyaml` - YAML parsing

**Optional**:
- `openai` - OpenAI provider support
- `anthropic` - Anthropic provider support
- `pytest` - Testing
- `pytest-asyncio` - Async testing

### Repository Structure

```
custom-skill-agent/
├── .claude/
│   ├── PRD.md                    (this document)
│   └── commands/
├── src/                          (core implementation)
├── skills/                       (skill library)
├── examples/                     (MongoDB RAG agent reference)
├── tests/                        (test suite)
├── .env.example                  (configuration template)
├── pyproject.toml                (dependencies)
└── README.md                     (setup guide)
```

### Example SKILL.md Template

```markdown
---
name: skill-name
description: Brief description for agent discovery (1-2 sentences)
version: 1.0.0
author: Your Name
---

# Skill Name

Brief overview of what this skill does.

## When to Use

- Scenario 1
- Scenario 2
- Scenario 3

## Available Operations

1. Operation 1: Description
2. Operation 2: Description

## Instructions

Step-by-step instructions for using this skill...

## Resources

- `references/api_docs.md` - Detailed API documentation
- `scripts/helper.py` - Helper script for complex operations
- `assets/template.txt` - Template file

## Examples

### Example 1: Simple Use Case
User asks: "..."
Response: "..."

### Example 2: Complex Use Case
User asks: "..."
Response: "..."

## Notes

Additional considerations or limitations.
```

---

**Document Version**: 1.0
**Last Updated**: 2025-12-11
**Status**: Draft for Review
