from flask import Flask, request, render_template, jsonify
import requests
import os
from werkzeug import secure_filename
import sys
import pandas as pd
import numpy as np
from app.mod_tables.serverside.serverside_table import ServerSideTable
from app.mod_tables.serverside import table_schemas
import predictPAM.main
from flask import Blueprint, jsonify, request
from app import table_builder
# import uuid 



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

#tables = Blueprint('tables', __name__, url_prefix='')

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
    # + <random_text>

    data = {"gbkfile":gbkfileloc, "pamseq":pamSeq, "targetlength":tarLength, 
    "strand":strand_str, "lcp":lcp,"eds":eds, "outfile":out, "tempdir":None, "threads":1, "log":"predictpam.log"}

    data_obj = objectview(data)

    # predictPAM.main.main(data_obj)

    return render_template("serverside_table.html");


@app.route("/serverside", methods=['GET'])
def serverside_table_content():
    #read query paramas
    # read the random text, and data from output_<random_text>.txt
    df = pd.read_csv('out.txt', sep="\t", header=0)
    print('here')

    data_dict = df.fillna(0).to_dict('records')
    a = [{
      "accession_x": "NC_007650", 
      "accession_y": "NC_007650", 
      "db_xref_x": "['GeneID:3844926']", 
      "db_xref_y": "['GeneID:3844868']", 
      "distaltopam": "GGCAAGACTTGT", 
      "distance_x": 1189, 
      "distance_y": 0, 
      "gene_synonym_x": 0, 
      "gene_synonym_y": 0, 
      "locus_tag_x": "['BTH_II0002']", 
      "locus_tag_y": "['BTH_II0001']", 
      "name_x": 0, 
      "name_y": 0, 
      "note_x": 0, 
      "note_y": 0, 
      "pam_seq": "ATGC", 
      "product_name_confidence_x": 0, 
      "product_name_confidence_y": 0, 
      "product_synonym_x": 0, 
      "product_synonym_y": 0, 
      "product_x": 0, 
      "product_y": 0, 
      "protein_id_x": 0, 
      "protein_id_y": 0, 
      "proxitopam": "CGCTGCACGC", 
      "seqid": "NC_007650", 
      "start_x": 1280, 
      "start_y": 0, 
      "stop_x": 2324, 
      "stop_y": 1188, 
      "strand": "forward", 
      "strand_for_feature_x": "reverse", 
      "strand_for_feature_y": "forward", 
      "target": "GGCAAGACTTGTCGCTGCACGC", 
      "target_ep": 92, 
      "target_sp": 70, 
      "translation_x": 0, 
      "translation_y": 0, 
      "type_x": "gene", 
      "type_y": "gene"
    }]

    # data_clean = []

    # for i in range(0,df.shape[0]):
    #     columns = df.SERVERSIDE_TABLE_COLUMNS


    columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
    print(columns)
    data = ServerSideTable(request, data_dict, columns).output_result()
    return jsonify(data)

@app.route("/")
def index():
    return render_template("input.html");   

if __name__ == '__main__':
    app.run(debug=True)