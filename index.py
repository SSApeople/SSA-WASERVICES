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
        
<!DOCTYPE html>
<html>
<body>


<style> 

.tableauPlaceholder {
	width:100% !important'
}

</style>



 

<div class='tableauPlaceholder' id='viz1733953915488' style='position: relative; width:100% !important'>
  <noscript>
    <a href='#'>
      <img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;PO&#47;POC-SSAv3&#47;Vistageneral&#47;1_rss.png' style='border: none' />
    </a>
  </noscript>
  <object class='tableauViz' style='display:none;'>
    <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
    <param name='embed_code_version' value='3' />
    <param name='site_root' value='' />
    <param name='name' value='POC-SSAv3&#47;Vistageneral' />
    <param name='tabs' value='yes' />
    <param name='toolbar' value='yes' />
    <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;PO&#47;POC-SSAv3&#47;Vistageneral&#47;1.png' />
    <param name='animate_transition' value='yes' />
    <param name='display_static_image' value='yes' />
    <param name='display_spinner' value='yes' />
    <param name='display_overlay' value='yes' />
    <param name='display_count' value='yes' />
    <param name='language' value='es-ES' />
  </object>
</div>
 



<script type='text/javascript'>var divElement = document.getElementById('viz1733953915488');

var vizElement = divElement.getElementsByTagName('object')[0];
vizElement.style.width='100%';
vizElement.style.height='1050px';                     
var scriptElement = document.createElement('script');                    
scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';  
console.log(scriptElement)                
vizElement.parentNode.insertBefore(scriptElement, vizElement);   

document.onreadystatechange = function () {
    if (document.readyState === "complete") {
	
        const elementos = document.querySelectorAll('.tableauViz');
        if (elementos.length > 0) {
            elementos[0].style.margin = "auto";
					
        } else {
            console.warn("No se encontraron elementos con la clase '.tableauViz'.");
        }
    }
};


let interval = setInterval(function(){
     
	document.getElementsByClassName('tableauViz')[0].style.width = "1200px";
	document.getElementsByClassName('tableauViz')[0].style.margin = "auto";
	
	if (document.getElementsByTagName('iframe').length > 0) {
	
		setTimeout(function(){ 
			clearInterval(interval);
		}, 14000);
		 
	} 
    console.log('...Censo...')    
}, 100);
 
               
</script>


</body>
</html>



    """
    return render_template_string(html_content)

#if __name__ == '__main__':
 #   app.run(debug=True)
 



if __name__ == '__main__':


    
    app.run(port=5000)





