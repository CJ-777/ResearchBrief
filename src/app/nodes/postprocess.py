from ..schemas import FinalBrief


def validate_and_fix(brief: FinalBrief) -> FinalBrief:
    """
    Post-process a generated FinalBrief to enforce additional rules beyond Pydantic validation.

    Rules currently applied:
    1. Ensure each section has a title; if missing, set as 'Untitled Section'.
    2. Ensure each section has content; if missing, set as ['Content missing'].
    3. Placeholder for additional post-processing (sanitizing text, trimming, formatting).
    """
    for section in brief.sections:
        # Ensure section has a title
        if not section.get("title"):
            section["title"] = "Untitled Section"

        # Ensure section has content
        if not section.get("content"):
            section["content"] = ["Content missing"]

    # Add other custom rules here as needed

    return brief
