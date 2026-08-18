import os
import glob
import yaml
from pathlib import Path
from typing import Dict, Any, List

class CrDBSkillTool:
    """
    Structured tool wrapper representing a canonical CockroachDB skill for LangChain agents.
    """
    def __init__(self, name: str, description: str, content: str):
        self.name = name
        self.description = description
        self.content = content

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        question = input_data.get("question", "")
        return {
            "skill": self.name,
            "matched_question": question,
            "instruction": f"Follow diagnosis & verification steps defined in skill '{self.name}'",
            "content_snippet": self.content[:300] + "...",
            "full_skill_content": self.content
        }

def load_skills() -> Dict[str, CrDBSkillTool]:
    """
    Dynamically loads all canonical SKILL.md definitions from the skills/ directory
    and wraps them into LangChain-compatible structured tool objects.
    """
    root_dir = Path(__file__).resolve().parent.parent.parent.parent
    skills_dir = root_dir / "skills"

    skill_files = glob.glob(str(skills_dir / "**" / "SKILL.md"), recursive=True)
    tools = {}

    for s_file in skill_files:
        with open(s_file, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        try:
            frontmatter = yaml.safe_load(parts[1])
            name = frontmatter.get("name")
            desc = frontmatter.get("description", "").strip()
            if name:
                tools[name] = CrDBSkillTool(name, desc, content)
        except Exception:
            continue

    return tools
