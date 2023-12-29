""" BetterRTX installer written in python and betterfied"""
import sys
from ctypes import WinDLL, windll
from os import getcwd, path, remove
from subprocess import CalledProcessError
from time import sleep
from typing import List

from requests import get
from utils import (check_path_exists, get_appx_package, perform_action,
                   print_logo, print_success, schedule)
from constants import UNINSTALL_STUB, UNINSTALL_TONEMAPPING, URL, lang


def select_installer_location():
    """Selects installer location or uses auto mode."""
    while True:  # Loop until a valid install location is found
        auto = len(sys.argv) > 2
        if not auto:
            print_logo()
            print(
                f"{lang['installerLocationChoice']}\n",  # Choose installation location
                f"{lang['installerLocationChoice1']}\n",  # Minecraft Bedrock Edition
                f"{lang['installerLocationChoice2']}\n",
            )  # Minecraft Preview Edition
            location = int(input(f"{lang['installerLocationPrompt']}: "))  # Select
        else:
            print("Automatic Mode Enabled")
            location = sys.argv[1]
        installlocation: str | None = None
        if location == 1:
            installlocation = get_appx_package("Microsoft.MinecraftUWP*")
        elif location == 2:
            installlocation = get_appx_package("Microsoft.MinecraftWindowsBeta*")
        else:
            print(lang["installerLocationInvalid"])
            sleep(5)
            continue  # Continue the loop to prompt again

        if installlocation is not None:
            return installlocation  # Valid install location found

        # If installlocation is None, print an error message and prompt again
        print("Unable to find a valid installation location. Please try again.")
        sleep(2)

        if auto:
            # In automatic mode, exit if a valid location isn't found
            sys.exit("Exiting: No valid installation location found in automatic mode.")


def check_for_minecraft(location: str):
    """Check if the installation location exists"""
    print_logo()
    print(lang["checkingForMinecraft"])
    if not path.exists(location):
        print(
            f'{lang["MinecraftCheckFail"]}\n',
            f'{lang["MinecraftPleaseInstall"]}\n',
            "https://www.microsoft.com/en-us/p/minecraft-for-windows-10/9nblggh2jhxj",
        )
        sleep(10)
        sys.exit()
    else:
        print(lang["MinecraftCheckPass"])


def uninstall(
    stub_new: str,
    tone_mapping_new: str,
    rtx_stub: str,
    tone_mapping: str,
    materials: str,
):
    """uninstalls betterRTX"""
    print(f"{lang['uninstalling']}\n", f"{lang['downloadingvanilla']}\n")
    # Downloading and saving the new_stub file
    response = get(UNINSTALL_STUB, timeout=2000)
    if response.status_code == 200:
        with open(stub_new, "wb") as file:
            file.write(response.content)
    # Downloading and saving the new_tonemapping file
    response = get(UNINSTALL_TONEMAPPING, timeout=2000)
    if response.status_code == 200:
        with open(tone_mapping_new, "wb") as file:
            file.write(response.content)

        if path.exists(rtx_stub):
            print(lang["removingStub"])
            try:
                schedule(f'del /F "{rtx_stub}"')
            except CalledProcessError:
                print("Failed to remove RTX stub.")

        if path.exists(tone_mapping):
            print(lang["removingTonemapping"])
            try:
                schedule(f'del /F "{tone_mapping}"')
            except CalledProcessError:
                print("Failed to remove tone mapping.")

        print(lang["insertingStub"])
        try:
            schedule(f'copy /Y /V "{stub_new}" "{materials}"')
        except CalledProcessError:
            print("Failed to insert new stub.")

        print(lang["insertingTonemapping"])
        try:
            schedule(f'copy /Y /V "{tone_mapping_new}" "{materials}"')
        except CalledProcessError:
            print("Failed to insert new tone mapping.")
    remove(tone_mapping_new)
    remove(stub_new)
    print(
        f"\n{lang['doneSadFace']}\n",
        "_______________________________________________________________________",
        "\n\n",
        f"{lang['sorryToSeeYouGo']}\n",
        f"{lang['inviteLink']}\n",
        f"{lang['helpChannellink']}\n",
    )
    sleep(10)
    sys.exit()


def download_from_server(stub_new: str, tone_mapping_new: str):
    """Downloads betterRTX from server"""
    releases = []
    response = get(URL, timeout=10000)
    releases = response.json()
    if not releases:
        print("No releases found.")
        # Handle the scenario where no releases are found
        return
    print(lang["versionSelect"])
    for i, release in enumerate(releases, start=1):
        print(f"{i}): {release['name']}")
    select_version = input(f"{lang['selectVersionPrompt']}: ")
    # Ensure the selected version is valid
    if 0 > int(select_version) >= len(releases):
        print("Invalid version selected.")
        # Handle invalid selection
        return
    version = releases[int(select_version) - 1]
    new_stub_url = version["stub"]
    new_tone_mapping_url = version["tonemapping"]
    print(f"\n{lang['downloadingBins']}")
    response = get(new_stub_url, timeout=1000)
    if response.status_code == 200:
        with open(stub_new, "wb") as file:
            file.write(response.content)
    # Downloading and saving the new_tone_mapping file
    response = get(new_tone_mapping_url, timeout=1000)
    if response.status_code == 200:
        with open(tone_mapping_new, "wb") as file:
            file.write(response.content)
    print(f"{lang['doneDownloading']}\n")


