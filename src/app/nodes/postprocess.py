from ..schemas import FinalBrief


def validate_and_fix(brief: FinalBrief) -> FinalBrief:
    """
    Post-process a generated FinalBrief to enforce additional rules beyond Pydantic validation.

    Currently:
    - Ensures at least one reference exists (redundant with schema, but placeholder for more rules)
    - Placeholder for other future post-processing: e.g., sanitizing sections, limiting text length, fixing formatting
    """

    # Example custom rule: ensure sections have title and content
    for section in brief.sections:
        if "title" not in section or not section["title"]:
            section["title"] = "Untitled Section"
        if "content" not in section or not section["content"]:
            section["content"] = ["Content missing"]

    # Could add other rules here (e.g., trimming text, checking thesis length)

    return brief
