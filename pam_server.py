from flask import Flask, request, render_template, jsonify
import requests
from werkzeug import secure_filename
import sys
import pandas as pd
import numpy as np
from app.mod_tables.serverside.serverside_table import ServerSideTable
from app.mod_tables.serverside import table_schemas
import predictPAM.main
from flask import Blueprint, jsonify, request
from app import table_builder


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users⁩/aswarup⁩/⁨Downloads⁩/⁨Storage⁩/⁨Github_repos⁩/⁨predictPAM-WebApp/⁩'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
ALLOWED_EXTENSIONS = {'gbk'}

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

def collect_data_serverside(self, request):
        columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
        return ServerSideTable(request, data_dict, columns).output_result()


app = Flask(__name__,
           template_folder="templates")

tables = Blueprint('tables', __name__, url_prefix='/tables')

@app.route('/handle_form', methods=['POST'])
def handle_form():
    # print("Posted file: {}".format(request.files['file']))
    # file = request.files('file[]')
    # print(file.filename)
    # print(file)
    # print(request.files.getlist('file[]'))
    # files = {'file': file.read()}
    # file.save(secure_filename(file.filename))

    files = request.files.getlist("file[]")
    for file in files:
        file.save(secure_filename(file.filename))


    pamSeq = request.form['pamseq']
    tarLength = int(request.form['targetLength'])
    strand  = request.form['strand']

    strand_str = None

    if(strand=='1'):
        strand_str = 'forward'
    elif(strand=='2'):
        strand_str = 'reverse'

    lcp = int(request.form['lcp']) 
    eds = int(request.form['eds'])

    gbkfileloc = []
    # gbkfileloc = np.asarray(gbkfileloc)

    for file in files:
        print(gbkfileloc)
        gbkfile = UPLOAD_FOLD+file.filename
        gbkfileloc.append(gbkfile)
        print(gbkfileloc)

    print(gbkfileloc)

    out = request.form['Output']

    data = {"gbkfile":gbkfileloc, "pamseq":pamSeq, "targetlength":tarLength, 
    "strand":strand_str, "lcp":lcp,"eds":eds, "outfile":out, "tempdir":None, "threads":1, "log":"predictpam.log"}

    data_obj = objectview(data)

    # predictPAM.main.main(data_obj)

    return render_template("serverside_table.html");


@tables.route("/serverside", methods=['GET'])
def serverside_table_content():

    df = pd.read_csv('out.txt', sep="\t", header=0)
    print('here')
    data_dict = df.to_dict()

    columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
    data = ServerSideTable(request, data_dict, columns).output_result()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
