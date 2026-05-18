import os
import json
import sys

#specify a file name
FILE_NAME = "tasks.json"

def menu():
    while True:
        decision = input("choose one of options:\n 1. List tasks\n 2. Filter tasks by status\n 3. Add new task\n 4. Change status\n 5. Remove task.\n 6. Edit task descrpiton\n 7. Close")
        loaded_tasks = load_tasks_list()


        if decision == "1":
            show_tasks(loaded_tasks)

        
        elif decision == "2":
            filter_tasks_by_status(loaded_tasks)
           

        elif decision == "3":
            new_task = input("what would you like to add?")
            write_tasks(loaded_tasks, new_task)


        elif decision == "4":
            set_the_status(loaded_tasks)

        
        elif decision == "5":
            remove_task(loaded_tasks)

        elif decision == "6":
            edit_task_description(loaded_tasks)


        elif decision == "7":
            sys.exit()


        else:
            print("No such option, try again")





# check wheter the file exists, if not - load empty list
def load_tasks_list():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


# introducing new feature for listing tasks by its status
# function can serve also legacy capitalized 'Done' status
def filter_tasks_by_status(loaded_tasks):
    try:
            decision = int(input("\nWhich status would you like to filter: \n1. To-do\n2. In-progress\n3. Done"))
                    
            if decision == 1:
                filter_tasks_by_status_local(loaded_tasks, "to-do")

            elif decision == 2:
               filter_tasks_by_status_local(loaded_tasks, "in-progress")

            elif decision == 3:
                filter_tasks_by_status_local(loaded_tasks, "done")

            else:
                print("\n-----------START-----------")
                print("Incorrect option, try again")
                print("-----------END-----------\n")
            
    except ValueError:
        print("\nIncorrect type, type an integer\n")


#unifing filtering operations, and making one general function for it
def filter_tasks_by_status_local(loaded_tasks, task_status):
    print("\n-----------START-----------")
    for index, task in enumerate(loaded_tasks, start=1):
        
        if task.get('status') is None:
            continue

        if (task["status"]).lower() == task_status:
            print(f"{index}. {(task['task']).capitalize()} | status: {task['status']}")
    print("-----------END-----------\n")




# showing tasks in order
# removing pending - done segmentation, listing compatible with "status" instead
def show_tasks(loaded_tasks):
    if loaded_tasks == []:
        print("Woho! Nothing to be done for now...")
        return

    try:
        print("\n-----------START-----------")
        for index, task in enumerate(loaded_tasks, start=1):

            if task.get('status') is None:
                print(f"{index}. {(task['task']).capitalize()} | isDone: {task['isDone']}")
            
            else:
                print(f"{index}. {(task['task']).capitalize()} | status: {task['status']}")
        
        print("-----------END-----------\n")

    except KeyError:
        print(f"legacy task: {task}")
        print("-----------END-----------\n")
        pass

# appending new tasks at the bottom
# instead isDone, changing the key naming to 'status' and by default setting it to to_do 
def write_tasks(file_from_load_tsk, new_task):
    file_from_load_tsk.append({"task": new_task, "status": "to-do"})
    save_task_file(file_from_load_tsk)
    print(f"task added: {new_task}")



# saving the file
def save_task_file(file):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(file, f, indent=4, ensure_ascii=False)



# removing given tasks
# shortening the loaded_tasks[index_for_removal -1]["task"] to pop method
def remove_task(loaded_tasks):
    
    if loaded_tasks == []:
        print("Since list is empty, there is no task to be removed!\n")
        return

    show_tasks(loaded_tasks)

    try:
        index_for_removal = int(input("Which task would you like to remove from the list?"))

        if index_for_removal <= 0 or index_for_removal > len(loaded_tasks):
            print(f"\nMake sure that integer chosen is bigger than 0 and it fits in current amount of tasks {len(loaded_tasks)}\n")

        else:
            print(f"task '{loaded_tasks[index_for_removal -1]["task"]}' has been succesfully removed from the list\n")
            loaded_tasks.pop(index_for_removal -1)
            save_task_file(loaded_tasks)


    except ValueError:
        print("\nIncorrect type, type an integer\n")


#changing the name of the function from complete_task to set_the_status
# giving option of setting the status according to user needs. Also option of reverting the status is possible now
# introducting in progress functionality
# marking task as done, instead of setting True or False value to the isDone parameter
# new rollout changes capitalized 'Done' to 'done' in terms of status
def set_the_status(loaded_tasks):

    if loaded_tasks == []:
        print("Woho! Nothing to be done for now...")
        return

    
    show_tasks(loaded_tasks)
    

    try: 
        index_for_completion = int(input("Choose task for changing status"))
        
        if index_for_completion <= 0 or index_for_completion > len(loaded_tasks):
            print(f"\nMake sure that integer chosen is bigger than 0 and it fits in current amount of tasks: {len(loaded_tasks)}\n")

        else:
            try:
                decision = int(input("\n1. To-do\n2. In-progress\n3. Done"))

                
                if decision == 1:
                    set_the_status_local(loaded_tasks, index_for_completion, "to-do")

                elif decision == 2:
                    set_the_status_local(loaded_tasks, index_for_completion, "in-progress")

                elif decision == 3:
                    set_the_status_local(loaded_tasks, index_for_completion, "done")

                else: 
                    print("\nOnly options 1, 2 and 3 are valid. Try again\n")
            
            except ValueError:
                print("\nIncorrect type, type integer\n")
    
    except ValueError:
        print("\nIncorrect type, type integer\n")



# setting one general function to run inside set_the_status for each condition, allowing to avoid repeatitions in code
def set_the_status_local(loaded_tasks, index_for_completion, status_to_be_set):
    if loaded_tasks[ index_for_completion -1 ].get("status") is None:
        loaded_tasks[ index_for_completion -1 ].pop('isDone')
        loaded_tasks[ index_for_completion -1 ]["status"] = status_to_be_set
        print(f"\nStatus set as '{status_to_be_set}' for: ({loaded_tasks[index_for_completion -1]["task"]})\n")
        save_task_file(loaded_tasks)
        
    else:
        loaded_tasks[ index_for_completion -1 ]["status"] = status_to_be_set
        print(f"\nStatus set as '{status_to_be_set}' for: ({loaded_tasks[index_for_completion -1]["task"]})\n")
        save_task_file(loaded_tasks)


# edit description for the already added task
def edit_task_description(loaded_tasks):
    
    if loaded_tasks == []:
        print("Since list is empty, there is no task where we can change the status!\n")
        return

    show_tasks(loaded_tasks)


    try:
        index_for_changing_status = int(input("On which task would you like to change description?"))

        if index_for_changing_status <= 0 or index_for_changing_status > len(loaded_tasks):
            print(f"\nMake sure that integer chosen is bigger than 0 and it fits in current amount of tasks: {len(loaded_tasks)}\n")
        
        else:
            while True:
                new_description = input(f"Type your new description for task: {loaded_tasks[index_for_changing_status -1]["task"]}")
                
                if new_description.strip() == "":
                    print("You cannot leave empty space as description\n")
                
                else:
                    loaded_tasks[index_for_changing_status -1]["task"] = new_description
                    save_task_file(loaded_tasks)
                    print("Description has been changed!")
                    break

    except ValueError:
        print("\nIncorrect type, type integer\n")




if __name__ == "__main__":
    menu()





