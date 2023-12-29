""" BetterRTX installer written in python and betterfied"""
import os
import sys
from os import getcwd, path, remove, system
from subprocess import CalledProcessError, run
from time import sleep

from requests import get

from constants import (
    IOBU,
    PRERELEASE,
    UNINSTALL_STUB,
    UNINSTALL_TONEMAPPING,
    URL,
    VERSION,
    lang,
)

windll = __import__("ctypes").windll if os.name == "nt" else None
# That made the linter angry
# We must appease the gods of python
# They demand a sacrifice


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
                run([IOBU, "/Delete", f'"{rtx_stub}"'], check=True)

            except CalledProcessError:
                print("Failed to remove RTX stub.")

        if path.exists(tone_mapping):
            print(lang["removingTonemapping"])
            try:
                run([IOBU, "/Delete", f'"{tone_mapping}"'], check=True)
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
        f"{lang['helpChannellink']}\n",
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
            run([IOBU, "/Delete", f'"{rtx_stub}"'], check=True)
            os.system("taskkill /im IObitUnlocker.exe")
        except CalledProcessError:
            print("Failed to remove RTX stub.")

    if path.exists(tone_mapping):
        print(lang["removingTonemapping"])
        try:
            run([IOBU, "/Delete", f'"{tone_mapping}"'], check=True)
            os.system("taskkill /im IObitUnlocker.exe")
        except CalledProcessError:
            print("Failed to remove tone mapping.")

    print(lang["insertingStub"])
    try:
        run([IOBU, "/Copy", f'"{stub_new}", "{materials}"'], check=True)
        os.system("taskkill /im IObitUnlocker.exe")
    except CalledProcessError:
        print("Failed to insert new stub.")

    print(lang["insertingTonemapping"])
    try:
        run([IOBU, "/Copy", f'"{tone_mapping_new}", "{materials}"'],
            check=True)
        os.system("taskkill /im IObitUnlocker.exe")
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
        f"{lang['helpChannellink']}\n",
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
