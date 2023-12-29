"""very functional utilities"""
import sys
import uuid
from os import path, system, getlogin, remove
from subprocess import CalledProcessError, CompletedProcess, run, PIPE
from time import sleep
import win32security
from constants import lang, LOGO

def is_task_completed(task_name):
    """Check if the scheduled task is completed."""
    result = run(f'schtasks /Query /TN "{task_name}" /FO LIST', shell=True, stdout=PIPE, stderr=PIPE, text=True, check=True)
    return "Ready" in result.stdout or "Could not start" in result.stdout


def schedule(command: str):
    task_name = f"Task_{uuid.uuid4()}"  # Unique task name
    batch_file = f"{task_name}.bat"
    batch_file_path = path.abspath(batch_file)
    # Write command to a batch file
    with open(batch_file, "w", encoding="utf_8") as file:
        _ = file.write(command)

    # Create, run, and delete the task
    _ = run(
        f'schtasks /Create /SC ONCE /TN "{task_name}" /TR "{path.abspath(batch_file)}" /ST:00:00 /RL HIGHEST /F',
        shell=True, check=True
    )
    _ = run(f'schtasks /Run /TN "{task_name}"', shell=True, check=True)
    while not is_task_completed(task_name):
        sleep(0.5)  # Check every 0.5 seconds

    # Delete the task
    run(f'schtasks /Delete /TN "{task_name}" /F', shell=True, check=True)

    # Clean up the batch file
    if path.exists(batch_file_path):
        sleep(1)  # Adding a delay to ensure the file is not in use
        try:
            remove(batch_file_path)
        except OSError as e:
            print(f"Failed to delete batch file: {e}")
    else:
        print(f"Batch file not found: {batch_file_path}")


def get_appx_package(name_pattern: str):
    """Gets APPX package location using powershell"""
    result: CompletedProcess[str] = run(
        [
            "powershell",
            "-Command",
            f"Get-AppxPackage -Name '{name_pattern}' | Select-Object -ExpandProperty InstallLocation",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def print_logo():
    """Prints the logo of BetterRTX"""
    _ = system("cls")

    print(LOGO)


def check_path_exists(file_path: str, found_message: str, not_found_message: str):
    if path.exists(file_path):
        print(found_message)
    else:
        print(not_found_message)
        sleep(10)
        sys.exit()

def take_ownership(file_path):
    login = getlogin()
    run(['takeown', '/f', file_path], check=True)
    run(['icacls', file_path, '/grant', f'{login}:F'], check=True)
    sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
    # Convert user name to SID
    sid, _, _ = win32security.LookupAccountName("", login)

    # Set the owner in the security descriptor
    sd.SetSecurityDescriptorOwner(sid, 0)

    # Apply the new security descriptor to the file
    win32security.SetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION, sd)

def perform_action(
    file_path: str, action_message: str, action_command: str, error_message: str
):
    if path.exists(file_path):
        print(action_message)
        take_ownership(file_path=file_path)
        try:
            schedule(action_command)
        except CalledProcessError:
            print(error_message)


def print_success():
    print(
        lang['doneHappyFace'],
        "_______________________________________________________________________",
        "\n",
        lang['thanks'],
        lang['resourcePackNotice'],
        lang['inviteLink'],
        lang['helpChannelLink'],
        sep="\n")
