import boto3

from flask import Flask, request, render_template


def upload_file(accesskey,secretkey,bname,fpath,file):
    try:
        session = boto3.Session(accesskey,secretkey)
        s3 = session.resource('s3')
        bucket=s3.Bucket(bname)
        bucket.put_object(Key=fpath, Body=file)
        return True
    except Exception as e:
        print e
        return False

def browse_bucket(accesskey,secretkey,bname,path):
    try:
        files={}
        files = {}
        session = boto3.Session(accesskey, secretkey)
        s3 = session.resource('s3')
        bucket = s3.Bucket(bname)
        i = 1
        for key in bucket.objects.filter(Prefix=path,Delimiter='/'):
            if len(str(key.key)[str(key.key).index(path)+len(path):])>0:
                files[i]=str(key.key)[str(key.key).index(path)+len(path):]
                i=i+1
        return files

    except Exception as e:
        print e
        return False



app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('FileUpload.html')

@app.route('/submit', methods=['POST'])
def my_form_post():
    akey = request.form['accesskey']
    skey=request.form['secretkey']
    bpath=request.form['targetbucketpath']
    file=request.files['file']

    if str(bpath).__contains__('/'):
        bname=bpath[0:str(bpath).index('/')]
        path = bpath[str(bpath).index('/') + 1:] + "/"
    else:
        bname=bpath
        path=""

    filestring=str(file)
    filename=filestring[16:filestring.index("'",16)]
    filepath=path+filename


    if upload_file(akey,skey,bname,filepath,file):
        files=browse_bucket(akey,skey,bname,path)
        return render_template('FileUpload.html', files=files,bucket=bpath,filename=filename)
    else:
        return render_template('FileUpload.html',files=None)


app.run()

