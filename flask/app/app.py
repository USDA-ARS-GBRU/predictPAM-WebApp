# -*- coding: utf-8 -*-
from flask import Flask, request,make_response, render_template, jsonify, session
import requests
import os
from werkzeug.utils import secure_filename
import sys
import pandas as pd
import numpy as np
from serverside.serverside_table import ServerSideTable
from serverside import table_schemas
import predictPAM.main
from flask import Blueprint, jsonify, request

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users/anushkaswarup/Downloads/Storage/EPI/WebAppPAM/app/'
UPLOAD_FOLD = os.getcwd()+"/"

UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
ALLOWED_EXTENSIONS = {'gbk','gb'}

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

def collect_data_serverside(self, request):
        columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
        return ServerSideTable(request, data_dict, columns).output_result()


application = Flask(__name__,
           template_folder="templates")
application.secret_key = 'go gators'

@application.route('/handle_form', methods=['POST'])
def handle_form():

    print('on submit')

    files = request.files.getlist("file[]")
    for file in files:
        file.save(secure_filename(file.filename))
        print("Hi "+os.getcwd())


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
    for file in files:
        gbkfile = UPLOAD_FOLD+file.filename
        gbkfileloc.append(gbkfile)

    out = request.form['Output']

    print("gbkfileloc: "+gbkfileloc[0])

    data = {"gbkfile":gbkfileloc, "pamseq":pamSeq, "targetlength":tarLength,
    "strand":strand_str, "lcp":lcp,"eds":eds, "outfile":out, "tempdir":None, "threads":1, "log":"predictpam.log"}

    data_obj = objectview(data)

    predictPAM.main.main(data_obj)

    session['output_file'] = out

    return render_template("serverside_table.html");


@application.route("/serverside", methods=['GET'])
def serverside_table_content():
    #read query paramas
    # read the random text, and data from output_<random_text>.txt
    out = session.get('output_file', None)
    df = pd.read_csv(out, sep="\t", header=0)

    data_dict = df.fillna(0).to_dict('records')

    columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
    data = ServerSideTable(request, data_dict, columns).output_result()
    return jsonify(data)

@application.route("/exportcsv", methods=['GET', 'POST'])
def exportcsv():
  out = session.get('output_file', None)
  df = pd.read_csv(out, sep="\t", header=0)
  resp = make_response(df.to_csv())
  resp.headers["Content-Disposition"] = ("attachment; filename=%s" % out)
  resp.headers["Content-Type"] = "text/csv"
  return resp

@application.route("/")
def index():
    return render_template("input.html");

if __name__ == '__main__':
    application.run(host='0.0.0.0')   