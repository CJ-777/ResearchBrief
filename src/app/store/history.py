from typing import List, Dict


_MEMORY: List[Dict] = []


def save_brief(user_id: str, topic: str, payload: Dict):
    _MEMORY.append({"user_id": user_id, "topic": topic, **payload})


def load_user_history(user_id: str) -> List[Dict]:
    return [x for x in _MEMORY if x.get("user_id") == user_id]