from adapters.langchain.src.tools import load_skills

def test_langchain_tools_loading():
    tools = load_skills()
    assert len(tools) >= 21
    assert "avoiding-hotspots" in tools

    tool = tools["avoiding-hotspots"]
    res = tool.invoke({"question": "How do I prevent hotspots in CockroachDB?"})
    assert res["skill"] == "avoiding-hotspots"
    assert "full_skill_content" in res
