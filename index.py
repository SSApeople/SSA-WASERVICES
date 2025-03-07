from flask import Flask, request, jsonify
import requests
import json
from Functions import Operaciones
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template_string
from waitress import serve
import ssl


app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PMS2024@10.166.0.56/vacunacion_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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


# Token para verificar el webhook
VERIFY_TOKEN = "valkiria0813dj9-falken"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificación del webhook
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Token inválido", 403

    elif request.method == 'POST':
        data = request.json
        if data is not None:
            
            
            ### Bienvenida
            try:
                data_ref = data["entry"][0]["changes"][0]["value"]["messages"][0]
                _cp_ = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
                escp = Operaciones().es_codigo_postal(_cp_)
                if escp:
                    Operaciones().UbicaClinica(data_ref)
                    Operaciones().PreguntarSalida(data_ref)
                else:   
                    body = data_ref['text']['body']
                    if Operaciones().es_curp_valida(body):
                         Operaciones().VacunasAplicadas(data_ref)
                         Operaciones().VacunasNoAplicadas(data_ref)
                         Operaciones().quieresUbicar(data_ref)
                    else:
                        val_ =  Operaciones().EnviaBienvenida(data_ref)
                    return jsonify({"status": "bypass"}), 200
            except Exception as e:
                pass
            ### Campañas / Verificar Vacunas
            try:
                data_ref = data["entry"][0]["changes"][0]["value"]["messages"][0]
                button_reply_id = data_ref["interactive"]["button_reply"]["id"]
                if button_reply_id == "1":
                    val_ =  Operaciones().EnviaListaCampanas(data_ref)
                elif button_reply_id == "2":
                    val_ =  Operaciones().PideCurp(data_ref)
                elif button_reply_id == "ES":
                    val_ =  Operaciones().EnviasoloEfectosSecu(data_ref)
                elif button_reply_id == "SV":
                    val_ =  Operaciones().PideCP(data_ref)
                elif button_reply_id == "SiUbi":
                    val_ =  Operaciones().PideCP(data_ref)
                elif button_reply_id == "SiAy":
                    Operaciones().EnviaBienvenida(data_ref)
                elif button_reply_id == "NoAy":
                    Operaciones().Despedida(data_ref)
                elif button_reply_id == "NoUbi":
                    Operaciones().PreguntarSalida(data_ref)
            except Exception as e:
                pass
            ### Efectos Secundarios / codigo Postal
            try:
                TipoVacuna = Operaciones().IfExistTipoVacuna(data_ref)
                if TipoVacuna == "covid" or TipoVacuna == "influenza" or TipoVacuna == "vph" or TipoVacuna == "neumococo":
                    Operaciones().EnviaEfecSecundariosCP(data_ref)
                
                    
            except Exception as e:
                pass
        return jsonify({"status": "bypass"}), 200
            
            
            
@app.route('/aplicacion', methods=['POST'])
def aplicacion():
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

        
@app.route('/deploy', methods=['GET'])
def home():
    html_content = """
        
<div class='tableauPlaceholder' id='viz1735962539299' style='position: relative'>
  <noscript>
    <a href='#'>
      <img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;PO&#47;POC-SSAv4&#47;ProyeccinPoblacional&#47;1_rss.png' style='border: none' />
    </a>
  </noscript>
  <object class='tableauViz' style='display:none;'>
    <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
    <param name='embed_code_version' value='3' />
    <param name='site_root' value='' />
    <param name='name' value='POC-SSAv4&#47;ProyeccinPoblacional' />
    <param name='tabs' value='yes' />
    <param name='toolbar' value='yes' />
    <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;PO&#47;POC-SSAv4&#47;ProyeccinPoblacional&#47;1.png' />
    <param name='animate_transition' value='yes' />
    <param name='display_static_image' value='yes' />
    <param name='display_spinner' value='yes' />
    <param name='display_overlay' value='yes' />
    <param name='display_count' value='yes' />
    <param name='language' value='es-ES' />
  </object>
</div>
<script type='text/javascript'>
  var divElement = document.getElementById('viz1735962539299');
  var vizElement = divElement.getElementsByTagName('object')[0];
  if (divElement.offsetWidth > 800) {
    vizElement.style.width = '1300px';
    vizElement.style.height = '1550px';
  } else if (divElement.offsetWidth > 500) {
    vizElement.style.width = '1300px';
    vizElement.style.height = '1550px';
  } else {
    vizElement.style.minWidth = '1300px';
    vizElement.style.maxWidth = '100%';
    vizElement.style.height = '2900px';
  }
  var scriptElement = document.createElement('script');
  scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
  vizElement.parentNode.insertBefore(scriptElement, vizElement);


  document.onreadystatechange = function () {
    if (document.readyState === 'complete') {
	
        const elementos = document.querySelectorAll('.tableauViz');
        if (elementos.length > 0) {
            elementos[0].style.margin = 'auto';
					
        } else {
            console.warn('No se encontraron elementos con la clase .tableauViz.');
        }
    }
};


let interval = setInterval(function(){
     
	document.getElementsByClassName('tableauViz')[0].style.width = '1200px';
	document.getElementsByClassName('tableauViz')[0].style.margin = 'auto';
    document.getElementsByClassName('tableauPlaceholder')[0].style.width = '100%';
	
	if (document.getElementsByTagName('iframe').length > 0) {
	
		setTimeout(function(){ 
			clearInterval(interval);
		}, 14000);
		 
	} 
    console.log('...Censo...')    
}, 100);




</script>




    """
    return render_template_string(html_content)