def installation_method(
    stub_new: str,
    tone_mapping_new: str,
    rtx_stub: str,
    tone_mapping: str,
    materials: str,
):
    """Selects installation method"""
    print_logo()
    print(
        f"{lang['installation_method']}",
        f"{lang['serverInstall']}",
        f"{lang['localInstall']}",
        f"{lang['uninstall']}",
        f"{lang['exit']}",
        sep="\n",
    )
    selection: str = input(f"{lang['installSelectionKeyword']}: ")
    match selection:
        case "1":  # install from server
            print_logo()
            download_from_server(stub_new, tone_mapping_new)
        case "2":  # install from local files
            pass
        case "3":  # uninstall
            print_logo()
            uninstall(stub_new, tone_mapping_new, rtx_stub, tone_mapping, materials)
        case "4":  # exit
            sys.exit()
        case _:  # invalid selection
            print(lang["installerOptionNotFound"])
            sleep(10)
            sys.exit()

    # Check for new stub and tone mapping
    check_path_exists(
        file_path=stub_new,
        found_message=lang["stubFound"],
        not_found_message=lang["stubNotFound"],
    )
    check_path_exists(
        file_path=tone_mapping_new,
        found_message=lang["tonemappingFound"],
        not_found_message=lang["tonemappingNotFound"],
    )

    print("\n\n")

    # Perform removal actions
    perform_action(
        file_path=rtx_stub,
        action_message=lang["removingStub"],
        action_command=f'del /F "{rtx_stub}"',
        error_message="Failed to remove RTX stub.",
    )
    perform_action(
        file_path=tone_mapping,
        action_message=lang["removingTonemapping"],
        action_command=f'del /F "{tone_mapping}"',
        error_message="Failed to remove tone mapping.",
    )

    # Perform insertion actions
    perform_action(
        file_path=stub_new,
        action_message=lang["insertingStub"],
        action_command=f'copy /Y /V "{stub_new}" "{materials}"',
        error_message="Failed to insert new stub.",
    )
    perform_action(
        file_path=tone_mapping_new,
        action_message=lang["insertingTonemapping"],
        action_command=f'copy /Y /V "{tone_mapping_new}" "{materials}"',
        error_message="Failed to insert new tone mapping.",
    )

    if selection != "2":
        remove(tone_mapping_new)
        remove(stub_new)

    sleep(3)
    print_logo()
    print_success()
    sleep(10)
    sys.exit()


def is_admin() -> bool:
    """detect if app is running as admin"""
    try:
        return bool(windll.shell32.IsUserAnAdmin())
    except OSError as e:
        print(f"Error checking admin status: {e}")
        return False


def run_as_admin(argv: List[str] | None = None, debug: bool = False):
    """run app as admin if not already"""
    shell32: WinDLL = windll.shell32
    if argv is None:
        if is_admin():
            # Already an admin
            return True
        argv = sys.argv
    arguments = map(str, argv[1:]) if hasattr(sys, "_MEIPASS") else map(str, argv)
    argument_line = " ".join(arguments)
    executable = str(sys.executable)
    if debug:
        print("Command line: ", executable, argument_line)
    ret = shell32.ShellExecuteW(None, "runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None


if __name__ == "__main__":
    if is_admin():
        installation_location: str = select_installer_location()
        files_location: str = sys.argv[2] if len(sys.argv) > 2 else getcwd()
        materials_location: str = path.join(
            installation_location, "data", "renderer", "materials"
        )
        tonemapping: str = path.join(
            materials_location, "RTXPostFX.Tonemapping.material.bin"
        )
        rtxstub: str = path.join(materials_location, "RTXStub.material.bin")
        new_tone_mapping: str = path.join(
            files_location, "RTXPostFX.Tonemapping.material.bin"
        )
        new_stub: str = path.join(files_location, "RTXStub.material.bin")
        installation_method(
            new_stub, new_tone_mapping, rtxstub, tonemapping, materials_location
        )
        check_for_minecraft(installation_location)
    else:
        # Re-run the program with admin rights
        adminify = run_as_admin()
        if adminify:
            # Code ran successfully with admin rights
            pass
        else:
            # User denied UAC prompt
            pass
        sys.exit()
