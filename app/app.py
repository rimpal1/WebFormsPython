from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import logging

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'bioStatsData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Biographic Data'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM bioData')
    result = cursor.fetchall()
    return render_template("index.html", title='Home', user=user, patients=result)


@app.route('/view/<int:id>', methods=['GET'])
def record_view(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM bioData WHERE id=%s', id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', patient=result[0])


@app.route('/edit/<int:id>', methods=['GET'])
def form_edit_get(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM bioData WHERE id=%s', id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', patient=result[0])


@app.route('/edit/<int:id>', methods=['POST'])
def form_update_post(id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('pname'), request.form.get('psex'), request.form.get('age'),
                 request.form.get('height'), request.form.get('weight'), id)
    sql_update_query = """UPDATE bioData t SET t.PatientName = %s, t.PatientSex = %s, t.Age = %s, t.Height =
    %s, t.Weight = %s WHERE id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/patients/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Patient Form')


@app.route('/patients/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('pname'), request.form.get('psex'), request.form.get('age'),
                 request.form.get('height'), request.form.get('weight'))
    app.logger.info('testing info log')
    app.logger.info(inputData)
    sql_insert_query = """INSERT INTO bioData (PatientName, PatientSex, Age, Height, Weight)
    VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:id>', methods=['POST'])
def form_delete_post(id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM bioData WHERE id = %s """
    cursor.execute(sql_delete_query, id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/patients', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM bioData')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/patients/<int:id>', methods=['GET'])
def api_retrieve(id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM bioData WHERE id=%s', id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/patients/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/patients/<int:id>', methods=['PUT'])
def api_edit(id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/patients/<int:id>', methods=['DELETE'])
def api_delete(id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)