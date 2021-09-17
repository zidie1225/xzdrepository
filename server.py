import time
import dto
import json

def get_machine_info(where_para_list, orderByUsageStatus, pagesize, offset):

    len_where_para = len(where_para_list)
    for i in range(len_where_para-1,-1,-1):
        if 'machine_type' in where_para_list[i] and list(where_para_list[i].values())[0] != None:
            aa = where_para_list[i].values()
            where_para_list[i]['machine_type'] = "'" + list(aa)[0] + "'"
        if list(where_para_list[i].values())[0] == None:
            where_para_list.remove(where_para_list[i])

    if where_para_list == []:
        where_para_list = None


    machine_detail = dto.getMachineTable(head='*', where_para=where_para_list, order_para=orderByUsageStatus, limit_para=pagesize, offset_para=offset)

    datalist = []
    for detail in machine_detail:
        datalist.append(
            {
                "rowid": detail[0],
                "hdm_ip": detail[1],
                "manage_ip": detail[2],
                "password": detail[3],
                "machine_type": detail[4],
                "usage_status": detail[5],
                "booking_status": detail[6],
                "solution_id": detail[7],
                "owner": detail[8],
                "useage_start_time": detail[9],
                "useage_end_time": detail[10],
                "city": detail[11],
                "location": detail[12],
                "booking_start_time": detail[13],
                "booking_end_time": detail[14],
                "is_delete": detail[15]
            }
        )

    machine_total = dto.getMachineTable(where_para=where_para_list)


    machine_dict = {'machineInfoList': datalist}
    machine_dict.update({'total': machine_total[0][0]})
    return machine_dict


def insert_machine_info(request_body):

    result_dict = json.loads(request_body)
    for result in result_dict['machineInfoList']:
        hdm_ip_value = result["hdm_ip"] if "hdm_ip" in result else None
        manage_ip_value = result["manage_ip"] if "manage_ip" in result else None
        password_value = result["password"] if "password" in result else None
        machine_type_value = result["machine_type"] if "machine_type" in result else None
        usage_status_value = result["usage_status"] if "usage_status" in result else None
        booking_status_value = result["booking_status"] if "booking_status" in result else None
        solution_id_value = result["solution_id"] if "solution_id" in result else None
        owner_value = result["owner"] if "owner" in result else None
        useage_start_time_value = result["useage_start_time"] if "useage_start_time" in result else None
        useage_end_time_value = result["useage_end_time"] if "useage_end_time" in result else None
        city_value = result["city"] if "city" in result else None
        location_value = result["location"] if "location" in result else None
        booking_start_time_value = result["booking_start_time"] if "booking_start_time" in result else None
        booking_end_time_value = result["booking_end_time"] if "booking_end_time" in result else None
        is_delete_value = result["is_delete"] if "is_delete" in result else None

        result = dto.insertMachineTable(hdm_ip_value, manage_ip_value, password_value, machine_type_value,
                                        usage_status_value, booking_status_value, solution_id_value, owner_value,
                                        useage_start_time_value, useage_end_time_value, city_value, location_value,
                                        booking_start_time_value, booking_end_time_value, is_delete_value)
    return result


def modify_machine_info(request_body):

    result = json.loads(request_body)

    for machineDict in result['machineInfoList']:
        update_sql_list = []
        for key ,value in machineDict.items():
            if key != 'rowid' and type(value) == type(""):
                update_sql_list.append(" " + key + " = " + "'" + value + "'")
            if key != 'rowid' and type(value) == type(1):
                update_sql_list.append(" " + key + " = " + str(value))
        update_sql = ','.join(update_sql_list)

        result = dto.modifyMachineTable(machineDict['rowid'],update_sql)
    return result


def del_machine_info(rowid):
    result = dto.delMachineTable(str(rowid))
    return result


def insert_solution_info(request_body):

    result = json.loads(request_body)
    for result_dict in result['solution_info']:
        solution_name_value = result_dict["solution_name"] if "solution_name" in result_dict else None
        tc_name_value = result_dict["tc_name"] if "tc_name" in result_dict else None
        result = dto.insertSolutionTable(solution_name_value, tc_name_value)
    return result


def get_solution_info(pagesize,offset):

    solution_detail = dto.getSolutionTable(head='*', limit_para=pagesize, offset_para=offset)

    datalist = []
    for detail in solution_detail:
        datalist.append(
            {
                "rowid": detail[0],
                "solution_name": detail[1],
                "tc_name": detail[2]
            }
        )

    solution_total = dto.getSolutionTable()


    solution_dict = {'solution_info': datalist}
    solution_dict.update({'total': solution_total[0][0]})
    return solution_dict

def get_solution_name(rowid):

    solution_detail = dto.getSolutionTable(head='*', where_para="rowid=" + str(rowid))

    datalist = {}
    for detail in solution_detail:
        datadict = {
            "rowid": detail[0],
            "solution_name": detail[1],
            "tc_name": detail[2]
        }

    return datadict

def modify_solution_info(request_body):

    result = json.loads(request_body)

    for solutionDict in result['solutionInfo']:
        update_sql_list = []
        for key ,value in solutionDict.items():
            if key != 'rowid' and type(value) == type(""):
                update_sql_list.append(" " + key + " = " + "'" + value + "'")
            if key != 'rowid' and type(value) == type(1):
                update_sql_list.append(" " + key + " = " + str(value))
        update_sql = ','.join(update_sql_list)

        result = dto.modifySolutionTable(solutionDict['rowid'],update_sql)
    return result



def del_solution_info(rowid):
    result = dto.delSolutionTable(str(rowid))
    return result


def insert_city_info(request_body):

    result = json.loads(request_body)
    for result_dict in result['city_info']:
        city_name_value = result_dict["city_name"] if "city_name" in result_dict else None
        result = dto.insertCityTable(city_name_value)
    return result


def modify_city_info(request_body):

    result = json.loads(request_body)

    for cityDict in result['city_info']:
        update_sql_list = []
        for key ,value in cityDict.items():
            if key != 'rowid' and type(value) == type(""):
                update_sql_list.append(" " + key + " = " + "'" + value + "'")
            if key != 'rowid' and type(value) == type(1):
                update_sql_list.append(" " + key + " = " + str(value))
        update_sql = ','.join(update_sql_list)

        result = dto.modifyCityTable(cityDict['rowid'],update_sql)
    return result


def get_city_info(pagesize,offset):

    city_detail = dto.getCityTable(head='*', limit_para=pagesize, offset_para=offset)

    datalist = []
    for detail in city_detail:
        datalist.append(
            {
                "rowid": detail[0],
                "city_name": detail[1]
            }
        )

    city_total = dto.getCityTable()


    city_dict = {'city_info': datalist}
    city_dict.update({'total': city_total[0][0]})
    return city_dict

def get_city_name(rowid):

    city_detail = dto.getCityTable(head='*', where_para="rowid=" + str(rowid))

    datalist = {}
    for detail in city_detail:
        datadict = {
            "rowid": detail[0],
            "city_name": detail[1]
        }

    return datadict


def del_city_info(rowid):
    result = dto.delCityTable(str(rowid))
    return result