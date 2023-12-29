config: dict[str, str] = {
    "dev": "False",
    "url": "https://betterrtx.vercel.app/",
    "uninstall-rtxstub-endpoint": "https://betterrtx.vercel.app/uninstall/rtxstub",
    "uninstall-rtxpostfx-endpoint": "https://betterrtx.vercel.app/uninstall/rtxpostfx",
    "iobit-unlocker-location": "C:/Program Files (x86)/IObit/IObit Unlocker/IObitUnlocker.exe",
    "dlssURL": "https://betterrtx.vercel.app/dlss",
}

lang: dict[str, str] = {
    "installerLocationChoice": "Choose installation location:",
    "installerLocationChoice1": "1): Minecraft Bedrock Edition (Default)",
    "installerLocationChoice2": "2): Minecraft Preview Edition (Advanced) (Not Recommended as features can change before we can update BetterRTX for it)",
    "installerLocationInvalid": "Invalid Selection",
    "installerLocationPrompt": "Selection",
    "checkingForIOBitUnlocker": "Checking for IOBit Unlocker...",
    "IOBitUnlockerCheckPass": "IObit Unlocker is installed, Continuing...",
    "IOBitUnlockerCheckFail": "IObit Unlocker is not installed",
    "IOBitUnlockerPleaseInstall": "Please install IObit Unlocker and try again",
    "checkingForMinecraft": "Checking for Minecraft...",
    "MinecraftCheckPass": "Minecraft is installed, Continuing...",
    "MinecraftCheckFail": "Minecraft is not installed",
    "MinecraftPleaseInstall": "Please install Minecraft and try again",
    "installation_method": "Choose installation method:",
    "serverInstall": "1): Install from Server (Recommended)",
    "localInstall": "2): Install from Local Files (Advanced) (Assumes you have the latest files in the same directory as the installer)",
    "uninstall": "3): Uninstall BetterRTX",
    "exit": "4): Exit",
    "installation_methodInvalid": "Invalid Selection",
    "installation_methodPrompt": "Selection",
    "installSelectionKeyword": "Select",
    "downloadingFromServer": "Downloading Latest Version List from server",
    "versionSelect": "Select the Preset to Install!",
    "selectVersionPrompt": "Select Version",
    "downloadingBins": "Downloading Latest RTXStub.material.bin and RTXPostFX.Tonemapping.material.bin from server",
    "doneDownloading": "Done Downloading. Continuing...",
    "uninstalling": "Uninstalling BetterRTX...",
    "downloadingVanilla": "Downloading Latest Vanilla RTXStub.material.bin and RTXPostFX.Tonemapping.material.bin",
    "removingStub": "Removing Old RTXStub.material.bin",
    "removingTonemapping": "Removing Old RTXPostFX.Tonemapping.material.bin",
    "insertingVanillaStub": "Inserting Vanilla RTXStub.material.bin",
    "insertingVanillaTonemapping": "Inserting Vanilla RTXPostFX.Tonemapping.material.bin",
    "doneSadFace": "Done :(",
    "sorryToSeeYouGo": "We're Sorry to See You Go. If you have any suggestions or issues, create a message in the #betterrtx-help forum channel in the Minecraft RTX Server.",
    "installerOptionNotFound": "Option Not Found. Restart the Program and try again. Exiting...",
    "inviteLink": "Invite Link: https://discord.gg/minecraft-rtx-691547840463241267",
    "helpChannelLink": "Help Channel Link: https://discord.com/channels/691547840463241267/1101280299427561523",
    "stubFound": "RTXStub.material.bin is present, Continuing...",
    "stubNotFound": "RTXStub.material.bin is not present",
    "tonemappingFound": "RTXPostFX.Tonemapping.material.bin is present, Continuing...",
    "tonemappingNotFound": "RTXPostFX.Tonemapping.material.bin is not present, Exiting...",
    "insertingTonemapping": "Inserting BetterRTX RTXPostFX.Tonemapping.material.bin",
    "insertingStub": "Inserting BetterRTX RTXStub.material.bin",
    "doneHappyFace": "Done :)",
    "thanks": "Thanks For Installing BetterRTX! If you have any issues, use the #betterrtx-help forum channel in the Minecraft RTX Server!",
    "resourcePackNotice": "YOU STILL NEED AN RTX RESOURCE PACK FOR THIS TO WORK!",
}

VERSION: str = "1.2.1"
PRERELEASE = True
IOBU: str = "C:\\Program Files (x86)\\IObit\\IObit Unlocker\\IObitUnlocker.exe"

URL: str = config["url"]
UNINSTALL_STUB: str = config["uninstall-rtxstub-endpoint"]
UNINSTALL_TONEMAPPING: str = config["uninstall-rtxpostfx-endpoint"]

releasestr = (
    f"|         This is v{VERSION} of the Quick Installer for Minecraft RTX         |"
)
prereleasestr = (
    f"| This is v{VERSION} (Pre-release) of the Quick Installer for Minecraft RTX   |"
)

LOGO = f"""
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
{prereleasestr if PRERELEASE else releasestr}
|            OFFICIAL BetterRTX INSTALLER | DO NOT DISTRIBUTE             |
|_________________________________________________________________________|



"""
