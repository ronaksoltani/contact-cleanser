from contact_cleanser.normalizer import normalize_email, normalize_phone


def test_email_is_normalized_and_disposable_domains_are_flagged():
    assert normalize_email("USER@Example.com")["normalized"] == "user@example.com"
    assert normalize_email("person@mailinator.com")["disposable"] is True


def test_phone_is_formatted_as_e164():
    result = normalize_phone("(415) 555-2671", "US")
    assert result["valid"] is True
    assert result["normalized"] == "+14155552671"
