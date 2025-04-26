from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from app.config import Config
from flasgger import Swagger
from app.auth.routes import auth_bp
from app.movies.routes import movies_bp
from app.series.routes import series_bp
from app.uploads.routes import upload_bp
from app.admin.routes import admin_bp

socketio = SocketIO(cors_allowed_origins="*")
swagger = Swagger(template={
    "swagger": "2.0",
    "info": {
        "title": "UCQIRE API",
        "description": "Professional Movie & Series API backend",
        "version": "1.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ]
})
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, origins=["https://ucqire.com", "https://dashboard.ucqire.com"])
    socketio.init_app(app)
    swagger.init_app(app) 
    

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(movies_bp, url_prefix="/movies")
    app.register_blueprint(series_bp, url_prefix="/series")
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    

    return app
