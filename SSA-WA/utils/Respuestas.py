class Respuesta:
    def __init__(self, Exito: bool, Mensaje: str, Detalle):
        self.Exito = Exito   
        self.Mensaje = Mensaje   
        self.Detalle = Detalle   
    
    def to_dict(self):
        return {"Exito": self.Exito, "Mensaje": self.Mensaje, "Detalle": self.Detalle}