from utils.db import Acceso
from collections import defaultdict
import json
from datetime import datetime
from flask import request

class paciente:
    def __init__(self,Params):
        self.Params = Params
    
    def InsertaPaciente(self,param):
        acceso = Acceso().EjecutaStoredProcedure("SP_InsertaActualizaPaciente",param)
        return acceso
    
    def InsertaUsuario(self,param):
        acceso = Acceso().EjecutaStoredProcedure("SP_InsertaActualizaPaciente",param)
        return acceso
    
    def Paciente_Usuario(self,param):
        params_Paciente = [
            self.Params["ID_LOCALIDAD"],
            self.Params["ID_GENERO"],
            self.Params["ID_LENGUA"],
            None,
            self.Params["ID_TIPO_FAMILIAR"],
            self.Params["NOM_PACIENTE"],
            self.Params["NOM_AP_PATERNO"],
            self.Params["NOM_AP_MATERNO"],
            self.Params["REF_CURP"],
            self.Params["FEC_NACIMIENTO"],
            True,
            None,
            True,
            datetime.now(),
            None,
            None,
            self.Params["REF_DOMICILIO"]]
        Response_Paciente = self.InsertaPaciente(params_Paciente)
        if not bool(Response_Paciente[0]["error"]):
            params_Usuario = [

            ]
            Response_Usuario = self.InsertaUsuario(params_Usuario)
            return Response_Usuario
            
            
        
