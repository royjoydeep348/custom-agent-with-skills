# Feature: Complete MVP - Remaining Items from PRD

The following plan should be complete, but it's important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Complete all remaining items from the PRD to deliver a fully functional MVP of the Custom Skill-Based Pydantic AI Agent. This includes:
1. Creating the advanced `code_review` skill with extensive reference materials (45KB+)
2. Creating `tests/test_agent.py` for agent integration tests
3. Completing and enhancing `README.md` with full setup and usage documentation

## User Story

As a **workshop participant or Python AI developer**
I want **a complete, working skill-based agent with multiple demo skills and comprehensive documentation**
So that **I can understand progressive disclosure patterns and extend the system with my own skills**

## Problem Statement

The current implementation is ~80% complete but missing:
- The advanced `code_review` skill that demonstrates Level 3 progressive disclosure with large reference files
- Agent integration tests to validate the system works end-to-end
- Complete README documentation for workshop participants

## Solution Statement

Create the missing code_review skill with:
- SKILL.md with multi-step review workflow
- Multiple reference files (best_practices.md, security_checklist.md, common_antipatterns.md)
- Scripts for lint checking (optional helpers)

Add agent integration tests to validate:
- Agent initialization and system prompt generation
- Tool registration and invocation
- Progressive disclosure flow

Update README with complete setup, usage, and workshop instructions.

## Feature Metadata

**Feature Type**: Enhancement (completing MVP)
**Estimated Complexity**: Medium
**Primary Systems Affected**: `skills/`, `tests/`, `README.md`
**Dependencies**: None (all dependencies already in pyproject.toml)

---

## CONTEXT REFERENCES

### Relevant Codebase Files IMPORTANT: YOU MUST READ THESE FILES BEFORE IMPLEMENTING!

- `skills/weather/SKILL.md` (full file) - Why: Template for SKILL.md structure, frontmatter format
- `skills/weather/references/api_reference.md` (full file) - Why: Pattern for reference documentation
- `src/skill_loader.py` (lines 13-21) - Why: SkillMetadata fields to ensure YAML frontmatter is valid
- `src/skill_tools.py` (lines 14-64) - Why: How load_skill strips frontmatter
- `src/agent.py` (full file) - Why: Agent structure for integration tests
- `tests/test_skill_loader.py` (full file) - Why: Test pattern and fixtures
- `tests/test_skill_tools.py` (full file) - Why: Mock patterns for RunContext and Dependencies
- `.claude/PRD.md` (lines 349-393) - Why: Code review skill specification
- `examples/tools.py` (lines 15-25) - Why: SearchResult model pattern for reference

### New Files to Create

**Code Review Skill:**
- `skills/code_review/SKILL.md` - Main skill file with YAML frontmatter and multi-step instructions
- `skills/code_review/references/best_practices.md` - Best practices guide (~10KB)
- `skills/code_review/references/security_checklist.md` - Security review checklist (~15KB)
- `skills/code_review/references/common_antipatterns.md` - Antipatterns guide (~20KB)
- `skills/code_review/scripts/lint_patterns.py` - Simple helper script (optional, for demonstration)

**Tests:**
- `tests/test_agent.py` - Agent integration tests

**Documentation:**
- `README.md` - Full documentation (update existing)

### Relevant Documentation YOU SHOULD READ THESE BEFORE IMPLEMENTING!

