# LangChain Adapter Guide

Integrate CrDB SkillForge into LangChain Python agents.

## Usage Example

```python
from adapters.langchain.src import load_skills

skills = load_skills()

# Retrieve structured tool for hotspot diagnosis
tool = skills["avoiding-hotspots"]

result = tool.invoke({
    "question": "How do I avoid primary key hotspots?"
})

print(result["content_snippet"])
```
