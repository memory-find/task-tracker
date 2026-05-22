# Task Tracker


Simple CLI task tracker written in Python. version 2.0 - 17.05.2026



## Features
- List tasks
- Filter tasks by status
- Add new task
- Complete task
- Remove task
- Edit task descrpiton
- Legacy data types migration

## Fixes history
- 16.05
    * Fix removes bugs with empty lists. This means taht when we have empty list, no further logic is applied on remove_task and complete_task function, return is used instead.
- 17.05
    * Version 2.0 introduces new status key, with three possible values: to-do, in-progress and done. Version maintains compatibility with previous version, providing service for legacy isDone key. 
    * New functionality of filtering tasks by status (to-do, in-progress, done)
- 18.05
    * Version 3.0 indtoduces functionality of editing satus for the existing task.
-22.05
    * Version 4.0 introduces data migration and simplifies function logic so they expect data to be in unified format

## Run
```bash
python app.py
```