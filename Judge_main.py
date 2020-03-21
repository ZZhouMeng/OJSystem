from queue import Queue
import threading
import time
import dbread as db
import Judge

q = Queue(10)
dblock = threading.Lock()


def put_task_into_queue():
    try:
        while True:
            lst = db.find_unfinished_solution()
            q.join()
            for i in lst:
                q.put(i)
            time.sleep(1)
    except Exception:
        start_get_task()


def judge_worker():
    try:
        while True:
            solution_id = q.get()
            solution_info = db.get_solution(str(solution_id))
            result = Judge.worker(*solution_info)
            print(result)
            db.update_solution(statu=result['result'], solution_id=str(solution_id),user_id=result['user_id'],problem_id=result['problem_id'])
            q.task_done()
            time.sleep(1)
    except Exception:
        db.update_solution(statu=11, solution_id=str(solution_id), user_id=result['user_id'],
                           problem_id=result['problem_id'])
        start_work_thread()




def start_get_task():
    t = threading.Thread(target=put_task_into_queue,name="get_task")
    #t.daemon = True
    t.start()


def start_work_thread():
    t = threading.Thread(target=judge_worker, name="get_task")
    #t.daemon = True
    t.start()


if __name__ == "__main__":


    start_get_task()
    start_work_thread()



