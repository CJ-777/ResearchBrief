def test_save_and_load_brief(sample_brief):
    from src.app.store.history import save_brief, load_user_history

    # Save brief
    save_brief("user123", sample_brief)

    # Load briefs
    briefs = load_user_history("user123", limit=5)

    assert len(briefs) >= 1
    latest = briefs[0]
    assert latest.topic == sample_brief.topic
    assert latest.thesis == sample_brief.thesis
    assert latest.references == sample_brief.references