- [OWASP Top 10](https://owasp.org/Top10/) - Security checklist reference
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) - Best practices reference
- [Pydantic AI Agent Testing](https://ai.pydantic.dev/testing/) - How to test Pydantic AI agents

### Patterns to Follow

**SKILL.md Frontmatter Format (from weather skill):**
```yaml
---
name: skill-name
description: Brief description for agent discovery (1-2 sentences)
version: 1.0.0
author: Workshop Team
---
```

**Test Mock Pattern (from test_skill_tools.py):**
```python
@dataclass
class MockDependencies:
    """Mock dependencies for testing."""
    skill_loader: Optional[SkillLoader] = None

@dataclass
class MockContext:
    """Mock RunContext for testing tools."""
    deps: MockDependencies = field(default_factory=MockDependencies)
```

**Reference File Format (from api_reference.md):**
- Use markdown with headers, tables, code blocks
- Include practical examples
- Structure for quick scanning (headers, bullets, tables)

---

## IMPLEMENTATION PLAN

### Phase 1: Code Review Skill Foundation

Create the code_review skill directory structure and SKILL.md with multi-step review workflow instructions.

**Tasks:**
- Create skill directory structure
- Write SKILL.md with comprehensive review instructions
- Reference the documentation files that will be created

### Phase 2: Reference Documentation

Create the three major reference files that demonstrate Level 3 progressive disclosure.

**Tasks:**
- Create best_practices.md (~10KB)
- Create security_checklist.md (~15KB)
- Create common_antipatterns.md (~20KB)
- Create optional lint_patterns.py helper script

### Phase 3: Agent Integration Tests

Create comprehensive tests for the agent module.

**Tasks:**
- Test agent initialization
- Test system prompt includes skill metadata
- Test tool registration works
- Test full skill invocation flow

### Phase 4: README Documentation

Update README with complete project documentation.

**Tasks:**
- Project overview and key concepts
- Installation and setup instructions
- Usage examples
- Workshop guide
- Skill creation guide

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### Task 1: CREATE skills/code_review/SKILL.md

- **IMPLEMENT**: Create SKILL.md with YAML frontmatter and multi-step code review instructions
- **PATTERN**: Mirror `skills/weather/SKILL.md` structure
- **IMPORTS**: None (markdown file)
- **GOTCHA**: Frontmatter must have `name`, `description` fields (required by SkillMetadata)
- **CONTENT REQUIREMENTS**:
  - Name: `code_review`
  - Description: Clear trigger for when to use (code quality, security, best practices)
  - When to Use section
  - Multi-step review workflow (analyze → check practices → check security → report)
  - Reference file links to `references/best_practices.md`, `references/security_checklist.md`, `references/common_antipatterns.md`
  - Examples section
- **VALIDATE**: `python -c "from src.skill_loader import SkillLoader; from pathlib import Path; l=SkillLoader(Path('skills')); s=l.discover_skills(); print(f'Found {len(s)} skills'); assert 'code_review' in l.skills"`

### Task 2: CREATE skills/code_review/references/best_practices.md

- **IMPLEMENT**: Create comprehensive best practices guide (~10KB)
- **PATTERN**: Mirror `skills/weather/references/api_reference.md` format (markdown with tables/code)
- **CONTENT REQUIREMENTS**:
  - Code organization principles
  - Naming conventions
  - Function design (single responsibility, pure functions)
  - Error handling patterns
  - Documentation standards
  - Testing principles
  - Code examples for each section
- **TARGET SIZE**: ~10KB (approximately 400-500 lines)
- **VALIDATE**: `python -c "from pathlib import Path; p=Path('skills/code_review/references/best_practices.md'); assert p.exists(); print(f'Size: {len(p.read_text())} bytes')"`

### Task 3: CREATE skills/code_review/references/security_checklist.md

- **IMPLEMENT**: Create security review checklist (~15KB)
- **PATTERN**: Structured checklist format with explanations
- **CONTENT REQUIREMENTS**:
  - Input validation section
  - Authentication & authorization
  - SQL injection prevention
  - XSS prevention
  - CSRF protection
  - Secret management
  - Dependency security
  - Logging security
  - OWASP Top 10 quick reference
  - Code examples showing vulnerable vs secure patterns
- **TARGET SIZE**: ~15KB (approximately 600-700 lines)
- **VALIDATE**: `python -c "from pathlib import Path; p=Path('skills/code_review/references/security_checklist.md'); assert p.exists(); print(f'Size: {len(p.read_text())} bytes')"`

### Task 4: CREATE skills/code_review/references/common_antipatterns.md

- **IMPLEMENT**: Create antipatterns guide (~20KB)
- **PATTERN**: Problem/Solution format with code examples
- **CONTENT REQUIREMENTS**:
  - God class/function antipattern
  - Spaghetti code
  - Copy-paste programming
  - Magic numbers/strings
  - Deep nesting
  - Premature optimization
  - Over-engineering
  - Poor error handling patterns
  - Resource leaks
  - Race conditions
  - Each antipattern should have: Description, Why it's bad, How to detect, How to fix, Code examples
- **TARGET SIZE**: ~20KB (approximately 800-1000 lines)
- **VALIDATE**: `python -c "from pathlib import Path; p=Path('skills/code_review/references/common_antipatterns.md'); assert p.exists(); print(f'Size: {len(p.read_text())} bytes')"`

### Task 5: CREATE skills/code_review/scripts/lint_patterns.py

- **IMPLEMENT**: Simple Python script with pattern checking utilities (demonstration purposes)
- **PATTERN**: Standard Python module with type hints and docstrings
- **IMPORTS**: `import re`, `from typing import List, Dict`, `from pathlib import Path`
- **CONTENT REQUIREMENTS**:
  - Function to check for magic numbers
  - Function to check for deep nesting
  - Function to check for long functions
  - Simple pattern-based checks (regex)
  - Clear docstrings explaining each check
- **TARGET SIZE**: ~100-150 lines
- **GOTCHA**: This is a demonstration script, not meant to replace real linters
- **VALIDATE**: `python -c "import skills.code_review.scripts.lint_patterns as lp; print('Script imports successfully')"`

### Task 6: CREATE tests/test_agent.py

- **IMPLEMENT**: Agent integration tests
- **PATTERN**: Mirror `tests/test_skill_tools.py` mock patterns
- **IMPORTS**:
  ```python
  import pytest
  from pathlib import Path
  from unittest.mock import Mock, AsyncMock, patch
  from dataclasses import dataclass, field
  from typing import Optional
  from src.agent import skill_agent, get_system_prompt
  from src.skill_loader import SkillLoader
  from src.dependencies import AgentDependencies
  ```
- **TEST CASES**:
  1. `test_agent_has_skill_tools_registered` - Verify tools are registered
  2. `test_system_prompt_includes_skill_metadata` - Verify skill metadata in prompt
  3. `test_agent_initialization` - Verify agent can be created
  4. `test_load_skill_tool_integration` - Test load_skill_tool works via agent
- **GOTCHA**: Use pytest-asyncio for async tests, mock settings to avoid .env dependency
- **VALIDATE**: `pytest tests/test_agent.py -v`

### Task 7: UPDATE README.md

- **IMPLEMENT**: Complete project documentation
- **PATTERN**: Standard Python project README with workshop focus
- **CONTENT REQUIREMENTS**:
  - Project title and badge placeholders
  - Overview (what is progressive disclosure, why it matters)
  - Key Features section
  - Quick Start (install, configure, run)
  - Architecture diagram (ASCII)
  - Usage examples (CLI interaction, skill loading)
  - Creating Your Own Skill guide
  - Workshop Information section
  - Contributing section
  - License section
- **TARGET SIZE**: ~500-700 lines
- **GOTCHA**: Don't add emojis unless asked
- **VALIDATE**: Manual review - file should be comprehensive and follow markdown best practices

### Task 8: VALIDATE Full System

- **IMPLEMENT**: Run all validation commands to ensure system works
- **VALIDATE ALL**:
  1. `pytest tests/ -v` - All tests pass
  2. `python -c "from src.skill_loader import SkillLoader; from pathlib import Path; l=SkillLoader(Path('skills')); s=l.discover_skills(); print([sk.name for sk in s]); assert len(s) >= 2"` - Both skills discovered
  3. `python -c "from src.agent import skill_agent; print(f'Agent tools: {[t.name for t in skill_agent.tools.values()]}')"` - Agent has tools

---

## TESTING STRATEGY

### Unit Tests

**test_agent.py** should cover:
- Agent tool registration (at least 5 tools: load_skill_tool, read_skill_file_tool, list_skill_files_tool, http_get_tool, http_post_tool)
- System prompt generation with skill metadata
- Mock-based testing without real LLM calls

### Integration Tests

**Skill Discovery Integration:**
- Verify both weather and code_review skills are discovered
- Verify metadata is correctly parsed for both
- Verify system prompt contains both skill descriptions

### Edge Cases

- Missing skills directory handled gracefully
- Malformed SKILL.md files are skipped (existing tests cover this)
- Large reference files can be loaded

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Level 1: Syntax & Style

```bash
# Check Python syntax
python -m py_compile src/agent.py src/skill_loader.py src/skill_tools.py

# Optional: Run ruff if installed
ruff check src/ tests/ --ignore E501 || echo "Ruff not installed or issues found"
```

### Level 2: Unit Tests

```bash
# Run all unit tests
pytest tests/ -v

# Run specific test files
pytest tests/test_skill_loader.py -v
pytest tests/test_skill_tools.py -v
pytest tests/test_agent.py -v
```

### Level 3: Integration Tests

```bash
# Verify skill discovery
python -c "
from src.skill_loader import SkillLoader
from pathlib import Path
loader = SkillLoader(Path('skills'))
skills = loader.discover_skills()
print(f'Discovered {len(skills)} skills:')
for s in skills:
    print(f'  - {s.name}: {s.description[:50]}...')
assert len(skills) >= 2, 'Expected at least 2 skills'
assert 'weather' in loader.skills
assert 'code_review' in loader.skills
print('SUCCESS: All skills discovered')
"

# Verify agent tools
python -c "
from src.agent import skill_agent
tools = list(skill_agent.tools.keys())
print(f'Agent tools: {tools}')
assert 'load_skill_tool' in tools
assert 'read_skill_file_tool' in tools
assert 'list_skill_files_tool' in tools
print('SUCCESS: All tools registered')
"
```

### Level 4: Manual Validation

```bash
# Test CLI starts (will require .env with valid API key)
# python -m src.cli

# Alternative: Test without full CLI
python -c "
from src.dependencies import AgentDependencies
import asyncio

async def test():
    deps = AgentDependencies()
    await deps.initialize()
    print(f'Skills loaded: {list(deps.skill_loader.skills.keys())}')
    print(f'Settings: skills_dir={deps.settings.skills_dir}')
    return True

result = asyncio.run(test())
print('SUCCESS: Dependencies initialize correctly')
"
```

### Level 5: Content Validation

```bash
# Verify reference file sizes (should be substantial)
python -c "
from pathlib import Path
files = [
    ('best_practices.md', 8000),
    ('security_checklist.md', 12000),
    ('common_antipatterns.md', 15000),
]
for name, min_size in files:
    p = Path(f'skills/code_review/references/{name}')
    size = len(p.read_text())
    status = 'OK' if size >= min_size else 'WARN: too small'
    print(f'{name}: {size} bytes ({status})')
"
```

---

## ACCEPTANCE CRITERIA

- [x] Weather skill exists and works (already complete)
- [ ] Code review skill exists with SKILL.md
- [ ] Code review skill has 3 reference files (best_practices, security_checklist, common_antipatterns)
- [ ] Reference files are substantial (~10KB, ~15KB, ~20KB respectively)
- [ ] Code review skill has optional scripts directory
- [ ] Agent integration tests exist and pass
- [ ] All existing tests continue to pass
- [ ] README.md provides complete setup and usage documentation
- [ ] Both skills are discovered on agent startup
- [ ] System prompt includes metadata for both skills

---

## COMPLETION CHECKLIST

- [ ] All tasks completed in order
- [ ] Each task validation passed immediately
- [ ] All validation commands executed successfully
- [ ] Full test suite passes (unit + integration)
- [ ] No linting or type checking errors
- [ ] Manual testing confirms feature works
- [ ] Acceptance criteria all met
- [ ] Code reviewed for quality and maintainability

---

## NOTES

### Design Decisions

1. **Code Review Skill Complexity**: The code_review skill is intentionally complex to demonstrate Level 3 progressive disclosure. The agent should NOT load all 45KB+ of reference material upfront - only when specific guidance is needed.

2. **Reference File Sizes**: The PRD specifies ~10KB, ~15KB, ~20KB for the three reference files. These are substantial to demonstrate real-world use cases where context window management matters.

3. **lint_patterns.py Script**: This is a simple demonstration script, not a replacement for real tools like ruff/flake8. It shows how skills can include executable scripts.

4. **Test Strategy**: Agent tests use mocks to avoid requiring a real LLM API key during testing. The focus is on verifying tool registration and system prompt generation.

### Risks and Mitigations

1. **Risk**: Reference files may be too generic
   **Mitigation**: Include specific code examples and practical checklists

2. **Risk**: Agent tests may be brittle
   **Mitigation**: Test structure/registration, not LLM responses

3. **Risk**: README may not cover all use cases
   **Mitigation**: Include "Creating Your Own Skill" section for extensibility

### Workshop Context

This MVP completion enables the workshop to demonstrate:
- Progressive disclosure in action (simple weather vs complex code_review)
- How to create and structure skills
- Testing patterns for skill-based agents
- Practical documentation for adoption
