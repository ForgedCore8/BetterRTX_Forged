""" BetterRTX installer written in python and betterfied"""
import os
import sys
from os import getcwd, path, remove, system
from subprocess import CalledProcessError, run
from time import sleep

from requests import get

# from constants import (
#     IOBU,
#     PRERELEASE,
#     UNINSTALL_STUB,
#     UNINSTALL_TONEMAPPING,
#     URL,
#     VERSION,
#     lang,
# )

windll = __import__("ctypes").windll if os.name == "nt" else None
# That made the linter angry
# We must appease the gods of python
# They demand a sacrifice

config = {
    "dev": False,
    "url": "https://betterrtx.vercel.app/",
    "uninstall-rtxstub-endpoint":
    "https://betterrtx.vercel.app/uninstall/rtxstub",
    "uninstall-rtxpostfx-endpoint":
    "https://betterrtx.vercel.app/uninstall/rtxpostfx",
    "iobit-unlocker-location":
    "C:/Program Files (x86)/IObit/IObit Unlocker/IObitUnlocker.exe",
    "dlssURL": "https://betterrtx.vercel.app/dlss"
}

lang = {
    "installerLocationChoice": "Choose installation location:",
    "installerLocationChoice1": "1): Minecraft Bedrock Edition (Default)",
    "installerLocationChoice2":
    "2): Minecraft Preview Edition (Advanced) (Not Recommended as features can change before we can update BetterRTX for it)",
    "installerLocationInvalid": "Invalid Selection",
    "installerLocationPrompt": "Selection",
    "checkingForIOBitUnlocker": "Checking for IOBit Unlocker...",
    "IOBitUnlockerCheckPass": "IObit Unlocker is installed, Continuing...",
    "IOBitUnlockerCheckFail": "IObit Unlocker is not installed",
    "IOBitUnlockerPleaseInstall":
    "Please install IObit Unlocker and try again",
    "checkingForMinecraft": "Checking for Minecraft...",
    "MinecraftCheckPass": "Minecraft is installed, Continuing...",
    "MinecraftCheckFail": "Minecraft is not installed",
    "MinecraftPleaseInstall": "Please install Minecraft and try again",
    "installation_method": "Choose installation method:",
    "serverInstall": "1): Install from Server (Recommended)",
    "localInstall":
    "2): Install from Local Files (Advanced) (Assumes you have the latest files in the same directory as the installer)",
    "uninstall": "3): Uninstall BetterRTX",
    "exit": "4): Exit",
    "installation_methodInvalid": "Invalid Selection",
    "installation_methodPrompt": "Selection",
    "installSelectionKeyword": "Select",
    "downloadingFromServer": "Downloading Latest Version List from server",
    "versionSelect": "Select the Preset to Install!",
    "selectVersionPrompt": "Select Version",
    "downloadingBins":
    "Downloading Latest RTXStub.material.bin and RTXPostFX.Tonemapping.material.bin from server",
    "doneDownloading": "Done Downloading. Continuing...",
    "uninstalling": "Uninstalling BetterRTX...",
    "downloadingVanilla":
    "Downloading Latest Vanilla RTXStub.material.bin and RTXPostFX.Tonemapping.material.bin",
    "removingStub": "Removing Old RTXStub.material.bin",
    "removingTonemapping": "Removing Old RTXPostFX.Tonemapping.material.bin",
    "insertingVanillaStub": "Inserting Vanilla RTXStub.material.bin",
    "insertingVanillaTonemapping":
    "Inserting Vanilla RTXPostFX.Tonemapping.material.bin",
    "doneSadFace": "Done :(",
    "sorryToSeeYouGo":
    "We're Sorry to See You Go. If you have any suggestions or issues, create a message in the #betterrtx-help forum channel in the Minecraft RTX Server.",
    "installerOptionNotFound":
    "Option Not Found. Restart the Program and try again. Exiting...",
    "inviteLink":
    "Invite Link: https://discord.gg/minecraft-rtx-691547840463241267",
    "helpChannelLink":
    "Help Channel Link: https://discord.com/channels/691547840463241267/1101280299427561523",
    "stubFound": "RTXStub.material.bin is present, Continuing...",
    "stubNotFound": "RTXStub.material.bin is not present",
    "tonemappingFound":
    "RTXPostFX.Tonemapping.material.bin is present, Continuing...",
    "tonemappingNotFound":
    "RTXPostFX.Tonemapping.material.bin is not present, Exiting...",
    "insertingTonemapping":
    "Inserting BetterRTX RTXPostFX.Tonemapping.material.bin",
    "insertingStub": "Inserting BetterRTX RTXStub.material.bin",
    "doneHappyFace": "Done :)",
    "thanks":
    "Thanks For Installing BetterRTX! If you have any issues, use the #betterrtx-help forum channel in the Minecraft RTX Server!",
    "resourcePackNotice":
    "YOU STILL NEED AN RTX RESOURCE PACK FOR THIS TO WORK!"
}

