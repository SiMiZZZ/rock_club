from blacksheep import get


@get("/api/v1/users")
def get_user():
    return "test_user_api"
