from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)



def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para todas las rutas
    
    app.config["JWT_SECRET_KEY"] = "PMS2024_PEOPL3M3D14"
    jwt = JWTManager(app)
    # Importar y registrar Blueprints
    from .auth import auth_bp
    from PerfilUsuario import PerfilPaciente_bp
    from EnrolamientoHijos import EnrolamientoHijos_bp
    
 
 
     
    
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(PerfilPaciente_bp, url_prefix="/PerfilPaciente")
    app.register_blueprint(EnrolamientoHijos_bp, url_prefix="/EnrolamientoHijos")
    
    
 
    
    
    return app