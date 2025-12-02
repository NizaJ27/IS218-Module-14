from app.security import hash_password, verify_password


def test_hash_and_verify():
    raw = "s3cret_pass"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
