from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PMS2024@10.166.0.56/vacunacion_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo Aplicacion
class Aplicacion(db.Model):
    __tablename__ = 'aplicacion'
    id_aplicacion = db.Column(db.Integer, primary_key=True)
    curp = db.Column(db.String(18), nullable=False)
    id_medico = db.Column(db.Integer, nullable=False)
    id_esquema = db.Column(db.Integer, nullable=False)
    id_clues = db.Column(db.Integer, nullable=False)
    dosis = db.Column(db.Integer, nullable=False)
    fecha_aplicacion = db.Column(db.Date, nullable=False)
    num_dosis = db.Column(db.Integer, nullable=False)
    id_info_vacuna = db.Column(db.Integer, nullable=False)
    id_brigada = db.Column(db.Integer, nullable=False)
    id_estatus = db.Column(db.Integer, nullable=False)
    id_vacuna_lista = db.Column(db.Integer, nullable=False)

    def __init__(self, curp, id_medico, id_esquema, id_clues, dosis, fecha_aplicacion, num_dosis, id_info_vacuna, id_brigada, id_estatus, id_vacuna_lista):
        self.curp = curp
        self.id_medico = id_medico
        self.id_esquema = id_esquema
        self.id_clues = id_clues
        self.dosis = dosis
        self.fecha_aplicacion = fecha_aplicacion
        self.num_dosis = num_dosis
        self.id_info_vacuna = id_info_vacuna
        self.id_brigada = id_brigada
        self.id_estatus = id_estatus
        self.id_vacuna_lista = id_vacuna_lista

# Endpoint POST para recibir un objeto del modelo Aplicacion y guardar la información en la base de datos
@app.route('/aplicacion', methods=['POST'])
def insertar_aplicacion():
    data = request.get_json()
    aplicacion = Aplicacion(
        curp=data['curp'],
        id_medico=data['id_medico'],
        id_esquema=data['id_esquema'],
        id_clues=data['id_clues'],
        dosis=data['dosis'],
        fecha_aplicacion=data['fecha_aplicacion'],
        num_dosis=data['num_dosis'],
        id_info_vacuna=data['id_info_vacuna'],
        id_brigada=data['id_brigada'],
        id_estatus=data['id_estatus'],
        id_vacuna_lista=data['id_vacuna_lista']
    )
    db.session.add(aplicacion)
    db.session.commit()
    return jsonify({'message': 'Aplicacion registrada exitosamente'}), 201

# Ejecución de la aplicación Flask
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=5021)

# JSON de prueba

# {
#     "curp": "LOCE980505HDFRRL02",
#     "id_medico": 1,
#     "id_esquema": 1,
#     "id_clues": 1,
#     "dosis": 1,
#     "fecha_aplicacion": "2024-12-11",
#     "num_dosis": 1,
#     "id_info_vacuna": 1,
#     "id_brigada": 1,
#     "id_estatus": 1,
#     "id_vacuna_lista": 1
# }