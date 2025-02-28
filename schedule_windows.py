import os
import sys
from datetime import datetime, timedelta
import win32com.client
import getpass

def create_task_scheduler():
    """Create a Windows Task Scheduler task to run the birthday emailer daily"""
    
    # Get the current user's username
    username = getpass.getuser()
    
    # Get the full path of the Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    emailer_path = os.path.join(script_dir, "birthday_emailer.py")
    python_path = sys.executable
    
    # Create a Windows Script Host Shell Object
    shell = win32com.client.Dispatch('WScript.Shell')
    
    # Create the scheduler object
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    
    # Get the task folder
    root_folder = scheduler.GetFolder('\\')
    
    # Create the task definition
    task_def = scheduler.NewTask(0)
    
    # Set general info
    task_def.RegistrationInfo.Description = 'Runs the birthday emailer script daily'
    task_def.Principal.LogonType = 3  # TASK_LOGON_INTERACTIVE_TOKEN
    task_def.Settings.Enabled = True
    task_def.Settings.AllowDemandStart = True
    
    # Create trigger (daily at 9 AM)
    start_time = datetime.now() + timedelta(minutes=1)  # Start from tomorrow
    TASK_TRIGGER_DAILY = 2
    trigger = task_def.Triggers.Create(TASK_TRIGGER_DAILY)
    trigger.StartBoundary = start_time.strftime('%Y-%m-%dT09:00:00')
    trigger.DaysInterval = 1
    
    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.Path = python_path
    action.Arguments = f'"{emailer_path}"'
    
    # Register the task
    task_name = "Birthday_Email_Sender"
    try:
        root_folder.RegisterTaskDefinition(
            task_name,
            task_def,
            6,  # TASK_CREATE_OR_UPDATE
            None,  # userid
            None,  # password
            3  # TASK_LOGON_INTERACTIVE_TOKEN
        )
        print(f"Task '{task_name}' has been created successfully!")
        print("The birthday emailer will run automatically at 9 AM every day.")
    except Exception as e:
        print(f"Error creating task: {str(e)}")

if __name__ == "__main__":
    create_task_scheduler() 