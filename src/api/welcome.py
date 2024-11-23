from blacksheep import get, allow_anonymous


@get("/")
@allow_anonymous()
def get_home():
    return "Welcome to Rock-club"
