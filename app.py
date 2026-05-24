import os
import json
import sys
import datetime

#specify a file name
FILE_NAME = "tasks.json"

def menu():
    loaded_tasks_for_conversion = load_tasks_list()
    loaded_tasks_after_conversion = data_migration(loaded_tasks_for_conversion)
    save_task_file(loaded_tasks_after_conversion)

    while True:
        decision = input("choose one of options:\n 1. List tasks\n 2. Filter tasks by status or priority\n 3. Add new task\n 4. Change status\n 5. Remove task.\n 6. Edit task descrpiton\n 7. Change priority\n 8. Set due to date\n 9. Close")
        loaded_tasks = load_tasks_list()


        if decision == "1":
            show_tasks(loaded_tasks)

        
        elif decision == "2":
            filter_tasks_by_status_or_prio_dueDate(loaded_tasks)
           

        elif decision == "3":
            new_task = input("what would you like to add?").strip()
            write_tasks(loaded_tasks, new_task)


        elif decision == "4":
            set_the_status(loaded_tasks)

        
        elif decision == "5":
            remove_task(loaded_tasks)

        elif decision == "6":
            edit_task_description(loaded_tasks)


        elif decision == "7":
            change_priority(loaded_tasks)


        elif decision == "8":
            due_date_set(loaded_tasks)


        elif decision == "9":
            sys.exit()


        else:
            print("No such option, try again")


# data migration function to be run once before menu loop is initiated, while initiated, isDone key is being replaced by status
# legacy tasks without priority will have medium priority assigned by default
# legacy tasks will have dueDate to 'not-set' by default
def data_migration(loaded_tasks):
    
    for record in loaded_tasks:

        if record.get('status') is None:
            if record['isDone'] == "True":
                record.pop('isDone')
                record['status'] = "done"
            
            elif record['isDone'] == "False":
                record.pop('isDone')
                record['status'] = "to-do"

        if record.get('priority') is None:
            record['priority'] = "medium"

        if record.get('dueDate') is None:
            record['dueDate'] = "not-set"
        
        

    return loaded_tasks


# check wheter the file exists, if not - load empty list
def load_tasks_list():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


# introducing new feature for listing tasks by its status
# function can serve also legacy capitalized 'Done' status
def filter_tasks_by_status_or_prio_dueDate(loaded_tasks):
    
    try:
    
        status_or_prio_dueDate = int(input("\nWhich filtering mechanism would you like to apply?: \n1. Status\n2. Priority\n3. Due Date"))    

        if status_or_prio_dueDate == 1:

            try:
                    decision_status = int(input("\nWhich status would you like to filter: \n1. To-do\n2. In-progress\n3. Done"))
                            
                    if decision_status == 1:
                        filter_tasks_by_status_local(loaded_tasks, "to-do")

                    elif decision_status == 2:
                        filter_tasks_by_status_local(loaded_tasks, "in-progress")

                    elif decision_status == 3:
                        filter_tasks_by_status_local(loaded_tasks, "done")

                    else:
                        print("\n-----------START-----------")
                        print("Incorrect option, try again")
                        print("-----------END-----------\n")
                    
            except ValueError:
                print("\nIncorrect type, type an integer\n")


        elif status_or_prio_dueDate == 2:
            
            try:
                    decision_prio = int(input("\nWhich priority would you like to filter: \n1. low\n2. medium\n3. high"))
                            
                    if decision_prio == 1:
                        filter_tasks_by_priority_local(loaded_tasks, "low")

                    elif decision_prio == 2:
                        filter_tasks_by_priority_local(loaded_tasks, "medium")

                    elif decision_prio == 3:
                        filter_tasks_by_priority_local(loaded_tasks, "high")

                    else:
                        print("\n-----------START-----------")
                        print("Incorrect option, try again")
                        print("-----------END-----------\n")
                    
            except ValueError:
                print("\nIncorrect type, type an integer\n")

        elif status_or_prio_dueDate == 3:
            filter_by_due_date(loaded_tasks)

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
        
        if (task["status"]).lower() == task_status:
            print(f"{index}. {(task['task']).capitalize()} | status: {task['status']}")
    print("-----------END-----------\n")



#unifiyng filtering by priority
def filter_tasks_by_priority_local(loaded_tasks, task_priority):
    print("\n-----------START-----------")
    for index, task in enumerate(loaded_tasks, start=1):
        
        if (task["priority"]).lower() == task_priority:
            print(f"{index}. {(task['task']).capitalize()} | status: {task['status']} | priority: {task['priority']}")
    print("-----------END-----------\n")

