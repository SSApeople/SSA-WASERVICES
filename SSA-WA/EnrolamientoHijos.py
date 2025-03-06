from flask import Flask, jsonify, request
from utils.db import Acceso
from flask import Blueprint
from flask_jwt_extended import jwt_required
from decouple import config
from utils.CallOpenAI import OpenAIConector
from Funciones.TutorHijos import TutorHijos

EnrolamientoHijos_bp = Blueprint('EnrolamientoHijos', __name__)

@EnrolamientoHijos_bp.route('Inserta/<IdPaciente>',methods=['POST'])
def PerfilPacienteGet(IdPaciente):
    datos = request.get_json()
    Response = TutorHijos(datos,IdPaciente).IngresaPacienteHijos()
    return jsonify(Response)
    
    

