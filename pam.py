import os
from flask import Flask, request, render_template
import requests
from werkzeug import secure_filename
import sys

sys.path.insert(1, '/Users/anushkaswarup/Downloads/Storage/EPI/WebAppPAM/predictPAM/predictPAM/')

from main import main

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users/anushkaswarup/Downloads/Storage/EPI/WebAppPAM/predictPAM/predictPAM/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

app = Flask(__name__)

@app.route('/handle_form', methods=['POST'])
def handle_form():
    print("Posted file: {}".format(request.files['file']))
    file = request.files['file']
    #files = {'file': file.read()}
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
    gbkfileloc = ['/Users/anushkaswarup/Downloads/Storage/EPI/WebAppPAM/predictPAM/test/test_data/Burkholderia_thailandensis_E264__ATCC_700388_133.gbk']
    out = request.form['Output']

    data = {"gbkfile":gbkfileloc, "pamseq":pamSeq, "targetlength":tarLength, 
    "strand":strand_str, "lcp":lcp,"eds":eds, "outfile":out, "tempdir":None, "threads":1, "log":"predictpam.log"}

    data_obj = objectview(data)

    # predictPAM.main(data_obj)
    main(data_obj)

    return render_template("submit.html")
   
@app.route("/")
def index():
    return render_template("input.html");   


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)