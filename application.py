# SJSU CS 218 Fall 2019 TEAM6
# Adapted from https://kishstats.com/python/2018/03/15/flask-amazon-s3-series.html
from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type
from resources import get_bucket, get_buckets_list

application = app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret_key'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


@app.route('/', methods=['GET', 'POST'])
def logged():
    return render_template("login.html")


@app.route('/loggedin', methods=['GET', 'POST'])
def loggedin():
    if request.method == 'POST':
        new_bucket = request.form['bucket']
        session['bucket'] = new_bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        if request.args.get("email"):
            session['username'] = request.args.get("email").split('@')[0]
        buckets_sorted = []
        for new_bucket in buckets:
            buckets_sorted.append(new_bucket['Name'])
        buckets_sorted = sorted(buckets_sorted, reverse=True)
        print(buckets_sorted)
        return render_template("index.html", buckets=buckets_sorted)


@app.route('/files')
def files():
    my_bucket = get_bucket()
    all_objects = my_bucket.objects.filter(Prefix=session['username']+'/')

    return render_template('files.html', my_bucket=my_bucket, files=all_objects)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    my_bucket = get_bucket()
    prefix = session['username']+'/'
    path = prefix+file.filename
    my_bucket.Object(path).put(Body=file)

    flash('File uploaded successfully. You should receive a summary in your inbox shortly.')

    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == "__main__":
    app.debug = True
    app.run()
