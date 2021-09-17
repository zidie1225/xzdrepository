from flask import Flask,url_for,request,render_template,redirect,session,make_response
import time
from flask import jsonify
from flask import render_template
import server


app = Flask(__name__)
@app.route('/machine/list',methods=['GET'])
def getmachinefilter():
    city = request.args.get('city', None)
    solution = request.args.get('solution_id', None)
    machine_type = request.args.get('machine_type', None)
    pagesize = request.args.get('pagesize', None)
    offset = request.args.get('offset', None)
    orderByUsageStatus = request.args.get('orderByUsageStatus', None)

    where_para_list = []
    where_para_list.append({'city':city})
    where_para_list.append({'solution_id': solution})
    where_para_list.append({'machine_type': machine_type})

    if request.method == 'GET':
        dict_machine = server.get_machine_info(where_para_list, orderByUsageStatus, pagesize, offset)
        return jsonify(dict_machine)



@app.route('/machine/create', methods=['POST'])
def createmachine():
    if request.method == 'POST':
        request_body = request.get_data()
        result = server.insert_machine_info(request_body)
        return jsonify(result)

@app.route('/machine/modify', methods=['PUT'])
def modifymachine():
    if request.method == 'PUT':
        request_body = request.get_data()
        result = server.modify_machine_info(request_body)
        return jsonify(result)

@app.route('/machine/del/<int:rowid>', methods=['DELETE'])
def delmachine(rowid):
    if request.method == 'DELETE':
        print(rowid)
        result = server.del_machine_info(rowid)
        return jsonify(result)


@app.route('/solution/create', methods=['POST'])
def createsolution():
    if request.method == 'POST':
        request_body = request.get_data()
        result = server.insert_solution_info(request_body)
        return jsonify(result)

@app.route('/solution/info',methods=['GET'])
def getsolution():
    pagesize = request.args.get('pagesize', None)
    offset = request.args.get('offset', None)

    if request.method == 'GET':
        dict_solution = server.get_solution_info(pagesize, offset)
        return jsonify(dict_solution)

@app.route('/solution/info/<int:rowid>',methods=['GET'])
def getSolutionById(rowid):

    if request.method == 'GET':
        dict_solution = server.get_solution_name(rowid)
        return jsonify(dict_solution)

@app.route('/solution/modify', methods=['PUT'])
def modifySolution():
    if request.method == 'PUT':
        request_body = request.get_data()    #获取body信息
        result = server.modify_solution_info(request_body)
        return jsonify(result)

@app.route('/solution/del/<int:rowid>', methods=['DELETE'])
def delSolution(rowid):
    if request.method == 'DELETE':
        print(rowid)
        result = server.del_solution_info(rowid)
        return jsonify(result)

@app.route('/city/create', methods=['POST'])
def createcity():
    if request.method == 'POST':
        request_body = request.get_data()
        result = server.insert_city_info(request_body)
        return jsonify(result)

@app.route('/city/modify', methods=['PUT'])
def modifyCity():
    if request.method == 'PUT':
        request_body = request.get_data()    #获取body信息
        result = server.modify_city_info(request_body)
        return jsonify(result)

@app.route('/city/info',methods=['GET'])
def getcity():
    pagesize = request.args.get('pagesize', None)
    offset = request.args.get('offset', None)

    if request.method == 'GET':
        dict_solution = server.get_city_info(pagesize, offset)
        return jsonify(dict_solution)

@app.route('/city/info/<int:rowid>',methods=['GET'])
def getCityById(rowid):

    if request.method == 'GET':
        dict_solution = server.get_city_name(rowid)
        return jsonify(dict_solution)


@app.route('/city/del/<int:rowid>', methods=['DELETE'])
def delCity(rowid):
    if request.method == 'DELETE':
        print(rowid)
        result = server.del_city_info(rowid)
        return jsonify(result)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False    #解决编码问题
    app.run(host='0.0.0.0', debug=True)