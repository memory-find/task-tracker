import os
import json

# objectives to accomplish:
# load contents of the task list from the file if the file exists
# if it doesn't - create new file for that purpose
# allow to append tasks to the end of the list

TASKS_FILE_NAME = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE_NAME):
        return []
    
    with open(TASKS_FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(TASKS_FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


def add_task(tasks, task_name):
    tasks.append({"name": task_name, "done": False})
    save_tasks(tasks)
    print(f"dodano zadanie {task_name}")

tasks = load_tasks()
add_task(tasks, "Nauczyć się gita i jsona!")
print("zadania: ", tasks)
    