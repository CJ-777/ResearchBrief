from ..schemas import FinalBrief


def validate_and_fix(brief: FinalBrief) -> FinalBrief:
    # Schema already enforces references; extend with custom rules later
    return brief