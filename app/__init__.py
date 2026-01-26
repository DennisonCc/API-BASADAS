from flask import Flask, render_template, jsonify
from flask_cors import CORS
from app.models.models import db
from flasgger import Swagger
import os

def create_app():
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    
    # Configuration
    # SECURITY IMPLEMENTATION: Fail if DATABASE_URL is not set, avoid hardcoded credentials
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize Extensions
    db.init_app(app)
    CORS(app)
    
    # Swagger Configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API de Control de Pausas",
            "description": "Documentación interactiva para la gestión de pausas activas y personal.",
            "contact": {
                "responsibleOrganization": "ESPE",
                "responsibleDeveloper": "Admin",
                "email": "soporte@espe.edu.ec",
                "url": "https://espe.edu.ec",
            },
            "version": "1.0.1"
        },
        "basePath": "/",  # base bash for blueprint registration
        "schemes": [
            "http",
            "https"
        ]
    }
    
    # Register Blueprints
    from app.api.employee_routes import employee_bp
    from app.api.pause_routes import pause_bp
    
    app.register_blueprint(employee_bp)
    app.register_blueprint(pause_bp)
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Global Error Handlers
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e), code=404), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error="Internal Server Error", code=500), 500
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api')
    def api_index():
        return jsonify({
            "message": "Bienvenido a la API de Control de Pausas",
            "documentation": "/apidocs/",
            "endpoints": {
                "empleados": "/api/empleados",
                "pausas": "/api/pausas"
            }
        })
    
    return app
