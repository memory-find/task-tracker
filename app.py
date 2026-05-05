import os
import json
import sys

#specify a file name
FILE_NAME = "tasks.json"

def menu():
    while True:
        decision = input("choose one of options:\n 1. List tasks\n 2. Add new task\n 3. Close")
        loaded_tasks = load_tasks_list()
        
        if decision == "1":
            if loaded_tasks == []:
                print("all is done!\n")

            x = 0
            for line in loaded_tasks:
                print(f"{loaded_tasks[x]["task"]}")
                x += 1
            

        elif decision == "2":
            new_task = input("what would you like to add?")
            write_tasks(loaded_tasks, new_task)

        elif decision == "3":
            sys.exit()
        
        else:
            print("No such option, try again")





# check wheter the file exists, if not - load empty list
def load_tasks_list():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

# appending new tasks at the bottom
def write_tasks(file_from_load_tsk, new_task):
    file_from_load_tsk.append({"task": new_task, "isDone": False})
    save_task_file(file_from_load_tsk)
    print(f"task added: {new_task}")

# saving the file
def save_task_file(file):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(file, f, indent=4, ensure_ascii=False)

def define_task():
    return input("What would you like to plan?")


if __name__ == "__main__":
    menu()

'''
# invoking list of tasks if exists
tasks_at_the_begining = load_tasks_list()

# taking input from a user and appending previous outputs
new_task = define_task()
write_tasks(tasks_at_the_begining, new_task)
print(f"full task list:", tasks_at_the_begining)
'''


