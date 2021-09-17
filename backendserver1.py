import sqlite3
from flask import Flask
from flask import jsonify
from flask import render_template

app = Flask(__name__)


@app.route('/manager')
def manager():
    db = sqlite3.connect("machine.db")
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS machine(ip varchar(30), password varchar(30), rick varchar(30), position varchar(30), user varchar(30))'
    cursor.execute(sql)
    sql = 'INSERT INTO machine(ip, password, rick, position, user) VALUES(\'10.177.1.64\', \'password\', \'D1\', \'04\', \'熊皮\')'
    cursor.execute(sql)
    sql = 'INSERT INTO machine(ip, password, rick, position, user) VALUES(\'10.177.1.63\', \'*a1qweqr\', \'A4\', \'07\', \'刘皮\')'
    cursor.execute(sql)
    db.commit()
    db.close()
    return render_template('form.html')

@app.route('/getmachine')
def getmachine():
    db = sqlite3.connect("machine.db")
    cursor = db.cursor()
    sql = 'SELECT * FROM machine'
    cursor.execute(sql)
    data = cursor.fetchall()
    datalist = []
    for detail in data:
        datalist.append(
            {
                "ip" : detail[0],
                "password" : detail[1],
                "rick" : detail[2],
                "position" : detail[3],
                "user" : detail[4]
            }
        )
    return jsonify({'data': datalist})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
