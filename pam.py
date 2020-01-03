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

app = Flask(__name__)

@app.route('/handle_form', methods=['POST'])
def handle_form():
    print("Posted file: {}".format(request.files['file']))
    file = request.files['file']
    #files = {'file': file.read()}
    file.save(secure_filename(file.filename))
    pamSeq = request.form['pamseq']
    tarLength = request.form['targetLength']
    strand  = request.form['strand']
    strand_str = ""
    if(strand==1):
    	strand_str = 'forward'
    elif(strand==2):
    	strand_str = 'reverse'

    lcp = request.form['lcp']
    eds = request.form['eds']
    gbkfileloc = '/Users/anushkaswarup/Downloads/Storage/EPI/WebAppPAM/Burkholderia_thailandensis_E264__ATCC_700388_133.gbk'

    data = {"gbkfile":gbkfileloc, "pamseq":pamSeq, "targetlength":tarLength, 
    "strand":strand_str, "lcp":lcp,"eds":eds, "tempdir":None, "threads":1, "log":"predictpam.log"}

    main(data)

    return strands
   
@app.route("/")
def index():
    return render_template("input.html");   


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)