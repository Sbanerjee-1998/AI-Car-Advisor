def register_payload(email: str = "driver@example.com") -> dict[str, str]:
    return {"name": "Test Driver", "email": email, "password": "correct horse", "password_confirmation": "correct horse"}
