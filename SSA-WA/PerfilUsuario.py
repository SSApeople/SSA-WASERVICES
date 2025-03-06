from flask import Flask, jsonify, request
from utils.db import Acceso
from flask import Blueprint
from flask_jwt_extended import jwt_required
from decouple import config
from utils.CallOpenAI import OpenAIConector


PerfilPaciente_bp = Blueprint('PerfilPaciente', __name__)

@PerfilPaciente_bp.route('Obtener/<idPaciente>',methods=['GET'])
def PerfilPacienteGet(idPaciente):
    Consolidado = {}
    PPacienteGet = Acceso("VW_PERFILPACIENTE").EjecutaVista(condiciones={"ID_PACIENTE": ("=", idPaciente)})
    if len(PPacienteGet) > 0:
        if PPacienteGet[0]["ValTutor"] is not None:
            condiciones={
                "ID_TUTOR": ("=", PPacienteGet[0]["ValTutor"])
                }
            columnas = [
            'ID_PACIENTE',
            'ID_LOCALIDAD',
            'NOM_PACIENTE',
            'NOM_AP_PATERNO',
            'NOM_AP_MATERNO',
            'REF_CURP',
            'FEC_NACIMIENTO',
            'REF_DOMICILIO'
            ]
            Hijos_ = Acceso("VACMXT_PACIENTE").EjecutaVista(condiciones=condiciones,columnas=columnas)
            
            Consolidado = {
                "Tutor":PPacienteGet,
                "Hijos":Hijos_
            }
        else:
            Consolidado = {
                "Tutor":PPacienteGet
            }
    return jsonify(Consolidado)
    
    

