from flask import Flask,render_template,flash,request,redirect,url_for,Markup
from werkzeug import secure_filename
import subprocess,os,shutil


app = Flask(__name__)
app.secret_key='ldx'

ALLOWED_EXTENSIONS = set(['zip'])

def runcmd(num):
    if num == 1:
        comm = "salt '172.16.124.21' state.sls omsh5"
    elif num == 10:
        comm = "salt '172.16.124.11' state.sls omsh5"
    elif num == 11:
        comm = "salt -N omsh5 state.sls omsh5"
    else:
        return "Error"
    p = subprocess.Popen(comm,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    lists = ""
    for line in iter(p.stdout.readline,b''):
        line = line.rstrip().decode('utf8')
        if "Failed" in line:
            tmp = line
            if int(tmp.split(':')[-1].strip())>=0:
                line = "<font color='#FF0000'>" + line + "</font> "
        lists = lists + str(line)+str("<br>")
    return lists

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload",methods=["POST","GET"])
def upload():
    if request.method == "POST":
        f = request.files['file']
        test = request.form.get('test')
        dev = request.form.get('dev')
        num = 0
        if test:
            num = num + 1
        if dev:
            num = num + 10
        if file and allowed_file(f.filename):
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static','uploads', secure_filename(f.filename))
            f.save(upload_path)
            path = os.path.join("/", "data", "data", "salt", "file", "files", "dist.zip")
            shutil.move(upload_path, path)
            if num == 0:
                flash("No release environment was selected")
            else:
                info = runcmd(num)
                flash(Markup(info))
            return redirect(url_for('index'))
        else:
            flash("Wrong file format(zip")
    return redirect(url_for('index'))


@app.route("/",methods=["GET","POST"])
def index():
    return render_template('show_entries.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4901)
    pass
