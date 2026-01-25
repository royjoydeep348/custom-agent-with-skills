"""Unit tests for SkillLoader and SkillMetadata."""

import pytest
from pathlib import Path
from pydantic import ValidationError

from src.skill_loader import SkillLoader, SkillMetadata


class TestSkillMetadata:
    """Tests for SkillMetadata Pydantic model."""

    def test_skill_metadata_model_validation(self, tmp_path: Path) -> None:
        """Test that SkillMetadata accepts valid input."""
        metadata = SkillMetadata(
            name="test_skill",
            description="A test skill for validation",
            version="1.0.0",
            author="Test Author",
            skill_path=tmp_path,
        )

        assert metadata.name == "test_skill"
        assert metadata.description == "A test skill for validation"
        assert metadata.version == "1.0.0"
        assert metadata.author == "Test Author"
        assert metadata.skill_path == tmp_path

    def test_skill_metadata_default_values(self, tmp_path: Path) -> None:
        """Test that SkillMetadata uses defaults for optional fields."""
        metadata = SkillMetadata(
            name="minimal_skill",
            description="Minimal description",
            skill_path=tmp_path,
        )

        assert metadata.version == "1.0.0"
        assert metadata.author == ""

    def test_skill_metadata_missing_required_fields(self, tmp_path: Path) -> None:
        """Test that SkillMetadata raises ValidationError for missing required fields."""
        # Missing name
        with pytest.raises(ValidationError):
            SkillMetadata(description="Test", skill_path=tmp_path)

        # Missing description
        with pytest.raises(ValidationError):
            SkillMetadata(name="test", skill_path=tmp_path)

        # Missing skill_path
        with pytest.raises(ValidationError):
            SkillMetadata(name="test", description="Test")


class TestSkillLoader:
    """Tests for SkillLoader class."""

    def test_skill_loader_discovers_skills(self, tmp_path: Path) -> None:
        """Test that SkillLoader discovers skills from directory."""
        # Create test skill
        skill_dir = tmp_path / "test_skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            """---
name: test_skill
description: A test skill for unit testing
version: 1.0.0
author: Test Author
---

# Test Skill

This is a test skill.
"""
        )

        # Test discovery
        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        assert len(skills) == 1
        assert skills[0].name == "test_skill"
        assert skills[0].description == "A test skill for unit testing"
        assert skills[0].version == "1.0.0"
        assert skills[0].author == "Test Author"
        assert skills[0].skill_path == skill_dir

    def test_skill_loader_empty_directory(self, tmp_path: Path) -> None:
        """Test that empty skills directory returns empty list."""
        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        assert len(skills) == 0

    def test_skill_loader_missing_directory(self, tmp_path: Path) -> None:
        """Test that missing skills directory returns empty list."""
        nonexistent = tmp_path / "nonexistent"
        loader = SkillLoader(nonexistent)
        skills = loader.discover_skills()

        assert len(skills) == 0

    def test_skill_loader_parses_frontmatter(self, tmp_path: Path) -> None:
        """Test that SkillLoader correctly parses YAML frontmatter."""
        skill_dir = tmp_path / "weather"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            """---
name: weather
description: Get weather information for locations
version: 2.0.0
author: Weather Team
---

# Weather Skill

Provides weather information.

## Instructions

Ask for a location to get weather data.
"""
        )

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        assert len(skills) == 1
        skill = skills[0]
        assert skill.name == "weather"
        assert skill.description == "Get weather information for locations"
        assert skill.version == "2.0.0"
        assert skill.author == "Weather Team"

    def test_skill_loader_generates_metadata_prompt(self, tmp_path: Path) -> None:
        """Test that get_skill_metadata_prompt generates correct format."""
        # Create two skills
        for name, desc in [
            ("weather", "Get weather data"),
            ("calendar", "Manage calendar events"),
        ]:
            skill_dir = tmp_path / name
            skill_dir.mkdir()
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(
                f"""---
name: {name}
description: {desc}
---

# {name.title()} Skill
"""
            )

        loader = SkillLoader(tmp_path)
        loader.discover_skills()

        prompt = loader.get_skill_metadata_prompt()

        assert "weather" in prompt
        assert "Get weather data" in prompt
        assert "calendar" in prompt
        assert "Manage calendar events" in prompt
        assert "**weather**" in prompt or "**calendar**" in prompt

    def test_skill_loader_handles_malformed_frontmatter(self, tmp_path: Path) -> None:
        """Test graceful handling of malformed YAML frontmatter."""
        skill_dir = tmp_path / "bad_skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            """---
name: bad_skill
description: [invalid yaml
version: 1.0.0
---

# Bad Skill
"""
        )

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        # Should skip the malformed skill
        assert len(skills) == 0

    def test_skill_loader_handles_missing_frontmatter(self, tmp_path: Path) -> None:
        """Test handling of SKILL.md without frontmatter."""
        skill_dir = tmp_path / "no_frontmatter"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            """# Skill Without Frontmatter

This skill has no YAML frontmatter.
"""
        )

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        # Should skip skill without frontmatter
        assert len(skills) == 0

    def test_skill_loader_handles_missing_required_fields(self, tmp_path: Path) -> None:
        """Test handling of frontmatter missing required fields."""
        skill_dir = tmp_path / "incomplete_skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            """---
name: incomplete_skill
version: 1.0.0
---

# Incomplete Skill

Missing description field.
"""
        )

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        # Should skip skill with missing required fields
        assert len(skills) == 0

    def test_skill_loader_discovers_multiple_skills(self, tmp_path: Path) -> None:
        """Test discovery of multiple skills."""
        skill_names = ["weather", "calendar", "todo"]

        for name in skill_names:
            skill_dir = tmp_path / name
            skill_dir.mkdir()
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text(
                f"""---
name: {name}
description: {name.title()} skill description
---

# {name.title()} Skill
"""
            )

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        assert len(skills) == 3
        discovered_names = {s.name for s in skills}
        assert discovered_names == set(skill_names)

    def test_skill_loader_skills_dict_populated(self, tmp_path: Path) -> None:
        """Test that skills dictionary is populated after discovery."""
        skill_dir = tmp_path / "test_skill"
        skill_dir.mkdir()

        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            """---
name: test_skill
description: Test skill
---

# Test Skill
"""
        )

        loader = SkillLoader(tmp_path)
        loader.discover_skills()

        assert "test_skill" in loader.skills
        assert loader.skills["test_skill"].name == "test_skill"

    def test_skill_loader_empty_prompt_when_no_skills(self, tmp_path: Path) -> None:
        """Test get_skill_metadata_prompt when no skills discovered."""
        loader = SkillLoader(tmp_path)
        loader.discover_skills()

        prompt = loader.get_skill_metadata_prompt()

        assert "No skills" in prompt or prompt == "No skills currently available."
