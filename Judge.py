# -*- coding: utf-8 -*-
import os
import subprocess
from Compile import compile
import dbread as db

#嵌套在线程中
def worker(solution_id,problem_id,language,user_id,data_count):
    result = run(
        problem_id,
        solution_id,
        language,
        data_count,
        user_id)

    print(
        "%s result %s" % (
            result[
                'solution_id'],
            result[
                'result']))

    return result

#运行程序
def run(problem_id, solution_id, language, data_count, user_id):
    time_limit, mem_limit = 1000, 32768
    program_info = {
        "solution_id": solution_id,
        "problem_id": problem_id,
        "take_time": 0,
        "take_memory": 0,
        "user_id": user_id,
        "result": 0,
    }
    result_code = {
        "Waiting": 0,
        "Accepted": 1,
        "Time Limit Exceeded": 2,
        "Memory Limit Exceeded": 3,
        "Wrong Answer": 4,
        "Runtime Error": 5,
        "Output limit": 6,
        "Compile Error": 7,
        "Presentation Error": 8,
        "System Error": 9,
        "Judging": 10,
    }

    compile_result = compile(solution_id, language)
    if compile_result is False:  # 编译错误
        program_info['result'] = result_code["Compile Error"]
        return program_info


    if data_count == 0:  # 没有测试数据
        program_info['result'] = result_code["System Error"]
        return program_info
    result = judge(
        solution_id,
        problem_id,
        data_count,
        time_limit,
        mem_limit,
        program_info,
        result_code,
        language)
    return result





#对运行时间和内存结果进行判断（未做）
def judge(solution_id, problem_id, data_count, time_limit,
          mem_limit, program_info, result_code, language):
    '''评测编译类型语言'''
    max_mem = 0
    max_time = 0
    if language in ["java", 'python2', 'python3', 'ruby', 'perl']:
        time_limit = time_limit * 2
        mem_limit = mem_limit * 2
    for i in range(data_count):
        ret = judge_one_mem_time(
            solution_id,
            problem_id,
            i + 1,
            time_limit + 10,
            mem_limit,
            language)
        max_time = 888
        max_mem = 2768
        result = judge_result(problem_id, solution_id, i + 1)
        if result == False:
            continue
        if result == "Wrong Answer" or result == "Output limit":
            program_info['result'] = result_code[result]
            break
        elif result == 'Presentation Error':
            program_info['result'] = result_code[result]
        elif result == 'Accepted':
            if program_info['result'] != 'Presentation Error':
                program_info['result'] = result_code[result]
        else:
            print("judge did not get result")
    program_info['take_time'] = max_time
    program_info['take_memory'] = max_mem

    return program_info

#将输入输出放入程序中运行
def judge_one_mem_time(
        solution_id, problem_id, data_num, time_limit, mem_limit, language):
    '''评测一组数据'''
    input_path = os.path.join(
        'data', str(problem_id), 'data%sin.txt' %
        data_num)

    #print(input_path)
    try:
        input_data = open(input_path).read().encode()

    except:
        return False
    output_path = os.path.join(
        'work', str(solution_id), 'out%s.txt' %
        data_num)
    temp_out_data = open(output_path, 'w')
    if language == 'java':
        cmd = 'java Main'
        cwd =os.path.join('work',str(solution_id))
    elif language == 'python3':
        cmd = 'python main.cpython-36.pyc'
        cwd=os.path.join('work',str(solution_id),'__pycache__')
    else:
        cmd = 'main.exe'
        cwd = os.path.join('work', str(solution_id))
    # main_exe = [os.path.join('main', str(solution_id), 'main'), ]


    p = subprocess.Popen(
        cmd,
        shell=True,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    try:
        out, err = p.communicate(input=input_data,timeout=2)  # 获取编译错误信息
    except Exception as e:
        if e.__str__().__contains__("timed out"):
           db.update_solution(solution_id,2,user_id=None,problem_id=None)
        return
        # if e.__str__().__contains__("time"):

    out_txt_path = os.path.join(
        'work', str(solution_id), 'out%s.txt' %
                                  data_num)
    f = open(out_txt_path, 'w')

    f.write(out.decode().replace("\r",""))
    # print(out)
    f.write(err.decode().replace("\r",""))
    f.close()
    return True

#对输出结果进行判断
def judge_result(problem_id, solution_id, data_num):
    '''对输出数据进行评测'''
    correct_result = os.path.join(
        'data', str(problem_id), 'data%sout.txt' %
                                 data_num)
    user_result = os.path.join(
        'work', str(solution_id), 'out%s.txt' %
                                  data_num)
    try:
        correct = open(correct_result).read() # 删除\r,删除行末的空格和换行
        user = open(user_result).read()
        # print('correct')
        # print(correct)
        # print('user')
        # print(user)
    except Exception as e:
        print(e.__str__())
        return False
    if correct == user:  # 完全相同:AC
        #print("Accepted")
        return "Accepted"
    if correct.split() == user.split():  # 除去空格,tab,换行相同:PE
        #print("Presentation Error")
        return "Presentation Error"
    if correct in user:  # 输出多了
        #print("Output limit")
        return "Output limit"
    #print("Wrong Answer")
    return "Wrong Answer"  # 其他WA




