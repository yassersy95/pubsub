import collections
import json
from flask import request
import flask
import pymysql

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def getToJson(sql: str, keys):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='weather', passwd='weather', db='weather')
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    rowarray_list = []
    for row in rows:
        t = (row[0], row[1])
        rowarray_list.append(t)
    j = json.dumps(rowarray_list)
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d[keys[0]] = row[0]
        d[keys[1]] = row[1]
        objects_list.append(d)
    j = json.dumps(objects_list)
    print(j)
    cursor.close()
    conn.close()
    return j


@app.route('/getdevicesmax', methods=['GET'])
def getdevicesmax():
    sql = 'select deviceid, max(temperature) temp from weather_trans group by deviceid;'
    print('sent sql:' + sql)
    j = getToJson(sql, ["deviceId", "temperature"])
    print('returned sql:' + j)
    return j;


@app.route('/getdaymax', methods=['GET'])
def getdaymax():
    day = request.args.get('d')
    month = request.args.get('m')
    sql = 'select deviceid, max(temperature) from weather_trans where FROM_UNIXTIME(time,\'%d\') = ' + day + ' and '
    sql += 'FROM_UNIXTIME(time,\'%m\') = ' + month + ' group by deviceid;'
    print(sql)
    j = getToJson(sql, ["deviceId", "temperature"])
    return j



@app.route('/getanomalies', methods=['GET'])
def getanomalies():
    sql = 'select deviceid, temperature from weather_trans where isanomal = 1 and UNIX_TIMESTAMP() - time < 1800 order by deviceid;'
    print('sent sql:' + sql)
    j = getToJson(sql,["deviceId", "temperature"])
    print('returned sql:' + j)
    return j;

@app.route('/getdatapoints', methods=['GET'])
def getdatapoints():
    sql = 'select deviceid, count(*) from weather_trans group by deviceid;'
    print('sent sql:' + sql)
    j = getToJson(sql, ["deviceId", "count"])
    print('returned sql:' + j)
    return j;

@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    output = '<h1>Welcome to the weatherAPI</h1>'
    output += '<p>You can check the max temperature collected from each device by adding <u>getdevicesmax</u></p>'
    output += '<p>You can check the max temperature for a selected day by passing the {d} & {m} parameters '
    output += '<u>getdaymax?d=&m=</u></p> '
    output += '<p>You can check the detected temperature anamolies for the last 30 for each device by adding <u>'
    output += 'getanomalies</u></p>'
    return output


app.run(debug=True)
