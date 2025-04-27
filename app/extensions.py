from flask_socketio import SocketIO
from flask_caching import Cache
from flasgger import Swagger

socketio = SocketIO(cors_allowed_origins="*")
cache = Cache()
swagger = Swagger(template={
    "swagger": "2.0",
    "info": {
        "title": "UCQIRE API",
        "description": "Professional Movie & Series API backend",
        "version": "1.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"]
})
