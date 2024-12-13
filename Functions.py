import requests
import json
import re

class Operaciones:
    
    def __init__(self):
        self.token = "EAARM4gGaSxsBO8QH5pZCFOtJYZAe8AVHd3dXFuZCFG4ZCyLLHuZC4uPXKGDN3jscFnJxXxN1RVMDZANFZBkgjYsobZAQZCZAbFin2n8SeOIoOVc2DGG18wXiZBbHFZCyXaeoj4K3TkrwIBhLi1dgPYQKtOAXluTFbeQU9ejPE2HkUN84Y7u7k904VYHfBNJwkNNZCv6ih"
        self.numIdentif = "429808380226322"
        self.imageWelcome = "https://d2q79iu7y748jz.cloudfront.net/s/_squarelogo/256x256/61e7d9b79fb925830e9a4a64d326b09f"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self.url = "https://graph.facebook.com/v17.0/"+self.numIdentif+"/messages"

    def IfExistWelcome(value)->str:
        try:
            body = value['text']['body']
            sender_id = value['from']
            return sender_id
        except Exception as e:
            return ''
        
    def IfExistTipoVacuna(self,data)->str:
        try:
            body = data['interactive']['list_reply']['id']
            return body
        except Exception as e:
            return ''    
        
        
    def EnviaBienvenida(self,value):
        Celular = Operaciones.IfExistWelcome(value).replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {"type": "image", "image":{"link":self.imageWelcome}},
                "body": {"text": "Por favor, selecciona una opción a continuación:"},
                "footer": {"text": "Gracias por usar nuestro servicio"},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "1", "title": "Campañas activas 💉"}},
                        {"type": "reply", "reply": {"id": "2", "title": "Verificar vacunas 💉"}},
                    ]
                },
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"
 
        
        
        
    def EnviaListaCampanas(self,value):
        Celular = value['from'].replace("521", "52")
        data = {
                "messaging_product": "whatsapp",
                "to": Celular,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "header": {
                        "type": "text",
                        "text": "Campañas Disponibles"
                    },
                    "body": {
                        "text": "Selecciona una campaña de las opciones disponibles:"
                    },
                    "footer": {
                        "text": "Elige una opción para continuar"
                    },
                    "action": {
                        "button": "Ver opciones",
                        "sections": [
                            {
                                "title": "Campañas de Vacunación",
                                "rows": [
                                    {"id": "influenza", "title": "Influenza"},
                                    {"id": "covid", "title": "COVID"},
                                    {"id": "vph", "title": "VPH"},
                                    {"id": "neumococo", "title": "Neumococo"}
                                ]
                            }
                        ]
                    }
                }
            }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"
        
    def EnviaEfecSecundariosCP(self,value):
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,
            "type": "interactive",
            "interactive": {
                "type": "button",
                
                "body": {"text": "Por favor, selecciona una opción a continuación:"},
                
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "ES", "title": "Efectos Secundarios"}},
                        {"type": "reply", "reply": {"id": "SV", "title": "Sitios de Vacunación"}},
                    ]
                },
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"
        
    def EnviasoloEfectosSecu(self,value):
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,   
            "type": "text",   
            "text": {
                "body": "Algunos de los efectos secundarios reportados por medicos y pacientes son:\n-Dolor, inflamación y enrojecimiento en el brazo, en la zona de la inyección.\n-Cansancio, dolor de cabeza, dolor muscular.\n-Escalofríos.\n-Náuseas.\n-Fiebre.\n\n Si los sintomas son incapacitantes debé consultar a su médico responsable de la aplicación."
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"
    def PideCP(self,value):
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,   
            "type": "text",   
            "text": {
                "body": "Ingresa tu código Postal para poder decirte que clinicas estan cerca de tu domicilio y puedas aplicarte tu vacuna de COVID."
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"
        
    def es_codigo_postal(self,cadena: str) -> bool:
        """
        Verifica si una cadena es un código postal válido (5 dígitos).
        
        Args:
            cadena (str): La cadena a validar.
        
        Returns:
            bool: True si es un código postal válido, False en caso contrario.
        """
        # Expresión regular para un código postal de 5 dígitos
        patron = r"^\d{5}$"
        return bool(re.match(patron, cadena))
    
    
    
    
    def UbicaClinica(self,value):
        
        copy_ = "Las clinicas donde puedes acudir a ponerte tu vacuna de COVID cerca de tu domicilio son:\n\n\n"
        copy_ = copy_ + "IMSS Unidad de Medicina Familiar 28 'DEL VALLE'\n"
        copy_ = copy_ + "https://maps.app.goo.gl/CxK7dTX6GFjTKWoZ9\n\n"
        
        copy_ = copy_ + "Centro de Salud T-III Portales\n"
        copy_ = copy_ + "https://maps.app.goo.gl/FhTfyBdy1t7nmj56A"
        
        
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,   
            "type": "text",   
            "text": {
                "body": copy_
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"
    
    
    def es_curp_valida(self,cadena: str) -> bool:
        patron = r"^[A-Z]{4}\d{6}[HM][A-Z]{2}[A-Z]{3}[A-Z0-9]\d$"
        return bool(re.match(patron, cadena))    
        
        
    def PideCurp(self,value):
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,   
            "type": "text",   
            "text": {
                "body": "Por favor ingresa tu Curp:"
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"    
        

    def VacunasAplicadas(self,value):
        
        copy_ = "Las vacunas que tienes aplicadas hasta el momento son:\n\n\n"
        copy_ = copy_ + "COVID 19, Marca: Pfizer, 3º Dosis\n\n"
        copy_ = copy_ + "Influenza Estacionaria, Marca: Afluria, 2023\n\n"
        copy_ = copy_ + "COVID 19, Marca: astrazeneca , 2º Dosis\n\n"
        copy_ = copy_ + "COVID 19, Marca: astrazeneca , 1º Dosis\n\n"
 
        
        
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,   
            "type": "text",   
            "text": {
                "body": copy_
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"

    def VacunasNoAplicadas(self,value):
        
        copy_ = "Las vacunas que aùn no tienes aplicadas son:\n\n\n"
        copy_ = copy_ + "COVID 19, 4º Dosis\n\n"
        copy_ = copy_ + "Influenza Estacionaria 2024\n\n"
        copy_ = copy_ + "VPH, Marca: Cervarix, 1º Dosis\n\n"
 
 
        
        
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,   
            "type": "text",   
            "text": {
                "body": copy_
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"

    def quieresUbicar(self,value):
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,
            "type": "interactive",
            "interactive": {
                "type": "button",
                
                "body": {"text": "Quieres ubicar un puesto de vacunaciòn cercano a tu domicilio?"},
                
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "SiUbi", "title": "Si"}},
                        {"type": "reply", "reply": {"id": "NoUbi", "title": "Menù Princial"}},
                        {"type": "reply", "reply": {"id": "salir", "title": "salir"}},

                    ]
                },
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"

    def PreguntarSalida(self,value):
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,
            "type": "interactive",
            "interactive": {
                "type": "button",
                
                "body": {"text": "¿Hay algo mas en lo que pueda ayudarte?"},
                
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "NoAy", "title": "No, Gracias!"}},
                        {"type": "reply", "reply": {"id": "SiAy", "title": "Llevame al menu principal"}},
                    ]
                },
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"
        




    def Despedida(self,value):
        
 
        copy_ = "Fue un placer atenderte, si requieres mas ayuda siempre puede escribirme un *Hola* y con gusto te responderé"
 
 
        
        
        Celular = value['from'].replace("521", "52")
        data = {
            "messaging_product": "whatsapp",
            "to": Celular,   
            "type": "text",   
            "text": {
                "body": copy_
            },
        }
        VALOR_ = requests.post(self.url, headers=self.headers, json=data)
        try:
            Error_ = VALOR_.content.decode('utf-8')
            return Error_
        except Exception as e:
            return "Procesado"



