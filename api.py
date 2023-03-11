import src.inference
import src.graph_data
import src.graph_folder
from flask import Flask,request
from read_params import read_params
from src.pdf_api import CheckFiles
from flask import Flask, jsonify, request, make_response

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

# API function for body-wise classification
def API_Body(data,username,password):
    try:
        label = src.inference.Prediction_On_Body(data['Body'])
        response_b = {
            'From':data['From'],
            'Subject':data['Subject'],
            'Body':data['Body'],
            'Label':label
            }
    except Exception:
        return make_response(jsonify({"Error": "There is some problem in Model for Body!"}),404)
    try:
        uid = data['UID']
        if src.graph_folder.FolderChecker_For_Body(label,username,password):
            src.graph_folder.Move_Items_For_Body(uid,label,username,password)
        else:
            src.graph_folder.Create_Folder_For_Body(label,username,password)
            src.graph_folder.Move_Items_For_Body(uid,label,username,password)
    except Exception:
        return make_response(jsonify({"Error": "There is no Mail in Inbox for Body "}),404)
    return response_b

config = read_params('config.yaml')

app = Flask(__name__)

@app.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'error': 'Misunderstood'}), 400)

@app.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({'error': 'Unauthorised'}), 401)

@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'error': 'Server error'}), 500)

@app.route('/mail_api_v1.0', methods=['GET', 'POST'])
def outllookAPI():
    try:
        username = request.args.get("username")
        password = request.args.get("password")
        types = request.args.get("type")
        data = src.graph_data.Outlook_Reader(username,password,types)
        if str(data)=='None':
            return make_response(jsonify({"Error": "There is no Mail in Inbox !"}),404)
    except  Exception as e:
        return make_response(jsonify({"Error": "Invalid Request, please try again!"}),404)
    if len(data)>0:
        try:
            CheckFiles(data['Subject'])
        except Exception as e:
            print(e)
        try:
            response_b = API_Body(data,username,password)
            return make_response(jsonify({'Responses': response_b}), 200)
        except Exception as e:
            return make_response(jsonify({"Error": "Invalid Request, please try again!"}),404)
        

if __name__=="__main__":
    app.run(host='127.0.0.1', port=3008,debug=True)
    