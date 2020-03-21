import os,subprocess
#编译程序
def compile(solution_id, language):
    '''将程序编译成可执行文件'''
    language = language.lower()

    dir_work = os.path.join('work', str(solution_id))



    build_cmd = {
        "gcc":"gcc main.c -o main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE",
        "g++": "g++ main.cpp -O2 -Wall -lm --static -DONLINE_JUDGE -o main",
        "java": "javac Main.java",
        "python3": 'python -m py_compile main.py',
    }



    if language not in build_cmd.keys():
        return False
    p = subprocess.Popen(
        build_cmd[language],
        cwd=dir_work,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    out, err = p.communicate()  # 获取编译错误信息
    err_txt_path = os.path.join('work', str(solution_id), 'error.txt')
    f = open(err_txt_path, 'w')
    f.write(str(err, encoding='gbk'))
    f.write(str(out, encoding='gbk'))
    f.close()
    if p.returncode == 0:  # 返回值为0,编译成功
        #print('编译成功')
        return True
    # update_compile_info(solution_id, err + out)  # 编译失败,更新题目的编译错误信息
    return False