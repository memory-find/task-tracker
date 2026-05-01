print("Welcome to task-tracker")

tasks = []

def add_task(task_name):
    tasks.append({"name": task_name, "done": False})
    print(f"dodano zadanie {task_name}")

add_task("Learn git!")

print("zadania: ", tasks)

