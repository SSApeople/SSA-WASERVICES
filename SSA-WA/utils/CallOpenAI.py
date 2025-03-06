import requests
from decouple import config
#from ApegoContractual.LOGS import LogCaratula

class OpenAIConector:

    def __init__(self):
        self.api_key_ = config('API_KEY_OPENAI')
        self.endpoint_ = config('ENDPOINT_OPENAI')
        self.model_ = config('MODELO_OPENAI')

    def enviarOPENAI(self, pregunta: str) -> str:
        resultado=''
        #log = LogCaratula('LOGOPENAI')
        api_key = self.api_key_
        endpoint = self.endpoint_
        headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
        data = {
                'model': self.model_,
                "messages": [
                {
                "role": "user",
                "content": pregunta
                }
            ]
            }
        try:
         #log.Agrega(f'Pregunta >> paso request a OPENAI', f'Anexo Técnico >> Desglose >> pregunta a OPENAI ', False)
         response = requests.post(endpoint, headers=headers, json=data, timeout=120)
         response.raise_for_status()
         resultado = response.json()
         resultado=resultado['choices'][0]['message']['content']
        except requests.exceptions.Timeout:
          print('Timeout en la solicitud a OpenAI');
          #log.Agrega('Timeout en la solicitud a OpenAI', 'Error en consulta a OpenAI', False)
        except requests.exceptions.RequestException as e:
          print('Error en consulta a OpenAI') 
          #log.Agrega(str(e), 'Error en consulta a OpenAI', False)
        except requests.exceptions.ConnectionError as e:
          print(f'Error de conexión: {e}');
          #log.Agrega(f'Error de conexión: {e}', 'Error en consulta a OpenAI', False)
        except KeyError:
          print('Respuesta inesperada de OpenAI');
          #log.Agrega('Respuesta inesperada de OpenAI', 'Error en consulta a OpenAI', False)
        except Exception as e:
          print('Error en consulta a OpenAI');
          #log.Agrega(str(e), 'Error en consulta a OpenAI', False)  
  
            
        
        return resultado
    










