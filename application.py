from flask import Flask
import hcp_find_response
import hcp_response_generator
import hcp_get_history
from lazywritter import log_writter

application = Flask(__name__)

logger = log_writter()

geneset = hcp_response_generator.response_generator()

@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        finder = hcp_find_response.response_finder()
        return "Welcome."
    except Exception as e:
        return str(e)
    


@application.route('/welcome', methods=['GET', 'POST'])
def welcome(): 
    finder = hcp_find_response.response_finder()

    res_json = finder.get_welcome_message()

    response = geneset.generate_response(res_json)

    return response

@application.route('/calling/', methods=['GET', 'POST', 'OPTIONS'])
def calling():
    print('welcome')
    input = request.args['value']    
    response = jsonify(message=input)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(response)
    return input

@application.route('/hcpchat', methods=['GET', 'POST'])
def hcpchatbot():
    finder = hcp_find_response.response_finder()
    history = hcp_get_history.History()
    user_chat = request.args['conv']
    uid = request.args['uid']
    
    res_json = finder.find_response(user_chat)

    cur_response = geneset.generate_response(res_json)

    uid = history.check_generate_uid(uid)

    history.check_update_history(uid, user_chat, cur_response)

    response = {
        "chats": [{"message": cur_response, "who": "bot", "time": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}],
        "uid": uid
    }

    return response

@application.route('/hcpchathistory', methods=['GET', 'POST'])
def hcpchathistory():
    finder = hcp_find_response.response_finder()
    history = hcp_get_history.History()
    uid = request.args['uid']

    uid = history.check_generate_uid(uid)
    response = history.get_history_alone(uid, finder, geneset)

    return response

@application.route('/patientchat', methods=['GET', 'POST'])
def patientchatbot():
    input = request.args['value']
    return input


@application.route('/refreshCorpus', methods=['GET', 'POST'])
def refreshCorpus():
    import upload_excel_to_database

    corpus_filename='Corpus/Corpus.xlsx'
    corpus_sheetname='Patient_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    corpus_sheetname='HCP_Website_Data'
    upload_excel_to_database.UpdateDB(corpus_filename, corpus_sheetname)
    return "Successfully Updated."

