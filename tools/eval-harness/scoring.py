from typing import Dict, Any, List

def score_case_result(case: Dict[str, Any], selected_skill: str, behaviors_found: List[str], db_passed: bool) -> Dict[str, Any]:
    expected_skills = case.get("expected_skill", [])
    expected_behaviors = case.get("expected_behaviors", [])

    skill_match = selected_skill in expected_skills
    behavior_score = len(set(behaviors_found).intersection(set(expected_behaviors))) / max(len(expected_behaviors), 1)

    db_score = 1.0 if (not case.get("database_required") or db_passed) else 0.0
    overall_score = (0.5 * (1.0 if skill_match else 0.0)) + (0.3 * behavior_score) + (0.2 * db_score)

    return {
        "case_name": case.get("name"),
        "skill_match": skill_match,
        "selected_skill": selected_skill,
        "behavior_score": round(behavior_score, 2),
        "db_passed": db_passed,
        "overall_score": round(overall_score, 2),
        "passed": overall_score >= 0.75
    }
