class _UserSchemaConfig:
    ADD_USER = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"},
            "email": {"type": "string"},
        },
        "required": ["username", "password", "email"],
    }
    LOGIN = {
        "type": "object",
        "properties": {"username": {"type": "string"}, "password": {"type": "string"}},
        "required": ["username", "password"],
    }
