import os
import json
import sys

#specify a file name
FILE_NAME = "tasks.json"

def menu():
    while True:
        decision = input("choose one of options:\n 1. List tasks\n 2. Add new task\n 3. Complete task\n 4. Close")
        loaded_tasks = load_tasks_list()


        if decision == "1":
            show_tasks(loaded_tasks)
           

        elif decision == "2":
            new_task = input("what would you like to add?")
            write_tasks(loaded_tasks, new_task)



        elif decision == "3":
            complete_task(loaded_tasks)


        elif decision == "4":
            sys.exit()


        else:
            print("No such option, try again")





# check wheter the file exists, if not - load empty list
def load_tasks_list():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)
    
# showing tasks in order
def show_tasks(loaded_tasks):
    if loaded_tasks == []:
        print("Woho! Nothing to be done for now...")
        return

    print("\n-----------START-----------")
    for index, task in enumerate(loaded_tasks, start=1):
        
        if loaded_tasks[index - 1]["isDone"] is False:
            status = "Pending"
        else:
            status = "Done"

        print(f"{index}. {loaded_tasks[index - 1]['task']} ----> {status}") 
    print("-----------END-----------\n")

# appending new tasks at the bottom
def write_tasks(file_from_load_tsk, new_task):
    file_from_load_tsk.append({"task": new_task, "isDone": False})
    save_task_file(file_from_load_tsk)
    print(f"task added: {new_task}")

# saving the file
def save_task_file(file):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(file, f, indent=4, ensure_ascii=False)


# marking task as completed
def complete_task(loaded_tasks):

    if loaded_tasks == []:
        print("Woho! Nothing to be done for now...")

    
    show_tasks(loaded_tasks)
    

    try: 
        index_for_completion = int(input("Which task are we closing?"))
        
        if index_for_completion <= 0 or index_for_completion > len(loaded_tasks):
            print(f"\nMake sure that integer chosen is bigger than 0 and it fits in current amount of tasks {len(loaded_tasks)}\n")

        else:    
            loaded_tasks[ index_for_completion -1 ]["isDone"] = True
            print(f"\nCongrats on finishing the task ({loaded_tasks[index_for_completion -1]["task"]})\n")
            save_task_file(loaded_tasks)
    
    except ValueError:
        print("\nIncorrect type, type integer\n")



if __name__ == "__main__":
    menu()