@app.route('/rutas', methods=['GET'])
def Rutas():
    html_content = """
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Aduanas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
	 <link href="https://framework-gb.cdn.gob.mx/gm/v4/css/main.css" rel="stylesheet">
	<script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
  <style>
        #map {
            height: 500px;
        }
		.form-select {
			font-size: 2rem;
		}
    </style>
</head>
<body>
    <div class="container mt-4">
        <h2>Selección de Aduana</h2>
        <form>
            <div class="mb-3">
                <label for="aduana" class="form-label">Aduana</label>
                <select id="aduana" class="form-select" onchange="cargarDatosAduana()">
                    <option value="">Seleccione una aduana</option>
                </select>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <label for="latitud" class="form-label">Latitud</label>
                    <input type="text" id="latitud" class="form-control" readonly>
                </div>
                <div class="col-md-6">
                    <label for="longitud" class="form-label">Longitud</label>
                    <input type="text" id="longitud" class="form-control" readonly>
                </div>
            </div>
            <h3 class="mt-4">Transportes</h3>
            <div class="mb-3">
                <label for="transportes" class="form-label">Transporte</label>
                <select id="transportes" class="form-select" onchange="cargarDatosTransporte()">
                    <option value="">Seleccione un transporte</option>
                </select>
            </div>
            <div id="datos-transporte"></div>

            <h3 class="mt-4">Centros de Almacenamiento</h3>
            <div class="mb-3">
                <label for="centros" class="form-label">Centro de Almacenamiento</label>
                <select id="centros" class="form-select" onchange="cargarDatosCentro2();cargarDatosCentro();">
                    <option value="">Seleccione un centro</option>
                </select>
            </div>
			<div class="row">
    <div class="col-md-6">
        <label for="latitudCentro" class="form-label">Latitud</label>
        <input type="text" id="latitudCentro" class="form-control" readonly>
    </div>
    <div class="col-md-6">
        <label for="longitudCentro" class="form-label">Longitud</label>
        <input type="text" id="longitudCentro" class="form-control" readonly>
    </div>
</div>

<div class="row">
	<div class="col-md-6"></div>
	<div class="col-md-6 d-flex justify-content-end">
	<br>
        <button style="width: 20%;" type="button" class="btn btn-success" onclick="agregarCentro()">Agregar</button>
    </div>
</div>




            <div id="datos-centro"></div>
			
			
			
			<h3 class="mt-4">Lista de Centros de Almacenamiento</h3>
<table id = "tablaCentros" class="table table-bordered mt-3">
    <thead>
        <tr>
            <th>Centro de Almacenamiento</th>
            <th>Latitud</th>
            <th>Longitud</th>
            <th>Aduana de Procedencia</th>
        </tr>
    </thead>
    <tbody id="tablaCentros">
    </tbody>
</table>


      
        </form>
    </div>

    



<div class="row">

	<div class="col-md-1"></div>
	<div id="map" class="col-md-10"></div>
	<div class="col-md-1"></div>
</div>


    <script>
        const aduanas = JSON.parse('[{"nombre":"Acapulco","latitud":16.8524,"longitud":-99.8237,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":23,"temperatura_minima":-25.4,"temperatura_maxima":7.6,"empresa":"RefrigSafe","placa":"704-XYZ-990"},{"tipo":"Van refrigerada","capacidad_m3":11,"temperatura_minima":-22.2,"temperatura_maxima":6.3,"empresa":"TransVacunas","placa":"785-XYZ-825"},{"tipo":"Contenedor frigorífico","capacidad_m3":30,"temperatura_minima":1.9,"temperatura_maxima":5.5,"empresa":"FríoExpress","placa":"655-XYZ-659"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 34 Guerrero","latitud":16.77155,"longitud":-99.626841,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":28,"temperatura_minima":-5.1,"temperatura_maxima":7.7,"empresa":"FríoExpress","placa":"820-XYZ-521"},{"tipo":"Camión refrigerado","capacidad_m3":17,"temperatura_minima":-3.8,"temperatura_maxima":6.4,"empresa":"TransVacunas","placa":"662-XYZ-263"},{"tipo":"Van refrigerada","capacidad_m3":25,"temperatura_minima":-11.2,"temperatura_maxima":6.1,"empresa":"RefrigSafe","placa":"555-XYZ-909"}],"unidades_medicas":[{"nombre":"UMF 77 Guerrero","latitud":16.684476,"longitud":-99.586531},{"nombre":"UMF 78 Guerrero","latitud":16.771187,"longitud":-99.597857},{"nombre":"UMF 82 Guerrero","latitud":16.842199,"longitud":-99.531494},{"nombre":"UMF 11 Guerrero","latitud":16.845211,"longitud":-99.650727},{"nombre":"UMF 5 Guerrero","latitud":16.782328,"longitud":-99.694328},{"nombre":"UMF 30 Guerrero","latitud":16.723726,"longitud":-99.599493},{"nombre":"UMF 96 Guerrero","latitud":16.866786,"longitud":-99.710633},{"nombre":"UMF 89 Guerrero","latitud":16.860178,"longitud":-99.671233}]},{"nombre":"Centro de Almacenamiento 50 Guerrero","latitud":16.732835,"longitud":-99.663107,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":16,"temperatura_minima":-14.8,"temperatura_maxima":5.9,"empresa":"TransVacunas","placa":"772-XYZ-687"},{"tipo":"Camión refrigerado","capacidad_m3":25,"temperatura_minima":-11.5,"temperatura_maxima":2.4,"empresa":"FríoExpress","placa":"114-XYZ-695"},{"tipo":"Camión refrigerado","capacidad_m3":8,"temperatura_minima":-20.7,"temperatura_maxima":5.6,"empresa":"RefrigSafe","placa":"174-XYZ-510"}],"unidades_medicas":[{"nombre":"UMF 43 Guerrero","latitud":16.6908,"longitud":-99.671703},{"nombre":"UMF 3 Guerrero","latitud":16.776151,"longitud":-99.654051},{"nombre":"UMF 30 Guerrero","latitud":16.792686,"longitud":-99.566959},{"nombre":"UMF 48 Guerrero","latitud":16.672634,"longitud":-99.626864},{"nombre":"UMF 39 Guerrero","latitud":16.697664,"longitud":-99.681621},{"nombre":"UMF 48 Guerrero","latitud":16.765038,"longitud":-99.651548},{"nombre":"UMF 49 Guerrero","latitud":16.828233,"longitud":-99.665406},{"nombre":"UMF 12 Guerrero","latitud":16.6349,"longitud":-99.763057}]},{"nombre":"Centro de Almacenamiento 28 Guerrero","latitud":16.873987,"longitud":-99.669757,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":29,"temperatura_minima":-23.6,"temperatura_maxima":6.9,"empresa":"FríoExpress","placa":"511-XYZ-456"},{"tipo":"Contenedor frigorífico","capacidad_m3":21,"temperatura_minima":-4.2,"temperatura_maxima":5.6,"empresa":"RefrigSafe","placa":"356-XYZ-987"},{"tipo":"Contenedor frigorífico","capacidad_m3":8,"temperatura_minima":-14.2,"temperatura_maxima":5.9,"empresa":"FríoExpress","placa":"492-XYZ-252"}],"unidades_medicas":[{"nombre":"UMF 86 Guerrero","latitud":16.874213,"longitud":-99.636552},{"nombre":"UMF 15 Guerrero","latitud":16.831286,"longitud":-99.632068},{"nombre":"UMF 87 Guerrero","latitud":16.876068,"longitud":-99.725618},{"nombre":"UMF 60 Guerrero","latitud":16.973272,"longitud":-99.668816},{"nombre":"UMF 44 Guerrero","latitud":16.92979,"longitud":-99.71699},{"nombre":"UMF 70 Guerrero","latitud":16.888942,"longitud":-99.717464},{"nombre":"UMF 65 Guerrero","latitud":16.962752,"longitud":-99.624118},{"nombre":"UMF 98 Guerrero","latitud":16.944104,"longitud":-99.65416}]}]},{"nombre":"Altamira","latitud":22.3916,"longitud":-97.9234,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":24,"temperatura_minima":-16.5,"temperatura_maxima":7.9,"empresa":"FríoExpress","placa":"335-XYZ-332"},{"tipo":"Van refrigerada","capacidad_m3":27,"temperatura_minima":1,"temperatura_maxima":4.8,"empresa":"TransVacunas","placa":"497-XYZ-719"},{"tipo":"Camión refrigerado","capacidad_m3":7,"temperatura_minima":-25.2,"temperatura_maxima":5.2,"empresa":"RefrigSafe","placa":"473-XYZ-235"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 19 Tamaulipas","latitud":22.285199,"longitud":-98.108769,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":18,"temperatura_minima":-16.2,"temperatura_maxima":4.9,"empresa":"RefrigSafe","placa":"530-XYZ-761"},{"tipo":"Van refrigerada","capacidad_m3":8,"temperatura_minima":-23.3,"temperatura_maxima":7.4,"empresa":"RefrigSafe","placa":"683-XYZ-613"},{"tipo":"Contenedor frigorífico","capacidad_m3":26,"temperatura_minima":-29.6,"temperatura_maxima":3.8,"empresa":"TransVacunas","placa":"134-XYZ-877"}],"unidades_medicas":[{"nombre":"UMF 72 Tamaulipas","latitud":22.306762,"longitud":-98.142509},{"nombre":"UMF 97 Tamaulipas","latitud":22.337034,"longitud":-98.019995},{"nombre":"UMF 49 Tamaulipas","latitud":22.339938,"longitud":-98.085834},{"nombre":"UMF 66 Tamaulipas","latitud":22.371086,"longitud":-98.204843},{"nombre":"UMF 43 Tamaulipas","latitud":22.23494,"longitud":-98.087392},{"nombre":"UMF 18 Tamaulipas","latitud":22.238689,"longitud":-98.023934},{"nombre":"UMF 41 Tamaulipas","latitud":22.263149,"longitud":-98.134523},{"nombre":"UMF 81 Tamaulipas","latitud":22.361053,"longitud":-98.05403}]},{"nombre":"Centro de Almacenamiento 25 Tamaulipas","latitud":22.34905,"longitud":-97.880692,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":23,"temperatura_minima":-8,"temperatura_maxima":5.1,"empresa":"TransVacunas","placa":"822-XYZ-819"},{"tipo":"Contenedor frigorífico","capacidad_m3":15,"temperatura_minima":-8.8,"temperatura_maxima":4.2,"empresa":"RefrigSafe","placa":"210-XYZ-963"},{"tipo":"Contenedor frigorífico","capacidad_m3":26,"temperatura_minima":-0.4,"temperatura_maxima":4.5,"empresa":"RefrigSafe","placa":"768-XYZ-285"}],"unidades_medicas":[{"nombre":"UMF 55 Tamaulipas","latitud":22.394344,"longitud":-97.931925},{"nombre":"UMF 62 Tamaulipas","latitud":22.307263,"longitud":-97.883251},{"nombre":"UMF 83 Tamaulipas","latitud":22.371921,"longitud":-97.828433},{"nombre":"UMF 50 Tamaulipas","latitud":22.252251,"longitud":-97.887951},{"nombre":"UMF 39 Tamaulipas","latitud":22.409112,"longitud":-97.877633},{"nombre":"UMF 37 Tamaulipas","latitud":22.268739,"longitud":-97.793203},{"nombre":"UMF 60 Tamaulipas","latitud":22.430052,"longitud":-97.803222},{"nombre":"UMF 6 Tamaulipas","latitud":22.249774,"longitud":-97.827519}]},{"nombre":"Centro de Almacenamiento 39 Tamaulipas","latitud":22.506847,"longitud":-97.880334,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":10,"temperatura_minima":-6.7,"temperatura_maxima":4.8,"empresa":"TransVacunas","placa":"781-XYZ-349"},{"tipo":"Camión refrigerado","capacidad_m3":22,"temperatura_minima":-1.4,"temperatura_maxima":2.8,"empresa":"RefrigSafe","placa":"758-XYZ-597"},{"tipo":"Van refrigerada","capacidad_m3":27,"temperatura_minima":-19.1,"temperatura_maxima":6,"empresa":"FríoExpress","placa":"793-XYZ-127"}],"unidades_medicas":[{"nombre":"UMF 51 Tamaulipas","latitud":22.557644,"longitud":-97.802877},{"nombre":"UMF 63 Tamaulipas","latitud":22.506093,"longitud":-97.86631},{"nombre":"UMF 10 Tamaulipas","latitud":22.587194,"longitud":-97.814929},{"nombre":"UMF 73 Tamaulipas","latitud":22.488361,"longitud":-97.8501},{"nombre":"UMF 60 Tamaulipas","latitud":22.480537,"longitud":-97.795241},{"nombre":"UMF 40 Tamaulipas","latitud":22.413411,"longitud":-97.891857},{"nombre":"UMF 77 Tamaulipas","latitud":22.538024,"longitud":-97.966572},{"nombre":"UMF 79 Tamaulipas","latitud":22.535433,"longitud":-97.874392}]}]},{"nombre":"Coatzacoalcos","latitud":18.1335,"longitud":-94.4427,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":5,"temperatura_minima":-11,"temperatura_maxima":7.1,"empresa":"FríoExpress","placa":"115-XYZ-384"},{"tipo":"Camión refrigerado","capacidad_m3":11,"temperatura_minima":1.9,"temperatura_maxima":7,"empresa":"RefrigSafe","placa":"422-XYZ-214"},{"tipo":"Contenedor frigorífico","capacidad_m3":22,"temperatura_minima":-4.7,"temperatura_maxima":5.5,"empresa":"FríoExpress","placa":"134-XYZ-915"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 1 Veracruz","latitud":18.311715,"longitud":-94.612418,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":15,"temperatura_minima":-18.4,"temperatura_maxima":7.9,"empresa":"RefrigSafe","placa":"423-XYZ-613"},{"tipo":"Contenedor frigorífico","capacidad_m3":20,"temperatura_minima":-27.4,"temperatura_maxima":5,"empresa":"TransVacunas","placa":"620-XYZ-233"},{"tipo":"Contenedor frigorífico","capacidad_m3":8,"temperatura_minima":-5.7,"temperatura_maxima":5.3,"empresa":"RefrigSafe","placa":"939-XYZ-797"}],"unidades_medicas":[{"nombre":"UMF 95 Veracruz","latitud":18.363299,"longitud":-94.643837},{"nombre":"UMF 22 Veracruz","latitud":18.320221,"longitud":-94.638112},{"nombre":"UMF 78 Veracruz","latitud":18.282757,"longitud":-94.617692},{"nombre":"UMF 83 Veracruz","latitud":18.388945,"longitud":-94.561704},{"nombre":"UMF 78 Veracruz","latitud":18.299189,"longitud":-94.654003},{"nombre":"UMF 37 Veracruz","latitud":18.248754,"longitud":-94.650567},{"nombre":"UMF 37 Veracruz","latitud":18.218724,"longitud":-94.550935},{"nombre":"UMF 10 Veracruz","latitud":18.256629,"longitud":-94.58385}]},{"nombre":"Centro de Almacenamiento 28 Veracruz","latitud":18.278908,"longitud":-94.312599,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":8,"temperatura_minima":-2.3,"temperatura_maxima":2.9,"empresa":"TransVacunas","placa":"999-XYZ-426"},{"tipo":"Camión refrigerado","capacidad_m3":24,"temperatura_minima":-0.8,"temperatura_maxima":5.9,"empresa":"RefrigSafe","placa":"709-XYZ-918"},{"tipo":"Van refrigerada","capacidad_m3":10,"temperatura_minima":-24.6,"temperatura_maxima":2.9,"empresa":"FríoExpress","placa":"182-XYZ-915"}],"unidades_medicas":[{"nombre":"UMF 42 Veracruz","latitud":18.284865,"longitud":-94.287687},{"nombre":"UMF 21 Veracruz","latitud":18.269157,"longitud":-94.385706},{"nombre":"UMF 47 Veracruz","latitud":18.315433,"longitud":-94.228638},{"nombre":"UMF 56 Veracruz","latitud":18.227474,"longitud":-94.305371},{"nombre":"UMF 65 Veracruz","latitud":18.333511,"longitud":-94.217034},{"nombre":"UMF 54 Veracruz","latitud":18.218465,"longitud":-94.221231},{"nombre":"UMF 5 Veracruz","latitud":18.239163,"longitud":-94.379011},{"nombre":"UMF 100 Veracruz","latitud":18.278195,"longitud":-94.281162}]},{"nombre":"Centro de Almacenamiento 48 Veracruz","latitud":17.961323,"longitud":-94.531777,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":8,"temperatura_minima":-15.3,"temperatura_maxima":4.4,"empresa":"RefrigSafe","placa":"605-XYZ-830"},{"tipo":"Van refrigerada","capacidad_m3":19,"temperatura_minima":-18.3,"temperatura_maxima":7.4,"empresa":"RefrigSafe","placa":"340-XYZ-607"},{"tipo":"Camión refrigerado","capacidad_m3":19,"temperatura_minima":-17.3,"temperatura_maxima":5.7,"empresa":"RefrigSafe","placa":"366-XYZ-215"}],"unidades_medicas":[{"nombre":"UMF 91 Veracruz","latitud":17.956877,"longitud":-94.533872},{"nombre":"UMF 18 Veracruz","latitud":17.941054,"longitud":-94.521838},{"nombre":"UMF 20 Veracruz","latitud":17.881262,"longitud":-94.454941},{"nombre":"UMF 35 Veracruz","latitud":17.902648,"longitud":-94.618184},{"nombre":"UMF 27 Veracruz","latitud":18.050708,"longitud":-94.434484},{"nombre":"UMF 71 Veracruz","latitud":17.898069,"longitud":-94.585493},{"nombre":"UMF 78 Veracruz","latitud":18.004166,"longitud":-94.597097},{"nombre":"UMF 63 Veracruz","latitud":17.907024,"longitud":-94.539506}]}]},{"nombre":"La Paz","latitud":24.1426,"longitud":-110.3128,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":6,"temperatura_minima":-14.7,"temperatura_maxima":7.3,"empresa":"FríoExpress","placa":"367-XYZ-211"},{"tipo":"Van refrigerada","capacidad_m3":17,"temperatura_minima":-19,"temperatura_maxima":6.9,"empresa":"RefrigSafe","placa":"533-XYZ-761"},{"tipo":"Contenedor frigorífico","capacidad_m3":23,"temperatura_minima":-3,"temperatura_maxima":4.1,"empresa":"RefrigSafe","placa":"431-XYZ-510"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 35 Baja California Sur","latitud":24.333236,"longitud":-110.155717,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":16,"temperatura_minima":-25.3,"temperatura_maxima":5.9,"empresa":"RefrigSafe","placa":"692-XYZ-584"},{"tipo":"Camión refrigerado","capacidad_m3":30,"temperatura_minima":-19.6,"temperatura_maxima":6.6,"empresa":"TransVacunas","placa":"345-XYZ-799"},{"tipo":"Contenedor frigorífico","capacidad_m3":13,"temperatura_minima":-15.7,"temperatura_maxima":3.6,"empresa":"FríoExpress","placa":"737-XYZ-915"}],"unidades_medicas":[{"nombre":"UMF 69 Baja California Sur","latitud":24.371617,"longitud":-110.159564},{"nombre":"UMF 7 Baja California Sur","latitud":24.28622,"longitud":-110.116375},{"nombre":"UMF 29 Baja California Sur","latitud":24.430015,"longitud":-110.254854},{"nombre":"UMF 82 Baja California Sur","latitud":24.236996,"longitud":-110.195931},{"nombre":"UMF 17 Baja California Sur","latitud":24.401446,"longitud":-110.235693},{"nombre":"UMF 46 Baja California Sur","latitud":24.36,"longitud":-110.210802},{"nombre":"UMF 80 Baja California Sur","latitud":24.414332,"longitud":-110.255532},{"nombre":"UMF 7 Baja California Sur","latitud":24.313197,"longitud":-110.162352}]},{"nombre":"Centro de Almacenamiento 45 Baja California Sur","latitud":24.094795,"longitud":-110.467836,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":26,"temperatura_minima":0.1,"temperatura_maxima":2.5,"empresa":"TransVacunas","placa":"358-XYZ-232"},{"tipo":"Camión refrigerado","capacidad_m3":11,"temperatura_minima":1,"temperatura_maxima":2.3,"empresa":"TransVacunas","placa":"285-XYZ-282"},{"tipo":"Camión refrigerado","capacidad_m3":14,"temperatura_minima":-4.8,"temperatura_maxima":4.2,"empresa":"TransVacunas","placa":"928-XYZ-252"}],"unidades_medicas":[{"nombre":"UMF 9 Baja California Sur","latitud":24.170857,"longitud":-110.369716},{"nombre":"UMF 89 Baja California Sur","latitud":24.135293,"longitud":-110.500898},{"nombre":"UMF 57 Baja California Sur","latitud":24.118143,"longitud":-110.437085},{"nombre":"UMF 55 Baja California Sur","latitud":24.157385,"longitud":-110.467316},{"nombre":"UMF 37 Baja California Sur","latitud":23.995958,"longitud":-110.405215},{"nombre":"UMF 2 Baja California Sur","latitud":24.090407,"longitud":-110.567402},{"nombre":"UMF 40 Baja California Sur","latitud":24.042711,"longitud":-110.464524},{"nombre":"UMF 82 Baja California Sur","latitud":24.002009,"longitud":-110.496403}]},{"nombre":"Centro de Almacenamiento 28 Baja California Sur","latitud":24.160553,"longitud":-110.431053,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":5,"temperatura_minima":-27.3,"temperatura_maxima":7.1,"empresa":"FríoExpress","placa":"823-XYZ-849"},{"tipo":"Camión refrigerado","capacidad_m3":28,"temperatura_minima":-27.2,"temperatura_maxima":2,"empresa":"TransVacunas","placa":"572-XYZ-594"},{"tipo":"Contenedor frigorífico","capacidad_m3":24,"temperatura_minima":-3.8,"temperatura_maxima":6.1,"empresa":"TransVacunas","placa":"455-XYZ-762"}],"unidades_medicas":[{"nombre":"UMF 29 Baja California Sur","latitud":24.082791,"longitud":-110.453424},{"nombre":"UMF 80 Baja California Sur","latitud":24.184725,"longitud":-110.505656},{"nombre":"UMF 45 Baja California Sur","latitud":24.099457,"longitud":-110.508891},{"nombre":"UMF 24 Baja California Sur","latitud":24.205977,"longitud":-110.503035},{"nombre":"UMF 22 Baja California Sur","latitud":24.104449,"longitud":-110.35207},{"nombre":"UMF 69 Baja California Sur","latitud":24.071082,"longitud":-110.439947},{"nombre":"UMF 53 Baja California Sur","latitud":24.255615,"longitud":-110.371305},{"nombre":"UMF 32 Baja California Sur","latitud":24.184483,"longitud":-110.352422}]}]},{"nombre":"Lázaro Cárdenas","latitud":17.9561,"longitud":-102.1941,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":16,"temperatura_minima":-4.2,"temperatura_maxima":2.5,"empresa":"RefrigSafe","placa":"967-XYZ-203"},{"tipo":"Van refrigerada","capacidad_m3":15,"temperatura_minima":-13.9,"temperatura_maxima":5.2,"empresa":"RefrigSafe","placa":"230-XYZ-273"},{"tipo":"Contenedor frigorífico","capacidad_m3":19,"temperatura_minima":-15.4,"temperatura_maxima":3.9,"empresa":"FríoExpress","placa":"744-XYZ-130"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 23 Michoacán","latitud":17.785161,"longitud":-102.218831,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":21,"temperatura_minima":-0.9,"temperatura_maxima":7.8,"empresa":"RefrigSafe","placa":"189-XYZ-281"},{"tipo":"Camión refrigerado","capacidad_m3":13,"temperatura_minima":-3,"temperatura_maxima":6.9,"empresa":"FríoExpress","placa":"233-XYZ-583"},{"tipo":"Camión refrigerado","capacidad_m3":8,"temperatura_minima":-1.8,"temperatura_maxima":4.8,"empresa":"TransVacunas","placa":"271-XYZ-626"}],"unidades_medicas":[{"nombre":"UMF 9 Michoacán","latitud":17.733028,"longitud":-102.236384},{"nombre":"UMF 94 Michoacán","latitud":17.74093,"longitud":-102.199331},{"nombre":"UMF 19 Michoacán","latitud":17.828251,"longitud":-102.201589},{"nombre":"UMF 35 Michoacán","latitud":17.820835,"longitud":-102.231325},{"nombre":"UMF 50 Michoacán","latitud":17.728305,"longitud":-102.228212},{"nombre":"UMF 24 Michoacán","latitud":17.805624,"longitud":-102.318125},{"nombre":"UMF 70 Michoacán","latitud":17.691601,"longitud":-102.14767},{"nombre":"UMF 98 Michoacán","latitud":17.792376,"longitud":-102.143086}]},{"nombre":"Centro de Almacenamiento 15 Michoacán","latitud":17.834898,"longitud":-102.160103,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":14,"temperatura_minima":-25.1,"temperatura_maxima":7.1,"empresa":"TransVacunas","placa":"997-XYZ-466"},{"tipo":"Camión refrigerado","capacidad_m3":9,"temperatura_minima":-24.4,"temperatura_maxima":3.5,"empresa":"FríoExpress","placa":"985-XYZ-216"},{"tipo":"Van refrigerada","capacidad_m3":16,"temperatura_minima":-14.8,"temperatura_maxima":4,"empresa":"RefrigSafe","placa":"186-XYZ-178"}],"unidades_medicas":[{"nombre":"UMF 50 Michoacán","latitud":17.798094,"longitud":-102.236744},{"nombre":"UMF 68 Michoacán","latitud":17.869172,"longitud":-102.23467},{"nombre":"UMF 66 Michoacán","latitud":17.918822,"longitud":-102.144703},{"nombre":"UMF 65 Michoacán","latitud":17.807856,"longitud":-102.06252},{"nombre":"UMF 34 Michoacán","latitud":17.801786,"longitud":-102.065382},{"nombre":"UMF 15 Michoacán","latitud":17.914143,"longitud":-102.186263},{"nombre":"UMF 98 Michoacán","latitud":17.805897,"longitud":-102.120297},{"nombre":"UMF 23 Michoacán","latitud":17.849417,"longitud":-102.210934}]},{"nombre":"Centro de Almacenamiento 2 Michoacán","latitud":17.832454,"longitud":-102.239573,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":28,"temperatura_minima":-29.1,"temperatura_maxima":2.8,"empresa":"TransVacunas","placa":"165-XYZ-560"},{"tipo":"Van refrigerada","capacidad_m3":17,"temperatura_minima":-6,"temperatura_maxima":6,"empresa":"RefrigSafe","placa":"360-XYZ-530"},{"tipo":"Contenedor frigorífico","capacidad_m3":20,"temperatura_minima":0.2,"temperatura_maxima":4.7,"empresa":"RefrigSafe","placa":"167-XYZ-802"}],"unidades_medicas":[{"nombre":"UMF 10 Michoacán","latitud":17.783914,"longitud":-102.147161},{"nombre":"UMF 12 Michoacán","latitud":17.881138,"longitud":-102.336986},{"nombre":"UMF 34 Michoacán","latitud":17.807412,"longitud":-102.306333},{"nombre":"UMF 69 Michoacán","latitud":17.895976,"longitud":-102.176174},{"nombre":"UMF 49 Michoacán","latitud":17.879665,"longitud":-102.338506},{"nombre":"UMF 19 Michoacán","latitud":17.761866,"longitud":-102.228505},{"nombre":"UMF 20 Michoacán","latitud":17.853108,"longitud":-102.339558},{"nombre":"UMF 36 Michoacán","latitud":17.87465,"longitud":-102.218425}]}]},{"nombre":"Manzanillo","latitud":19.052,"longitud":-104.3188,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":9,"temperatura_minima":-14.7,"temperatura_maxima":6.2,"empresa":"RefrigSafe","placa":"352-XYZ-501"},{"tipo":"Camión refrigerado","capacidad_m3":8,"temperatura_minima":-25.2,"temperatura_maxima":4.1,"empresa":"TransVacunas","placa":"101-XYZ-734"},{"tipo":"Van refrigerada","capacidad_m3":24,"temperatura_minima":-26.8,"temperatura_maxima":4.7,"empresa":"RefrigSafe","placa":"683-XYZ-708"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 44 Colima","latitud":18.93577,"longitud":-104.221167,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":6,"temperatura_minima":-17.9,"temperatura_maxima":4,"empresa":"TransVacunas","placa":"977-XYZ-670"},{"tipo":"Camión refrigerado","capacidad_m3":9,"temperatura_minima":-22.6,"temperatura_maxima":5.3,"empresa":"RefrigSafe","placa":"929-XYZ-980"},{"tipo":"Camión refrigerado","capacidad_m3":26,"temperatura_minima":-5.1,"temperatura_maxima":4.1,"empresa":"RefrigSafe","placa":"453-XYZ-454"}],"unidades_medicas":[{"nombre":"UMF 85 Colima","latitud":18.959157,"longitud":-104.292952},{"nombre":"UMF 72 Colima","latitud":19.017312,"longitud":-104.220378},{"nombre":"UMF 6 Colima","latitud":18.935029,"longitud":-104.213484},{"nombre":"UMF 58 Colima","latitud":18.86314,"longitud":-104.125184},{"nombre":"UMF 45 Colima","latitud":18.852501,"longitud":-104.15015},{"nombre":"UMF 16 Colima","latitud":18.861068,"longitud":-104.267367},{"nombre":"UMF 19 Colima","latitud":18.951183,"longitud":-104.279438},{"nombre":"UMF 68 Colima","latitud":18.847554,"longitud":-104.203119}]},{"nombre":"Centro de Almacenamiento 45 Colima","latitud":19.059253,"longitud":-104.305609,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":12,"temperatura_minima":-26.9,"temperatura_maxima":4.8,"empresa":"FríoExpress","placa":"684-XYZ-794"},{"tipo":"Van refrigerada","capacidad_m3":26,"temperatura_minima":-5.8,"temperatura_maxima":2,"empresa":"TransVacunas","placa":"852-XYZ-978"},{"tipo":"Van refrigerada","capacidad_m3":7,"temperatura_minima":-1.7,"temperatura_maxima":3.7,"empresa":"RefrigSafe","placa":"727-XYZ-527"}],"unidades_medicas":[{"nombre":"UMF 52 Colima","latitud":18.99603,"longitud":-104.281484},{"nombre":"UMF 74 Colima","latitud":19.063286,"longitud":-104.382782},{"nombre":"UMF 59 Colima","latitud":19.044374,"longitud":-104.208624},{"nombre":"UMF 51 Colima","latitud":19.146551,"longitud":-104.290134},{"nombre":"UMF 100 Colima","latitud":19.14936,"longitud":-104.297286},{"nombre":"UMF 12 Colima","latitud":19.113461,"longitud":-104.307947},{"nombre":"UMF 50 Colima","latitud":19.020148,"longitud":-104.242147},{"nombre":"UMF 6 Colima","latitud":19.083276,"longitud":-104.271772}]},{"nombre":"Centro de Almacenamiento 8 Colima","latitud":19.034435,"longitud":-104.277459,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":9,"temperatura_minima":-4.2,"temperatura_maxima":3.2,"empresa":"TransVacunas","placa":"594-XYZ-954"},{"tipo":"Van refrigerada","capacidad_m3":5,"temperatura_minima":-10.3,"temperatura_maxima":2.5,"empresa":"TransVacunas","placa":"521-XYZ-739"},{"tipo":"Contenedor frigorífico","capacidad_m3":28,"temperatura_minima":-14.8,"temperatura_maxima":3.6,"empresa":"RefrigSafe","placa":"273-XYZ-245"}],"unidades_medicas":[{"nombre":"UMF 30 Colima","latitud":19.009116,"longitud":-104.351739},{"nombre":"UMF 95 Colima","latitud":19.070509,"longitud":-104.331006},{"nombre":"UMF 23 Colima","latitud":18.9495,"longitud":-104.34425},{"nombre":"UMF 88 Colima","latitud":19.019363,"longitud":-104.298926},{"nombre":"UMF 1 Colima","latitud":19.037171,"longitud":-104.233555},{"nombre":"UMF 77 Colima","latitud":18.979322,"longitud":-104.332605},{"nombre":"UMF 44 Colima","latitud":18.936689,"longitud":-104.306724},{"nombre":"UMF 8 Colima","latitud":19.119979,"longitud":-104.199426}]}]},{"nombre":"Mazatlán","latitud":23.2494,"longitud":-106.4111,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":10,"temperatura_minima":-23.8,"temperatura_maxima":2.5,"empresa":"TransVacunas","placa":"670-XYZ-577"},{"tipo":"Contenedor frigorífico","capacidad_m3":16,"temperatura_minima":-2.3,"temperatura_maxima":4.8,"empresa":"FríoExpress","placa":"645-XYZ-994"},{"tipo":"Camión refrigerado","capacidad_m3":22,"temperatura_minima":-23.6,"temperatura_maxima":7.3,"empresa":"RefrigSafe","placa":"433-XYZ-726"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 31 Sinaloa","latitud":23.310737,"longitud":-106.278014,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":23,"temperatura_minima":-1.2,"temperatura_maxima":6.3,"empresa":"FríoExpress","placa":"979-XYZ-450"},{"tipo":"Camión refrigerado","capacidad_m3":9,"temperatura_minima":-0.4,"temperatura_maxima":2.7,"empresa":"TransVacunas","placa":"190-XYZ-784"},{"tipo":"Van refrigerada","capacidad_m3":8,"temperatura_minima":-23,"temperatura_maxima":2.7,"empresa":"RefrigSafe","placa":"435-XYZ-607"}],"unidades_medicas":[{"nombre":"UMF 2 Sinaloa","latitud":23.325605,"longitud":-106.376709},{"nombre":"UMF 28 Sinaloa","latitud":23.350157,"longitud":-106.341649},{"nombre":"UMF 9 Sinaloa","latitud":23.221159,"longitud":-106.245551},{"nombre":"UMF 64 Sinaloa","latitud":23.263346,"longitud":-106.229027},{"nombre":"UMF 65 Sinaloa","latitud":23.337096,"longitud":-106.232502},{"nombre":"UMF 59 Sinaloa","latitud":23.368858,"longitud":-106.349806},{"nombre":"UMF 49 Sinaloa","latitud":23.309802,"longitud":-106.341796},{"nombre":"UMF 31 Sinaloa","latitud":23.374289,"longitud":-106.232382}]},{"nombre":"Centro de Almacenamiento 42 Sinaloa","latitud":23.258903,"longitud":-106.44688,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":28,"temperatura_minima":1,"temperatura_maxima":8,"empresa":"TransVacunas","placa":"545-XYZ-922"},{"tipo":"Camión refrigerado","capacidad_m3":5,"temperatura_minima":-14.7,"temperatura_maxima":2.8,"empresa":"FríoExpress","placa":"498-XYZ-847"},{"tipo":"Van refrigerada","capacidad_m3":22,"temperatura_minima":-6,"temperatura_maxima":3.4,"empresa":"RefrigSafe","placa":"972-XYZ-335"}],"unidades_medicas":[{"nombre":"UMF 98 Sinaloa","latitud":23.301128,"longitud":-106.385027},{"nombre":"UMF 98 Sinaloa","latitud":23.33477,"longitud":-106.444936},{"nombre":"UMF 92 Sinaloa","latitud":23.160131,"longitud":-106.463204},{"nombre":"UMF 74 Sinaloa","latitud":23.167946,"longitud":-106.499826},{"nombre":"UMF 28 Sinaloa","latitud":23.194125,"longitud":-106.40644},{"nombre":"UMF 77 Sinaloa","latitud":23.340164,"longitud":-106.377983},{"nombre":"UMF 81 Sinaloa","latitud":23.236591,"longitud":-106.520387},{"nombre":"UMF 13 Sinaloa","latitud":23.305912,"longitud":-106.350963}]},{"nombre":"Centro de Almacenamiento 49 Sinaloa","latitud":23.348936,"longitud":-106.600138,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":13,"temperatura_minima":-28,"temperatura_maxima":7.6,"empresa":"TransVacunas","placa":"876-XYZ-855"},{"tipo":"Van refrigerada","capacidad_m3":27,"temperatura_minima":-14.6,"temperatura_maxima":2.6,"empresa":"FríoExpress","placa":"323-XYZ-391"},{"tipo":"Contenedor frigorífico","capacidad_m3":27,"temperatura_minima":-22.7,"temperatura_maxima":6.7,"empresa":"FríoExpress","placa":"223-XYZ-455"}],"unidades_medicas":[{"nombre":"UMF 1 Sinaloa","latitud":23.261968,"longitud":-106.653538},{"nombre":"UMF 8 Sinaloa","latitud":23.364831,"longitud":-106.582324},{"nombre":"UMF 90 Sinaloa","latitud":23.331257,"longitud":-106.543923},{"nombre":"UMF 17 Sinaloa","latitud":23.266885,"longitud":-106.681159},{"nombre":"UMF 8 Sinaloa","latitud":23.346466,"longitud":-106.639292},{"nombre":"UMF 11 Sinaloa","latitud":23.343301,"longitud":-106.533448},{"nombre":"UMF 13 Sinaloa","latitud":23.401105,"longitud":-106.685287},{"nombre":"UMF 4 Sinaloa","latitud":23.428902,"longitud":-106.609308}]}]},{"nombre":"Progreso","latitud":21.2783,"longitud":-89.6641,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":12,"temperatura_minima":-9.5,"temperatura_maxima":3.4,"empresa":"RefrigSafe","placa":"736-XYZ-345"},{"tipo":"Van refrigerada","capacidad_m3":29,"temperatura_minima":-27.6,"temperatura_maxima":4.2,"empresa":"FríoExpress","placa":"828-XYZ-950"},{"tipo":"Camión refrigerado","capacidad_m3":19,"temperatura_minima":-5.5,"temperatura_maxima":4.9,"empresa":"RefrigSafe","placa":"401-XYZ-544"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 10 Yucatán","latitud":21.136916,"longitud":-89.847542,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":19,"temperatura_minima":-13.6,"temperatura_maxima":3.6,"empresa":"TransVacunas","placa":"640-XYZ-323"},{"tipo":"Van refrigerada","capacidad_m3":10,"temperatura_minima":-19,"temperatura_maxima":4.9,"empresa":"FríoExpress","placa":"948-XYZ-184"},{"tipo":"Contenedor frigorífico","capacidad_m3":16,"temperatura_minima":-0.8,"temperatura_maxima":3.7,"empresa":"RefrigSafe","placa":"506-XYZ-877"}],"unidades_medicas":[{"nombre":"UMF 59 Yucatán","latitud":21.053071,"longitud":-89.83268},{"nombre":"UMF 15 Yucatán","latitud":21.044058,"longitud":-89.822487},{"nombre":"UMF 28 Yucatán","latitud":21.18474,"longitud":-89.79563},{"nombre":"UMF 70 Yucatán","latitud":21.235095,"longitud":-89.827739},{"nombre":"UMF 7 Yucatán","latitud":21.059694,"longitud":-89.920515},{"nombre":"UMF 27 Yucatán","latitud":21.073351,"longitud":-89.842224},{"nombre":"UMF 3 Yucatán","latitud":21.093817,"longitud":-89.790243},{"nombre":"UMF 23 Yucatán","latitud":21.179934,"longitud":-89.858475}]},{"nombre":"Centro de Almacenamiento 42 Yucatán","latitud":21.236999,"longitud":-89.586492,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":13,"temperatura_minima":-27.2,"temperatura_maxima":6.2,"empresa":"RefrigSafe","placa":"322-XYZ-890"},{"tipo":"Contenedor frigorífico","capacidad_m3":24,"temperatura_minima":-22.9,"temperatura_maxima":5.6,"empresa":"FríoExpress","placa":"973-XYZ-202"},{"tipo":"Van refrigerada","capacidad_m3":28,"temperatura_minima":-20.6,"temperatura_maxima":5.3,"empresa":"TransVacunas","placa":"182-XYZ-691"}],"unidades_medicas":[{"nombre":"UMF 38 Yucatán","latitud":21.298186,"longitud":-89.660915},{"nombre":"UMF 89 Yucatán","latitud":21.335918,"longitud":-89.671629},{"nombre":"UMF 76 Yucatán","latitud":21.22901,"longitud":-89.600266},{"nombre":"UMF 40 Yucatán","latitud":21.188924,"longitud":-89.548979},{"nombre":"UMF 4 Yucatán","latitud":21.230589,"longitud":-89.533552},{"nombre":"UMF 38 Yucatán","latitud":21.328701,"longitud":-89.609597},{"nombre":"UMF 10 Yucatán","latitud":21.239422,"longitud":-89.521216},{"nombre":"UMF 77 Yucatán","latitud":21.214194,"longitud":-89.520234}]},{"nombre":"Centro de Almacenamiento 19 Yucatán","latitud":21.339916,"longitud":-89.788191,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":13,"temperatura_minima":-1.7,"temperatura_maxima":4.5,"empresa":"TransVacunas","placa":"369-XYZ-878"},{"tipo":"Contenedor frigorífico","capacidad_m3":26,"temperatura_minima":-25.6,"temperatura_maxima":4.1,"empresa":"FríoExpress","placa":"978-XYZ-753"},{"tipo":"Contenedor frigorífico","capacidad_m3":14,"temperatura_minima":-28.3,"temperatura_maxima":6.5,"empresa":"RefrigSafe","placa":"776-XYZ-439"}],"unidades_medicas":[{"nombre":"UMF 76 Yucatán","latitud":21.248084,"longitud":-89.755717},{"nombre":"UMF 86 Yucatán","latitud":21.266691,"longitud":-89.870903},{"nombre":"UMF 63 Yucatán","latitud":21.35216,"longitud":-89.832289},{"nombre":"UMF 63 Yucatán","latitud":21.299671,"longitud":-89.780516},{"nombre":"UMF 39 Yucatán","latitud":21.242896,"longitud":-89.80795},{"nombre":"UMF 50 Yucatán","latitud":21.33795,"longitud":-89.713196},{"nombre":"UMF 84 Yucatán","latitud":21.370575,"longitud":-89.779778},{"nombre":"UMF 21 Yucatán","latitud":21.283318,"longitud":-89.762202}]}]},{"nombre":"Salina Cruz","latitud":16.1793,"longitud":-95.1981,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":19,"temperatura_minima":-30,"temperatura_maxima":3.4,"empresa":"TransVacunas","placa":"199-XYZ-296"},{"tipo":"Camión refrigerado","capacidad_m3":18,"temperatura_minima":-19.3,"temperatura_maxima":5.6,"empresa":"RefrigSafe","placa":"629-XYZ-162"},{"tipo":"Contenedor frigorífico","capacidad_m3":12,"temperatura_minima":-3.7,"temperatura_maxima":6.4,"empresa":"TransVacunas","placa":"673-XYZ-172"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 12 Oaxaca","latitud":16.042769,"longitud":-95.093178,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":21,"temperatura_minima":0,"temperatura_maxima":6.2,"empresa":"RefrigSafe","placa":"318-XYZ-683"},{"tipo":"Van refrigerada","capacidad_m3":14,"temperatura_minima":-27.5,"temperatura_maxima":6.9,"empresa":"FríoExpress","placa":"199-XYZ-277"},{"tipo":"Camión refrigerado","capacidad_m3":10,"temperatura_minima":-8.5,"temperatura_maxima":6,"empresa":"RefrigSafe","placa":"472-XYZ-422"}],"unidades_medicas":[{"nombre":"UMF 70 Oaxaca","latitud":15.961727,"longitud":-95.035741},{"nombre":"UMF 21 Oaxaca","latitud":16.142693,"longitud":-95.165675},{"nombre":"UMF 34 Oaxaca","latitud":16.067146,"longitud":-95.05848},{"nombre":"UMF 66 Oaxaca","latitud":16.084492,"longitud":-95.158829},{"nombre":"UMF 88 Oaxaca","latitud":16.137511,"longitud":-95.126163},{"nombre":"UMF 46 Oaxaca","latitud":16.108436,"longitud":-95.070225},{"nombre":"UMF 93 Oaxaca","latitud":15.985833,"longitud":-95.163125},{"nombre":"UMF 37 Oaxaca","latitud":15.9654,"longitud":-95.045696}]},{"nombre":"Centro de Almacenamiento 37 Oaxaca","latitud":16.18773,"longitud":-95.039089,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":17,"temperatura_minima":-28.7,"temperatura_maxima":3.9,"empresa":"RefrigSafe","placa":"302-XYZ-415"},{"tipo":"Van refrigerada","capacidad_m3":19,"temperatura_minima":-19.7,"temperatura_maxima":4.3,"empresa":"RefrigSafe","placa":"436-XYZ-949"},{"tipo":"Camión refrigerado","capacidad_m3":24,"temperatura_minima":-22.2,"temperatura_maxima":4.2,"empresa":"FríoExpress","placa":"453-XYZ-201"}],"unidades_medicas":[{"nombre":"UMF 86 Oaxaca","latitud":16.130474,"longitud":-95.036057},{"nombre":"UMF 15 Oaxaca","latitud":16.112974,"longitud":-95.050565},{"nombre":"UMF 40 Oaxaca","latitud":16.227259,"longitud":-95.0042},{"nombre":"UMF 56 Oaxaca","latitud":16.22643,"longitud":-94.970255},{"nombre":"UMF 76 Oaxaca","latitud":16.107969,"longitud":-95.028351},{"nombre":"UMF 21 Oaxaca","latitud":16.274697,"longitud":-94.958989},{"nombre":"UMF 5 Oaxaca","latitud":16.228358,"longitud":-95.10885},{"nombre":"UMF 32 Oaxaca","latitud":16.28543,"longitud":-94.999161}]},{"nombre":"Centro de Almacenamiento 34 Oaxaca","latitud":16.098296,"longitud":-95.085839,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":28,"temperatura_minima":-2.8,"temperatura_maxima":5.4,"empresa":"RefrigSafe","placa":"814-XYZ-144"},{"tipo":"Contenedor frigorífico","capacidad_m3":28,"temperatura_minima":-3.8,"temperatura_maxima":6.7,"empresa":"RefrigSafe","placa":"752-XYZ-843"},{"tipo":"Contenedor frigorífico","capacidad_m3":14,"temperatura_minima":-27.7,"temperatura_maxima":4.2,"empresa":"FríoExpress","placa":"459-XYZ-597"}],"unidades_medicas":[{"nombre":"UMF 20 Oaxaca","latitud":16.024552,"longitud":-95.086714},{"nombre":"UMF 60 Oaxaca","latitud":15.998526,"longitud":-95.102346},{"nombre":"UMF 29 Oaxaca","latitud":16.061774,"longitud":-95.021523},{"nombre":"UMF 75 Oaxaca","latitud":16.055797,"longitud":-95.089488},{"nombre":"UMF 13 Oaxaca","latitud":16.110955,"longitud":-94.987907},{"nombre":"UMF 48 Oaxaca","latitud":16.11765,"longitud":-95.148364},{"nombre":"UMF 100 Oaxaca","latitud":16.0436,"longitud":-95.099525},{"nombre":"UMF 74 Oaxaca","latitud":16.042504,"longitud":-95.169011}]}]},{"nombre":"Tampico","latitud":22.2149,"longitud":-97.8516,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":9,"temperatura_minima":-27.7,"temperatura_maxima":2.8,"empresa":"FríoExpress","placa":"852-XYZ-735"},{"tipo":"Contenedor frigorífico","capacidad_m3":10,"temperatura_minima":-4.9,"temperatura_maxima":2.6,"empresa":"TransVacunas","placa":"513-XYZ-957"},{"tipo":"Contenedor frigorífico","capacidad_m3":13,"temperatura_minima":-17.8,"temperatura_maxima":2.4,"empresa":"TransVacunas","placa":"810-XYZ-550"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 26 Tamaulipas","latitud":22.373,"longitud":-97.694433,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":8,"temperatura_minima":-14.5,"temperatura_maxima":4.9,"empresa":"RefrigSafe","placa":"818-XYZ-983"},{"tipo":"Camión refrigerado","capacidad_m3":29,"temperatura_minima":-2.5,"temperatura_maxima":5.4,"empresa":"FríoExpress","placa":"160-XYZ-135"},{"tipo":"Van refrigerada","capacidad_m3":23,"temperatura_minima":-3.1,"temperatura_maxima":3.3,"empresa":"RefrigSafe","placa":"647-XYZ-170"}],"unidades_medicas":[{"nombre":"UMF 35 Tamaulipas","latitud":22.290568,"longitud":-97.729678},{"nombre":"UMF 34 Tamaulipas","latitud":22.351933,"longitud":-97.692823},{"nombre":"UMF 80 Tamaulipas","latitud":22.314422,"longitud":-97.738397},{"nombre":"UMF 53 Tamaulipas","latitud":22.437549,"longitud":-97.690802},{"nombre":"UMF 4 Tamaulipas","latitud":22.370817,"longitud":-97.656404},{"nombre":"UMF 65 Tamaulipas","latitud":22.274778,"longitud":-97.781117},{"nombre":"UMF 92 Tamaulipas","latitud":22.32564,"longitud":-97.623759},{"nombre":"UMF 4 Tamaulipas","latitud":22.439028,"longitud":-97.653146}]},{"nombre":"Centro de Almacenamiento 37 Tamaulipas","latitud":22.025445,"longitud":-97.959076,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":9,"temperatura_minima":-17.8,"temperatura_maxima":5.6,"empresa":"TransVacunas","placa":"859-XYZ-705"},{"tipo":"Contenedor frigorífico","capacidad_m3":18,"temperatura_minima":-5.2,"temperatura_maxima":6.3,"empresa":"RefrigSafe","placa":"637-XYZ-365"},{"tipo":"Van refrigerada","capacidad_m3":24,"temperatura_minima":-17,"temperatura_maxima":6.3,"empresa":"RefrigSafe","placa":"773-XYZ-484"}],"unidades_medicas":[{"nombre":"UMF 69 Tamaulipas","latitud":22.045668,"longitud":-98.04857},{"nombre":"UMF 64 Tamaulipas","latitud":22.061838,"longitud":-97.888088},{"nombre":"UMF 95 Tamaulipas","latitud":22.114849,"longitud":-97.94779},{"nombre":"UMF 25 Tamaulipas","latitud":22.004784,"longitud":-98.003322},{"nombre":"UMF 11 Tamaulipas","latitud":22.003235,"longitud":-97.978693},{"nombre":"UMF 66 Tamaulipas","latitud":22.097622,"longitud":-97.883658},{"nombre":"UMF 59 Tamaulipas","latitud":21.934325,"longitud":-97.907909},{"nombre":"UMF 60 Tamaulipas","latitud":22.051956,"longitud":-97.892683}]},{"nombre":"Centro de Almacenamiento 14 Tamaulipas","latitud":22.142982,"longitud":-97.830215,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":15,"temperatura_minima":-5,"temperatura_maxima":6,"empresa":"TransVacunas","placa":"760-XYZ-736"},{"tipo":"Van refrigerada","capacidad_m3":7,"temperatura_minima":-1.8,"temperatura_maxima":3.1,"empresa":"FríoExpress","placa":"983-XYZ-734"},{"tipo":"Contenedor frigorífico","capacidad_m3":7,"temperatura_minima":1.5,"temperatura_maxima":5.5,"empresa":"TransVacunas","placa":"884-XYZ-732"}],"unidades_medicas":[{"nombre":"UMF 74 Tamaulipas","latitud":22.166557,"longitud":-97.917544},{"nombre":"UMF 44 Tamaulipas","latitud":22.106822,"longitud":-97.89525},{"nombre":"UMF 63 Tamaulipas","latitud":22.144514,"longitud":-97.904865},{"nombre":"UMF 51 Tamaulipas","latitud":22.191479,"longitud":-97.806271},{"nombre":"UMF 93 Tamaulipas","latitud":22.145967,"longitud":-97.786879},{"nombre":"UMF 90 Tamaulipas","latitud":22.186039,"longitud":-97.766514},{"nombre":"UMF 68 Tamaulipas","latitud":22.044679,"longitud":-97.754609},{"nombre":"UMF 68 Tamaulipas","latitud":22.138979,"longitud":-97.927654}]}]},{"nombre":"Tuxpan","latitud":20.9633,"longitud":-97.4089,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":30,"temperatura_minima":-10.5,"temperatura_maxima":4.1,"empresa":"RefrigSafe","placa":"970-XYZ-522"},{"tipo":"Contenedor frigorífico","capacidad_m3":6,"temperatura_minima":-10.5,"temperatura_maxima":7.6,"empresa":"TransVacunas","placa":"761-XYZ-272"},{"tipo":"Camión refrigerado","capacidad_m3":8,"temperatura_minima":-20.3,"temperatura_maxima":4.2,"empresa":"TransVacunas","placa":"494-XYZ-428"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 22 Veracruz","latitud":21.130892,"longitud":-97.348938,"transportes":[{"tipo":"Van refrigerada","capacidad_m3":29,"temperatura_minima":-18.7,"temperatura_maxima":6,"empresa":"FríoExpress","placa":"234-XYZ-482"},{"tipo":"Contenedor frigorífico","capacidad_m3":25,"temperatura_minima":-9.3,"temperatura_maxima":2.4,"empresa":"RefrigSafe","placa":"737-XYZ-718"},{"tipo":"Van refrigerada","capacidad_m3":22,"temperatura_minima":-3.3,"temperatura_maxima":4.2,"empresa":"FríoExpress","placa":"990-XYZ-458"}],"unidades_medicas":[{"nombre":"UMF 43 Veracruz","latitud":21.088983,"longitud":-97.316612},{"nombre":"UMF 95 Veracruz","latitud":21.059208,"longitud":-97.330718},{"nombre":"UMF 77 Veracruz","latitud":21.194702,"longitud":-97.385084},{"nombre":"UMF 29 Veracruz","latitud":21.121464,"longitud":-97.369001},{"nombre":"UMF 82 Veracruz","latitud":21.150392,"longitud":-97.342508},{"nombre":"UMF 30 Veracruz","latitud":21.036659,"longitud":-97.341616},{"nombre":"UMF 40 Veracruz","latitud":21.085138,"longitud":-97.435044},{"nombre":"UMF 78 Veracruz","latitud":21.195266,"longitud":-97.250579}]},{"nombre":"Centro de Almacenamiento 37 Veracruz","latitud":21.10829,"longitud":-97.483404,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":5,"temperatura_minima":-9.3,"temperatura_maxima":6.1,"empresa":"FríoExpress","placa":"438-XYZ-768"},{"tipo":"Contenedor frigorífico","capacidad_m3":18,"temperatura_minima":-1.6,"temperatura_maxima":6.9,"empresa":"RefrigSafe","placa":"147-XYZ-111"},{"tipo":"Van refrigerada","capacidad_m3":24,"temperatura_minima":-10.5,"temperatura_maxima":7.3,"empresa":"TransVacunas","placa":"103-XYZ-851"}],"unidades_medicas":[{"nombre":"UMF 28 Veracruz","latitud":21.046132,"longitud":-97.389728},{"nombre":"UMF 69 Veracruz","latitud":21.084272,"longitud":-97.39287},{"nombre":"UMF 71 Veracruz","latitud":21.11963,"longitud":-97.5732},{"nombre":"UMF 40 Veracruz","latitud":21.158019,"longitud":-97.545579},{"nombre":"UMF 39 Veracruz","latitud":21.174196,"longitud":-97.515286},{"nombre":"UMF 29 Veracruz","latitud":21.137496,"longitud":-97.57245},{"nombre":"UMF 44 Veracruz","latitud":21.059127,"longitud":-97.456079},{"nombre":"UMF 57 Veracruz","latitud":21.205548,"longitud":-97.518106}]},{"nombre":"Centro de Almacenamiento 43 Veracruz","latitud":20.795162,"longitud":-97.232146,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":17,"temperatura_minima":-10.1,"temperatura_maxima":5.2,"empresa":"TransVacunas","placa":"568-XYZ-433"},{"tipo":"Contenedor frigorífico","capacidad_m3":6,"temperatura_minima":-29.4,"temperatura_maxima":5.4,"empresa":"RefrigSafe","placa":"888-XYZ-733"},{"tipo":"Van refrigerada","capacidad_m3":17,"temperatura_minima":-26.8,"temperatura_maxima":4.6,"empresa":"FríoExpress","placa":"836-XYZ-410"}],"unidades_medicas":[{"nombre":"UMF 65 Veracruz","latitud":20.766606,"longitud":-97.23111},{"nombre":"UMF 43 Veracruz","latitud":20.726945,"longitud":-97.269684},{"nombre":"UMF 20 Veracruz","latitud":20.751131,"longitud":-97.319972},{"nombre":"UMF 38 Veracruz","latitud":20.824845,"longitud":-97.217552},{"nombre":"UMF 45 Veracruz","latitud":20.751142,"longitud":-97.274924},{"nombre":"UMF 87 Veracruz","latitud":20.699898,"longitud":-97.260118},{"nombre":"UMF 74 Veracruz","latitud":20.884797,"longitud":-97.18012},{"nombre":"UMF 15 Veracruz","latitud":20.887295,"longitud":-97.225066}]}]},{"nombre":"Veracruz","latitud":19.1809,"longitud":-96.1429,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":11,"temperatura_minima":-27.7,"temperatura_maxima":3.2,"empresa":"FríoExpress","placa":"712-XYZ-972"},{"tipo":"Contenedor frigorífico","capacidad_m3":11,"temperatura_minima":-24,"temperatura_maxima":6.9,"empresa":"TransVacunas","placa":"117-XYZ-271"},{"tipo":"Van refrigerada","capacidad_m3":16,"temperatura_minima":-11.5,"temperatura_maxima":7.5,"empresa":"RefrigSafe","placa":"923-XYZ-543"}],"centros_almacenamiento":[{"nombre":"Centro de Almacenamiento 4 Veracruz","latitud":19.204958,"longitud":-96.233762,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":27,"temperatura_minima":-4.2,"temperatura_maxima":4.5,"empresa":"RefrigSafe","placa":"501-XYZ-738"},{"tipo":"Camión refrigerado","capacidad_m3":27,"temperatura_minima":-3.8,"temperatura_maxima":2.2,"empresa":"FríoExpress","placa":"904-XYZ-824"},{"tipo":"Contenedor frigorífico","capacidad_m3":27,"temperatura_minima":-28.4,"temperatura_maxima":2.3,"empresa":"RefrigSafe","placa":"735-XYZ-438"}],"unidades_medicas":[{"nombre":"UMF 21 Veracruz","latitud":19.113488,"longitud":-96.23326},{"nombre":"UMF 45 Veracruz","latitud":19.190744,"longitud":-96.14165},{"nombre":"UMF 85 Veracruz","latitud":19.303607,"longitud":-96.192331},{"nombre":"UMF 82 Veracruz","latitud":19.127684,"longitud":-96.221772},{"nombre":"UMF 44 Veracruz","latitud":19.23403,"longitud":-96.251843},{"nombre":"UMF 98 Veracruz","latitud":19.267734,"longitud":-96.236844},{"nombre":"UMF 98 Veracruz","latitud":19.299286,"longitud":-96.256568},{"nombre":"UMF 20 Veracruz","latitud":19.191528,"longitud":-96.315347}]},{"nombre":"Centro de Almacenamiento 40 Veracruz","latitud":19.162761,"longitud":-96.153595,"transportes":[{"tipo":"Camión refrigerado","capacidad_m3":21,"temperatura_minima":0.3,"temperatura_maxima":4.3,"empresa":"FríoExpress","placa":"839-XYZ-673"},{"tipo":"Camión refrigerado","capacidad_m3":10,"temperatura_minima":-19.6,"temperatura_maxima":4.9,"empresa":"FríoExpress","placa":"344-XYZ-969"},{"tipo":"Contenedor frigorífico","capacidad_m3":25,"temperatura_minima":-29.6,"temperatura_maxima":3.4,"empresa":"RefrigSafe","placa":"131-XYZ-824"}],"unidades_medicas":[{"nombre":"UMF 72 Veracruz","latitud":19.177237,"longitud":-96.100294},{"nombre":"UMF 84 Veracruz","latitud":19.223202,"longitud":-96.141379},{"nombre":"UMF 21 Veracruz","latitud":19.163527,"longitud":-96.238031},{"nombre":"UMF 49 Veracruz","latitud":19.097055,"longitud":-96.233507},{"nombre":"UMF 50 Veracruz","latitud":19.219462,"longitud":-96.072562},{"nombre":"UMF 44 Veracruz","latitud":19.189,"longitud":-96.162335},{"nombre":"UMF 31 Veracruz","latitud":19.199185,"longitud":-96.14147},{"nombre":"UMF 37 Veracruz","latitud":19.094305,"longitud":-96.175263}]},{"nombre":"Centro de Almacenamiento 24 Veracruz","latitud":19.078928,"longitud":-96.080855,"transportes":[{"tipo":"Contenedor frigorífico","capacidad_m3":21,"temperatura_minima":-10.4,"temperatura_maxima":7.7,"empresa":"FríoExpress","placa":"646-XYZ-289"},{"tipo":"Van refrigerada","capacidad_m3":24,"temperatura_minima":-7.1,"temperatura_maxima":2.4,"empresa":"TransVacunas","placa":"983-XYZ-354"},{"tipo":"Camión refrigerado","capacidad_m3":6,"temperatura_minima":-29.3,"temperatura_maxima":7.9,"empresa":"RefrigSafe","placa":"577-XYZ-414"}],"unidades_medicas":[{"nombre":"UMF 52 Veracruz","latitud":19.069802,"longitud":-96.042024},{"nombre":"UMF 29 Veracruz","latitud":18.992013,"longitud":-96.107655},{"nombre":"UMF 71 Veracruz","latitud":19.143162,"longitud":-96.073809},{"nombre":"UMF 33 Veracruz","latitud":19.009348,"longitud":-96.062831},{"nombre":"UMF 90 Veracruz","latitud":19.162456,"longitud":-96.05854},{"nombre":"UMF 52 Veracruz","latitud":19.010639,"longitud":-96.050792},{"nombre":"UMF 86 Veracruz","latitud":19.10712,"longitud":-96.043425},{"nombre":"UMF 2 Veracruz","latitud":19.078706,"longitud":-96.171713}]}]}]');

        function cargarAduanas() {
            let select = document.getElementById("aduana");
            aduanas.forEach(aduana => {
                let option = document.createElement("option");
                option.value = aduana.nombre;
                option.textContent = aduana.nombre;
                select.appendChild(option);
            });
        }

        function cargarDatosAduana() {
            let seleccion = document.getElementById("aduana").value;
            let aduana = aduanas.find(a => a.nombre === seleccion);
            document.getElementById("latitud").value = aduana?.latitud || '';
            document.getElementById("longitud").value = aduana?.longitud || '';

            let transporteSelect = document.getElementById("transportes");
            transporteSelect.innerHTML = '<option value="">Seleccione un transporte</option>';
            aduana?.transportes.forEach(transporte => {
                let option = document.createElement("option");
                option.value = JSON.stringify(transporte);
                option.textContent = transporte.tipo;
                transporteSelect.appendChild(option);
            });
        }

        function cargarDatosTransporte() {
            let datos = JSON.parse(document.getElementById("transportes").value);
            let contenedor = document.getElementById("datos-transporte");
            contenedor.innerHTML = `
                <div class="row">
                    <div class="col-md-4"><strong>Tipo:</strong> ${datos.tipo}</div>
                    <div class="col-md-4"><strong>Capacidad:</strong> ${datos.capacidad_m3} m³</div>
                    <div class="col-md-4"><strong>Empresa:</strong> ${datos.empresa}</div>
                    <div class="col-md-4"><strong>Placa:</strong> ${datos.placa}</div>
                    <div class="col-md-4"><strong>Temperatura:</strong> ${datos.temperatura_minima}°C a ${datos.temperatura_maxima}°C</div>
                </div>
            `;
        }
function cargarCentros() {
    let seleccion = document.getElementById("aduana").value;
    let aduana = aduanas.find(a => a.nombre === seleccion);

    let centroSelect = document.getElementById("centros");
    centroSelect.innerHTML = '<option value="">Seleccione un centro</option>';

    if (aduana && aduana.centros_almacenamiento) {
        aduana.centros_almacenamiento.forEach(centro => {
            let option = document.createElement("option");
            option.value = centro.nombre;
            option.textContent = centro.nombre;
            centroSelect.appendChild(option);
        });
    }
}


function cargarDatosCentro() {
    let seleccion = document.getElementById("centros").value;
    let selectUnidades = document.getElementById("unidades");
    let latitudUnidad = document.getElementById("latitudUnidad");
    let longitudUnidad = document.getElementById("longitudUnidad");

    selectUnidades.innerHTML = '<option value="">Seleccione una unidad médica</option>';
    latitudUnidad.value = '';
    longitudUnidad.value = '';

    let aduanaSeleccionada = document.getElementById("aduana").value;
    let aduana = aduanas.find(a => a.nombre === aduanaSeleccionada);

    if (aduana) {
        let centro = aduana.centros_almacenamiento.find(c => c.nombre === seleccion);
       
    }
}

 
    function cargarDatosCentro2() {
        const centrosSelect = document.getElementById("centros");
        const latitudCentro = document.getElementById("latitudCentro");
        const longitudCentro = document.getElementById("longitudCentro");
        
        const centroSeleccionado = centrosSelect.value;
        
        if (centroSeleccionado) {
            const aduana = aduanas.find(a => a.centros_almacenamiento.some(c => c.nombre === centroSeleccionado));
            const centro = aduana ? aduana.centros_almacenamiento.find(c => c.nombre === centroSeleccionado) : null;
            
            if (centro) {
                latitudCentro.value = centro.latitud;
                longitudCentro.value = centro.longitud;
            }
        } else {
            latitudCentro.value = "";
            longitudCentro.value = "";
        }
    }



document.getElementById("aduana").addEventListener("change", cargarCentros);
        window.onload = cargarAduanas;
		
		
		        // Inicializar el mapa
       let map; // Declarar globalmente

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;

        map = L.map('map').setView([lat, lon], 10); // Asegurar que el zoom no sea muy alto
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        L.marker([lat, lon]).addTo(map)
            .bindPopup('Tu ubicación actual')
            .openPopup();
    }, function() {
        //alert("No se pudo obtener la ubicación");
    });
} else {
    //alert("La geolocalización no es compatible con este navegador.");
}


        // Agregar capa de OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
		
function Recorrertabla() {		



rutas = generarRutasDesdeTabla();

rutas.forEach(ruta => {
            L.polyline(ruta.coordenadas, { color: ruta.color, weight: 50 }).addTo(map)
                .bindPopup(ruta.nombre);
        });
console.log(rutas)
}		
		
function agregarCentro() {
    // Obtener valores seleccionados
    let centro = document.getElementById("centros").value;
    let latitudCentro = document.getElementById("latitudCentro").value;
    let longitudCentro = document.getElementById("longitudCentro").value;
    let aduana = document.getElementById("aduana").value;

    // Validar que se haya seleccionado un centro y una aduana
    if (!centro || !aduana) {
        alert("Seleccione un centro de almacenamiento y una aduana.");
        return;
    }

    // Obtener la tabla donde se agregarán los datos
    let tabla = document.getElementById("tablaCentros");

    // Crear una nueva fila y celdas
    let nuevaFila = tabla.insertRow();
    let celdaCentro = nuevaFila.insertCell(0);
    let celdaLatitud = nuevaFila.insertCell(1);
    let celdaLongitud = nuevaFila.insertCell(2);
    let celdaAduana = nuevaFila.insertCell(3);

    // Insertar valores en las celdas
    celdaCentro.innerHTML = centro;
    celdaLatitud.innerHTML = latitudCentro;
    celdaLongitud.innerHTML = longitudCentro;
    celdaAduana.innerHTML = aduana;
	
	if (typeof map !== 'undefined' && map !== null) {
    map.remove();
}

// Coordenadas de la ruta
var coordinates = [];
    var table = document.getElementById("tablaCentros");

    if (table) {
        var rows = table.getElementsByTagName("tr");

        for (var i = 1; i < rows.length; i++) { // Empezamos en 1 para omitir encabezado
            var cells = rows[i].getElementsByTagName("td");
            if (cells.length >= 3) {
                var lat = parseFloat(cells[1].textContent.trim());
                var lon = parseFloat(cells[2].textContent.trim());
                coordinates.push([lat, lon]);
            }
        }
    }

// Inicializar el mapa centrado en la primera coordenada con zoom 20
 map = L.map('map').setView(coordinates[0], 10);

// Agregar capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Agregar un marcador en la primera coordenada
L.marker(coordinates[0]).addTo(map)
    .bindPopup('Inicio de la ruta')
    .openPopup();

// Dibujar la línea de la ruta
L.polyline(coordinates, { color: 'blue' }).addTo(map);
}		



function generarRutasDesdeTabla() {
    var rutas = [];
    var filas = document.querySelectorAll("#tablaCentros tr");

    filas.forEach((fila, index) => {
        var columnas = fila.querySelectorAll("td");
        if (columnas.length > 0) {
            var nombreCentro = columnas[0].textContent.trim();
            var latitud = parseFloat(columnas[1].textContent.trim());
            var longitud = parseFloat(columnas[2].textContent.trim());
			map.setView([latitud, longitud], 50);
            rutas.push({
                nombre: `Ruta ${index + 1}`,
                color: index % 2 === 0 ? "blue" : "red", // Alternando colores para ejemplo
                coordenadas: [[latitud, longitud]]
            });
        }
    });
    
    console.log(rutas);
    return rutas;
}



setTimeout(function () {
    console.log("STOP!");
}, 1);


    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
	<script src="https://framework-gb.cdn.gob.mx/gm/v4/js/gobmx.js"></script>
</body>
</html>


    """
    return render_template_string(html_content)



if __name__ == '__main__':


    
    app.run(host='0.0.0.0',port=5021)





