
import pymysql,configparser
import json,os
# import Judge
def connect():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    host = config['db']['host']
    port = config.read('db', 'port')
    user = config['db']['user']
    password = config['db']['password']
    database = config['db']['database']
    charset = config['db']['charset']
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset=charset
    )
    return conn

def find_unfinished_solution():
    conn = connect()
    sql = 'select id from user_code where statu=0'
    with conn.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()

    lst = []
    for i in data:
        lst.append(i[0])
    return lst



def update_solution(solution_id,statu,user_id,problem_id):
    conn = connect()
    sql ='update user_code set statu='+str(statu)+" where id="+solution_id
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()
    if int(statu)==1:
        sql_ac_user = 'update users set acnum=acnum+1 where userid='+"'"+user_id+"'"
        sql_ac_pro = 'update problem set acsum=acsum+1 where id='+"'"+str(problem_id)+"'"
        with conn.cursor() as cursor:
            cursor.execute(sql_ac_user)
            cursor.execute(sql_ac_pro)
            print(sql_ac_pro)
            conn.commit()




def get_solution(solution_id):
    conn = connect()
    sql = 'select id,userid,problemid,language,code from user_code where id='+solution_id
    sql_count = 'select iocount from problem where id='
    with conn.cursor() as cursor:
        cursor.execute(sql)
        solution = cursor.fetchall()[0]
        info = get_language(int(solution[3]))
        code = solution[4]
        cursor.execute(sql_count+str(solution[2]))
        data_count = cursor.fetchall()[0][0]
    if not os.path.exists("work/" + solution_id):
        os.mkdir("work/" + solution_id)
    with open("work/"+solution_id+"/"+"Main"+info['suffix'],"w") as f:
        f.write(code)
    solution_info = (solution_id,solution[2],info["language"],solution[1],data_count)
    return solution_info


def get_language(code):
    info = {}
    if code==1:
        info['suffix'] = '.c'
        info['language'] = "gcc"

    elif code==2:
        info['suffix'] = '.cpp'
        info['language'] = "g++"

    elif code==4:
        info['suffix'] = '.java'
        info['language'] = "java"

    else:
        info['suffix'] = '.py'
        info['language'] = "python3"
    return info



if __name__ =="__main__":
    solution = get_solution("1")
    # result = Judge.worker(*solution)
    # update_solution(statu=result['result'],solution_id="1")

