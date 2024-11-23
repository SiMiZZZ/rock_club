import api  # noqa: F401
import api.v1  # noqa: F401


from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info  # type: ignore

app = Application()


docs = OpenAPIHandler(info=Info(title="URFU Rock Club Api", version="0.0.1"))
docs.bind_app(app)

app.use_cors(
    allow_methods="*",
    allow_origins="*",
    allow_headers="*",
    max_age=300,
)