#function for filtering tasks by due date
def filter_by_due_date(loaded_tasks):
    loaded_tasks_local_copy = [{"task": line['task'],'status': line['status'], "dueDate": line['dueDate']} for line in loaded_tasks]
    

    task_with_dates = []
    task_with_dates_overdue = []
    task_with_date_not_set = []
    today = datetime.date.today()

    for index, task in enumerate(loaded_tasks_local_copy, start=1):

        if task['dueDate'] != "not-set":
            year, month, day = [int(x) for x in task['dueDate'].split('-')]
            task['dueDate'] = datetime.date(year, month, day)

            if task['dueDate'] < today:
                if task['status'].lower() != 'done':
                    task_with_dates_overdue.append(task)
            
            else:
                if task['status'].lower() != 'done':
                    task_with_dates.append(task)
        
        else:
            task_with_date_not_set.append(task)

    if task_with_dates_overdue != []:
        print("\nTHESE TASKS ARE OVERDUE!\n")

        for line in sorted(task_with_dates_overdue, key=lambda x: x['dueDate']):
            print(f"{(line['task']).capitalize()} | status: {line['status']} | dueDate: {line['dueDate']}")


    if task_with_dates != []:
        print("\nTASKS WITH DATES SET\n")

        for line in sorted(task_with_dates, key=lambda x: x['dueDate']):
            print(f"{(line['task']).capitalize()} | status: {line['status']} | dueDate: {line['dueDate']}")

    if task_with_date_not_set != []:
        print("\nTASKS WITHOUT DATES\n")
        
        for line in task_with_date_not_set:
            print(f"{(line['task']).capitalize()} | status: {line['status']} | dueDate: {line['dueDate']}")


# showing tasks in order
# removing pending - done segmentation, listing compatible with "status" instead
def show_tasks(loaded_tasks):
    if loaded_tasks == []:
        print("Woho! Nothing to be done for now...")
        return

    else:
        print("\n-----------START-----------")
        for index, task in enumerate(loaded_tasks, start=1):

            print(f"{index}. {(task['task']).capitalize()} | status: {task['status']} | priority: {task['priority']} | dueDate: {task['dueDate']}")

        print("-----------END-----------\n")


# appending new tasks at the bottom
# instead isDone, changing the key naming to 'status' and by default setting it to to_do 
# priority feature implementation, new tasks by default will land with new key: 'priority' and it will be set to medium
def write_tasks(file_from_load_tsk, new_task):
    file_from_load_tsk.append({"task": new_task, "status": "to-do", "priority": "medium", "dueDate": "not-set"})
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
                    loaded_tasks[index_for_changing_status -1]["task"] = new_description.strip()
                    save_task_file(loaded_tasks)
                    print("Description has been changed!")
                    break

    except ValueError:
        print("\nIncorrect type, type integer\n")


def change_priority(loaded_tasks):

    if loaded_tasks == []:
        print("Woho! Nothing to change priority for...")
        return

    
    show_tasks(loaded_tasks)
    

    try: 
        index_for_prio = int(input("Choose task for changing priority"))
        
        if index_for_prio <= 0 or index_for_prio > len(loaded_tasks):
            print(f"\nMake sure that integer chosen is bigger than 0 and it fits in current amount of tasks: {len(loaded_tasks)}\n")

        else:
            try:
                priority = int(input("\n1. low\n2. medium\n3. high"))

                
                if priority == 1:
                    set_the_prio_local(loaded_tasks, index_for_prio, "low")

                elif priority == 2:
                    set_the_prio_local(loaded_tasks, index_for_prio, "medium")

                elif priority == 3:
                    set_the_prio_local(loaded_tasks, index_for_prio, "high")

                else: 
                    print("\nOnly options 1, 2 and 3 are valid. Try again\n")
            
            except ValueError:
                print("\nIncorrect type, type integer\n")
    
    except ValueError:
        print("\nIncorrect type, type integer\n")



# setting one general function to run inside change_priority for each condition, allowing to avoid repeatitions in code
def set_the_prio_local(loaded_tasks, index_for_prio, prio_to_be_set):
    
    loaded_tasks[ index_for_prio -1 ]["priority"] = prio_to_be_set
    print(f"\nPriority set as '{prio_to_be_set}' for: ({loaded_tasks[index_for_prio -1]["task"]})\n")
    save_task_file(loaded_tasks)
        

# setting dueDate to existing records
def due_date_set(loaded_tasks):
    
    if loaded_tasks == []:
        print("Woho! Nothing to set due date for...")
        return

    
    show_tasks(loaded_tasks)

    try: 
        index_for_dueDate = int(input("Choose task for changing due date"))
        
        if index_for_dueDate <= 0 or index_for_dueDate > len(loaded_tasks):
            print(f"\nMake sure that integer chosen is bigger than 0 and it fits in current amount of tasks: {len(loaded_tasks)}\n")

        else:
            today = datetime.date.today()

            while True:
                try:
                    year, month, day = [int(x) for x in input("Type due date in <year-month-day> format").split('-')]
                    chosen_dueDate = datetime.date(year, month, day)


                    if chosen_dueDate < today:
                        print(f"\nYou cannot set dueDate older than today: ({today})")


                    else:
                        loaded_tasks[index_for_dueDate -1]['dueDate'] = chosen_dueDate.strftime(('%Y-%m-%d'))
                        save_task_file(loaded_tasks)
                        break


                except ValueError:
                    print("\nMake sure to type date in correct format '<year-month-day>'\n")


    except ValueError:
        print("\nIncorrect type, type integer\n")


if __name__ == "__main__":
    menu()





