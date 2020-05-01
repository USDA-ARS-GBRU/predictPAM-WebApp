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
import logging
import uuid

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'gbk','gb','gz'}

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

def collect_data_serverside(self, request):
        columns = table_schemas.SERVERSIDE_TABLE_COLUMNS
        return ServerSideTable(request, data_dict, columns).output_result()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


application = Flask(__name__,
           template_folder="templates")
application.secret_key = 'go gators'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    
    file_handler = logging.FileHandler('server.log')
    file_handler.setLevel(logging.DEBUG)

    application.logger.addHandler(file_handler)

    application.logger.setLevel(gunicorn_logger.level)


@application.route('/handle_form', methods=['POST'])
def handle_form():
    try:
        files = request.files.getlist("file[]")
        gbkfileloc = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4())+'.'+file.filename.rsplit('.', 1)[1].lower()
                print(filename)
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                gbkfileloc.append(os.path.join(application.config['UPLOAD_FOLDER'], filename))


        pamSeq = request.form['pamseq']
        tarLength = int(request.form['targetLength'])
        strand  = request.form['strand']
        orient = request.form['orient']

        strandStr = None

        if(strand=='1'):
            strandStr = 'forward'
        elif(strand=='2'):
            strandStr = 'reverse'
        elif(strand=='3'):
            strandStr = 'both'

        #add pamOrient to data dictionary when guidefinder integrated

        pamOrient = None

        if(strand=='1'):
            pamOrient = '5prime'
        elif(strand=='2'):
            pamOrient = '3prime'

        lcp = int(request.form['lcp']) 
        eds = int(request.form['eds'])

        out = request.form['Output']

        print("gbkfileloc: "+gbkfileloc[0])

        data = {"gbkfile":gbkfileloc, "pamseq":pamSeq, "targetlength":tarLength,
        "strand":strandStr, "lcp":lcp,"eds":eds, "outfile":out, "tempdir":None, "threads":1, "log":"predictpam.log"}

        data_obj = objectview(data)

        predictPAM.main.main(data_obj)

        session['output_file'] = out

        return render_template("serverside_table.html");

    except Exception as e:
        print("An error occurred in predictPAM")
        raise e


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
    application.logger.info('Start')
    return render_template("input.html");

if __name__ == '__main__':
    application.run(host='0.0.0.0')   