import flask
from flask import Flask,Response
import requests
from read_params import read_params

config = read_params('credential.yaml')
app = Flask(__name__)
@app.route('/24x7_api', methods=['GET', 'POST'])
def prediction():
    def inner():
        for i in range(86600*365):
            parameters = {
                "username":config['Outlook']['username'],
                "password":config['Outlook']['password'],
                "type":"UNSEEN"
                }
            response = requests.get("http://127.0.0.1:3008/mail_api_v1.0",params = parameters)
        return  str(response.json()) +  '<br/>\n'
    return Response(inner())

if __name__=="__main__":
    app.run(host='127.0.0.1', port=5000,debug =True)
