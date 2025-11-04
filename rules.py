def assign_task(task):
    """
    Simple automation rule:
    - If amount > 10000 → assign to Manager
    - Else → assign to Employee
    """
    if task.amount > 10000:
        task.assigned_to = "Manager"
    else:
        task.assigned_to = "Employee"
    return task
