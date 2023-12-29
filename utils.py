import sys
import uuid
from os import path, system
from subprocess import CalledProcessError, CompletedProcess, run
from time import sleep

from constants import LOGO


def schedule(command: str):
    task_name = f"Task_{uuid.uuid4()}"  # Unique task name
    batch_file = f"{task_name}.bat"

    # Write command to a batch file
    with open(batch_file, "w") as file:
        _ = file.write(command)

    # Create, run, and delete the task
    _ = run(
        f'schtasks /Create /SC ONCE /TN "{task_name}" /TR "{path.abspath(batch_file)}" /ST 00:00 /RL HIGHEST /F',
        shell=True,
    )
    _ = run(f'schtasks /Run /TN "{task_name}"', shell=True)
    _ = run(f'schtasks /Delete /TN "{task_name}" /F', shell=True)

    # Clean up the batch file
    if path.exists(batch_file):
        try:
            _ = run(["del", "/F", f'"{batch_file}"'], shell=True)
        except Exception as e:
            print(f"Failed to delete batch file: {e}")


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


def perform_action(
    file_path: str, action_message: str, action_command: str, error_message: str
):
    if path.exists(file_path):
        print(action_message)
        try:
            schedule(action_command)
        except CalledProcessError:
            print(error_message)


def print_success(lang: dict[str, str]):
    print(
        f"{lang['doneHappyFace']}",
        "_______________________________________________________________________",
        "\n",
        f"{lang['thanks']}",
        f"{lang['resourcePackNotice']}",
        f"{lang['inviteLink']}",
        f"{lang['helpChannellink']}",
        sep="\n",
    )
