from utils.db import Acceso
from collections import defaultdict
import json
from datetime import datetime
from flask import request
class TutorHijos:
    
    def __init__(self,Params,ID_PACIENTE):
        self.Params = Params
        self.ID_PACIENTE = ID_PACIENTE
    
    def ExistePaciente(self,CURP):
        condiciones = {"REF_CURP": ("=", CURP)}
        columnas = ["count(*) Total"]
        acceso = Acceso("VACMXT_PACIENTE").EjecutaVista(condiciones=condiciones, columnas=columnas)
        return acceso
    
    def ExisteTutor(self,CURP):
        condiciones = {"REF_CURP_TUTOR": ("=", CURP)}
        columnas = ["ID_TUTOR"]
        acceso = Acceso("VACMXT_TUTOR").EjecutaVista(condiciones=condiciones, columnas=columnas)
        return acceso
    
    def BuscaDatosPaciente(self):
        condiciones = {"ID_PACIENTE": ("=", self.ID_PACIENTE)}
        columnas = [
            "ID_LOCALIDAD",
            "ID_GENERO",
            "ID_LENGUA",
            "NOM_PACIENTE",
            "NOM_AP_PATERNO",
            "NOM_AP_MATERNO",
            "REF_CURP",
            "REF_DOMICILIO"            
            ]
        acceso = Acceso("VACMXT_PACIENTE").EjecutaVista(condiciones=condiciones, columnas=columnas)
        return acceso

    def InsertaPaciente(self,param):
        acceso = Acceso().EjecutaStoredProcedure("SP_InsertaActualizaPaciente",param)
        return acceso
    
    def InsertaTutor(self,param):
        acceso = Acceso().EjecutaStoredProcedure("SP_InsertaActualizaTutor",param)
        return acceso   
    
    def IngresaPacienteHijos(self):
        Existe = self.ExistePaciente(self.Params["REF_CURP"])[0]["Total"] > 0
        if Existe:
            return {"mensaje": "El paciente con CURP " + self.Params["REF_CURP"] + " ya existe en el registro."}
        Res_paciente = self.BuscaDatosPaciente()[0]
        if not Res_paciente:
            return {"mensaje": "No se encontraron datos del paciente"}
        
        ExisteTutor = self.ExisteTutor(self.Params["REF_CURP"])
      
        if not ExisteTutor:    
            params_Tutor = [int(Res_paciente["ID_LOCALIDAD"]),
                                int(Res_paciente["ID_GENERO"]),
                                int(Res_paciente["ID_LENGUA"]),
                                str(Res_paciente["NOM_PACIENTE"]),
                                str(Res_paciente["NOM_AP_PATERNO"]),
                                str(Res_paciente["NOM_AP_MATERNO"]),
                                str(Res_paciente["REF_CURP"]),
                                str(Res_paciente["REF_DOMICILIO"]),
                                None, True, None, None, None,
                                datetime.now(),None, None
                                ]
            Res_tutor = self.InsertaTutor(params_Tutor)[0]
            params_Paciente = [
                self.Params["ID_LOCALIDAD"],
                self.Params["ID_GENERO"],
                self.Params["ID_LENGUA"],
                Res_tutor["mensaje"],
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
                self.Params["REF_DOMICILIO"]
            ]
            Res_paciente_insert = self.InsertaPaciente(params_Paciente)[0]
            return Res_paciente_insert
        else:
            params_Paciente = [
                self.Params["ID_LOCALIDAD"],
                self.Params["ID_GENERO"],
                self.Params["ID_LENGUA"],
                ExisteTutor["ID_TUTOR"],
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
                self.Params["REF_DOMICILIO"]
            ]
            Res_paciente_insert = self.InsertaPaciente(params_Paciente)[0]
            return Res_paciente_insert
        


        
        
 
    
  
 