VERSION = "1.2.1"
PRERELEASE = True
IOBU = "C:\\Program Files (x86)\\IObit\\IObit Unlocker\\IObitUnlocker.exe"

URL = config["url"]
UNINSTALL_STUB = config["uninstall-rtxstub-endpoint"]
UNINSTALL_TONEMAPPING = config["uninstall-rtxpostfx-endpoint"]

def get_appx_package(name_pattern):
    """Gets APPX package location using powershell"""
    result = run(
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
    system("cls")
    releasestr = f"|         This is v{VERSION} of the Quick Installer for Minecraft RTX         |"
    prereleasestr = f"| This is v{VERSION} (Pre-release) of the Quick Installer for Minecraft RTX   |"
    versionstr = prereleasestr if PRERELEASE is True else releasestr
    logo = f"""
 _________________________________________________________________________
|    ____           _     _                   _____    _______  __   __   |
|   |  _ \\         | |   | |                 |  __ \\  |__   __| \\ \\ / /   |
|   | |_) |   ___  | |_  | |_    ___   _ __  | |__) |    | |     \\ V /    |
|   |  _ <   / _ \\ | __| | __|  / _ \\ | '__| |  _  /     | |      > <     |
|   | |_) | |  __/ | |_  | |_  |  __/ | |    | | \\ \\     | |     / . \\    |
|   |____/   \\___|  \\__|  \\__|  \\___| |_|    |_|  \\_\\    |_|    /_/ \\_\\   |
|_____________________________QUICK INSTALLER_____________________________|
 _________________________________________________________________________
|                                                                         |
{versionstr}
|            OFFICIAL BetterRTX INSTALLER | DO NOT DISTRIBUTE             |
|_________________________________________________________________________|



"""
    print(logo)


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
            location = int(
                input(f"{lang['installerLocationPrompt']}: "))  # Select
        else:
            print("Automatic Mode Enabled")
            location = sys.argv[1]

        if location == 1:
            installlocation = get_appx_package("Microsoft.MinecraftUWP*")
        elif location == 2:
            installlocation = get_appx_package(
                "Microsoft.MinecraftWindowsBeta*")
        else:
            print(lang["installerLocationInvalid"])
            sleep(5)
            continue  # Continue the loop to prompt again

        if installlocation is not None:
            return installlocation  # Valid install location found

        # If installlocation is None, print an error message and prompt again
        print(
            "Unable to find a valid installation location. Please try again.")
        sleep(2)

        if auto:
            # In automatic mode, exit if a valid location isn't found
            sys.exit(
                "Exiting: No valid installation location found in automatic mode."
            )


def check_for_iobu():
    """Checks that IO BitUnlocker is installed"""
    print_logo()
    if not path.exists(IOBU):
        print(
            f"{lang['IOBitUnlockerCheckFail']}\n",
            f"{lang['IOBitUnlockerPleaseInstall']}\n",
            "https://www.iobit.com/en/iobit-unlocker.php",
        )
        sleep(10)
        sys.exit()
    print(lang["IOBitUnlockerCheckPass"])
    sleep(2)

def take_ownership(file_path):
    login = os.getlogin()
    run(['takeown', '/f', file_path], check=True)
    run(['icacls', file_path, '/grant', f'{login}:F'], check=True)


def check_for_minecraft(location):
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


def uninstall(stub_new, tone_mapping_new, rtx_stub, tone_mapping, materials):
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
            #    take_ownership(rtx_stub)
            #    os.remove(rtx_stub)
                run([IOBU, "/Delete", f'"{rtx_stub}"'],
                check=True)
            except CalledProcessError:
                print("Failed to remove RTX stub.")

        if path.exists(tone_mapping):
            print(lang["removingTonemapping"])
            try:
            #    take_ownership(tone_mapping)
            #    os.remove(tone_mapping)
                run([IOBU, "/Delete", f'"{tone_mapping}"'],
                check=True)
            except CalledProcessError:
                print("Failed to remove tone mapping.")

            print(lang["insertingStub"])
        try:
            run([IOBU, "/Copy", f'"{stub_new}", "{materials}"'], check=True)
        except CalledProcessError:
            print("Failed to insert new stub.")

        print(lang["insertingTonemapping"])
        try:
            run([IOBU, "/Copy", f'"{tone_mapping_new}", "{materials}"'],
                check=True)
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
        f"{lang['helpChannelLink']}\n",
    )
    sleep(10)
    sys.exit()


