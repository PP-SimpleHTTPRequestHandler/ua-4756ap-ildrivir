USERS_LIST = [
    {
        "id": 1,
        "username": "theUser",
        "firstName": "John",
        "lastName": "James",
        "email": "john@email.com",
        "password": "12345",
    }
]

REQUIRED_FIELDS = {
    "id": int,
    "username": str,
    "firstName": str,
    "lastName": str,
    "email": str,
    "password": str,
}

PUT_REQUIRED_FIELDS = {k: v for k, v in REQUIRED_FIELDS.items() if k != "id"}