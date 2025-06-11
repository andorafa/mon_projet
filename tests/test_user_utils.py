import uuid

def test_generate_api_key_format():
    key = str(uuid.uuid4())
    assert isinstance(key, str)
    assert len(key) == 36