def download_from_server(stub_new, tone_mapping_new):
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

def installation_method(stub_new, tone_mapping_new, rtx_stub, tone_mapping,
                        materials):
    """Selects installation method"""
    print_logo()
    print(
        f"{lang['installation_method']}\n",
        f"{lang['serverInstall']}\n",
        f"{lang['localInstall']}\n",
        f"{lang['uninstall']}\n",
        f"{lang['exit']}\n",
    )
    selection = input(f"{lang['installSelectionKeyword']}: ")
    if int(selection) == 1:  # install from server
        print_logo()
        download_from_server(stub_new, tone_mapping_new)
    elif int(selection) == 2:  # install from local files
        pass
    elif int(selection) == 3:  # uninstall
        print_logo()
        uninstall(stub_new, tone_mapping_new, rtx_stub, tone_mapping,
                  materials)
    elif int(selection) == 4:  # exit
        sys.exit()
    else:
        print(lang["installerOptionNotFound"])
        sleep(10)
        sys.exit()

    if path.exists(stub_new):
        print(lang["stubFound"])
    else:
        print(lang["stubNotFound"])
        sleep(10)
        sys.exit()
    if path.exists(tone_mapping_new):
        print(lang["tonemappingFound"])
    else:
        print(lang["tonemappingNotFound"])
        sleep(10)
        sys.exit()
    print("\n\n")
    if path.exists(rtx_stub):
        print(lang["removingStub"])
        try:
        #    take_ownership(rtx_stub)
        #    os.remove(rtx_stub)
            run([IOBU, "/Delete", f'"{rtx_stub}"'],
            check=True)
        except CalledProcessError:
            print("Failed to remove RTX stub.")

    if path.exists(tone_mapping):
        print(lang["removingTonemapping"])
        try:
        #    take_ownership(tone_mapping)
        #    os.remove(tone_mapping)
            run([IOBU, "/Delete", f'"{tone_mapping}"'],
            check=True)
        except CalledProcessError:
            print("Failed to remove tone mapping.")
    print(lang["insertingStub"])
    try:
        run([IOBU, "/Copy", f'"{stub_new}", "{materials}"'], check=True)
    except CalledProcessError:
        print("Failed to insert new stub.")
    print(lang["insertingTonemapping"])
    try:
        run([IOBU, "/Copy", f'"{tone_mapping_new}", "{materials}"'],
            check=True)
    except CalledProcessError:
        print("Failed to insert new tone mapping.")
        if selection != 2:
            remove(tone_mapping_new)
            remove(stub_new)
    sleep(3)
    print_logo()
    print(
        f"\n{lang['doneHappyFace']}\n",
        "_______________________________________________________________________",
        "\n\n",
        f"{lang['thanks']}\n",
        f"{lang['resourcePackNotice']}\n",
        f"{lang['inviteLink']}\n",
        f"{lang['helpChannelLink']}\n",
    )
    sleep(10)
    sys.exit()


def is_admin():
    """detect if app is running as admin"""
    if windll is None:
        return False
    try:
        return windll.shell32.IsUserAnAdmin()
    except OSError as e:
        print(f"Error checking admin status: {e}")
        return False


def run_as_admin(argv=None, debug=False):
    """run app as admin if not already"""
    if windll is None:
        return
    shell32 = windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        # Already an admin
        return True
    if argv is None:
        argv = sys.argv
    if hasattr(sys, "_MEIPASS"):
        # Support pyinstaller wrapped program.
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)
    argument_line = " ".join(arguments)
    executable = str(sys.executable)
    if debug:
        print("Command line: ", executable, argument_line)
    ret = shell32.ShellExecuteW(None, "runas", executable, argument_line, None,
                                1)
    if int(ret) <= 32:
        return False
    return None


if __name__ == "__main__":
    if is_admin():
        installation_location = select_installer_location()
        files_location = sys.argv[2] if len(sys.argv) > 2 else getcwd()
        check_for_iobu()
        materials_location = path.join(installation_location,
                                       "data\\renderer\\materials")
        tonemapping = path.join(materials_location,
                                "RTXPostFX.Tonemapping.material.bin")
        rtxstub = path.join(materials_location, "RTXStub.material.bin")
        new_tone_mapping = path.join(files_location,
                                     "RTXPostFX.Tonemapping.material.bin")
        new_stub = path.join(files_location, "RTXStub.material.bin")
        installation_method(new_stub, new_tone_mapping, rtxstub, tonemapping,
                            materials_location)
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
