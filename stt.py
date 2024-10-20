from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, CloseClipboard
from win32gui import GetWindowText, EnumWindows
from os import system, path
from configparser import ConfigParser

CONFIG_FILE_NAME = "config.ini"
CONFIG_SECTION_NAME = "SETTINGS"
DEFAULT_CONFIG_SETTINGS = {'title_first': "'True'",
                            'text_before': "''",
                            'seperator': "' by '",
                            'text_after': "''",
                          }

def configIsValid():
    config = ConfigParser()
    try:
        config.read(CONFIG_FILE_NAME)
    except:
        return False
    if CONFIG_SECTION_NAME not in config.keys():
        return False
    for field in DEFAULT_CONFIG_SETTINGS.keys():
        if field not in config[CONFIG_SECTION_NAME]:
            return False
    return True


def setupDefaultConfig():
    config = ConfigParser()
    config[CONFIG_SECTION_NAME] = DEFAULT_CONFIG_SETTINGS
    with open(CONFIG_FILE_NAME, 'w') as configfile:
        config.write(configfile)

def setConfigValue(config: ConfigParser, key: str, value):
    config[CONFIG_SECTION_NAME][key] = f"'{value}'"
    with open(CONFIG_FILE_NAME, 'w') as configfile:
        config.write(configfile)

def getConfigValue(config: ConfigParser, key: str):
    if key == "title_first":
        return config[CONFIG_SECTION_NAME][key] == "'True'"
    else:
        return config[CONFIG_SECTION_NAME][key].strip("'")

clearScreen = lambda : system('cls')

def quitProgram():
    print()
    print("quitting...")
    quit()

def textToClipboard(text: str):
    OpenClipboard()
    EmptyClipboard()
    SetClipboardText(text)
    CloseClipboard()

def getSongText(songTitle, songArtist, config):
    if getConfigValue(config, "title_first"):
        return "".join([getConfigValue(config, "text_before"), songTitle, getConfigValue(config, "seperator"), songArtist, getConfigValue(config, "text_after")])
    else:
        return "".join([getConfigValue(config, "text_before"), songArtist, getConfigValue(config, "seperator"), songTitle, getConfigValue(config, "text_after")])

def changeDisplaySettings(config):
    while True:
        print("Select what you want to change:")

        print(f"Current display settings: {getSongText("'example song title'", "'example song artist'", config)}")
        
        print(f"t : Does the title display first = {getConfigValue(config, "title_first")}")
        print(f"b : Text before the song = '{getConfigValue(config, "text_before")}'")
        print(f"s : Text seperating the title and artists= '{getConfigValue(config, "seperator")}'")
        print(f"a : Text after the song = '{getConfigValue(config, "text_after")}'")
        print(f"q : return to display menu")
        userInputSettings = input("Selection: ")
        clearScreen()

        match userInputSettings:
            case "q":
                break

            case "t":
                while True:
                    print("Type 't' if you want the title first, or 'a' for the artist first")
                    userInputTitleSettings = input("Selection: ")
                    clearScreen()
                    match userInputTitleSettings:
                        case "t":
                            setConfigValue(config, "title_first", "True")
                            break

                        case "a":
                            setConfigValue(config, "title_first", "False")
                            break

                        case _:
                            print("Incorrect Selection. Please try again")
            case "b":
                setConfigValue(config, "text_before", input("What text do you want before the song:"))

            case "s":
                setConfigValue(config, "seperator", input("What text do you want seperating the song title and artist:"))

            case "a":
                setConfigValue(config, "text_after", input("What text do you want after the song:"))

            case _:
                print("Incorrect Selection. Please try again")


if not path.isfile("config.ini"):
    print("Config file not found. Creating it.")
    setupDefaultConfig()

if not configIsValid():
    print("Config file corrupted. Creating a new one.")
    setupDefaultConfig()

config = ConfigParser()
config.read(CONFIG_FILE_NAME)

print("What is the correct window: ")

windows = []
count = 0
def enumHandler(hwnd, lParam):
    global count, windows
    if " - " in GetWindowText(hwnd) or "spotify" in GetWindowText(hwnd).lower():
        count += 1
        windows.append(hwnd)
        print(f"({count}) : {GetWindowText(hwnd)}")
EnumWindows(enumHandler, None)

hwnd = -1
while hwnd < 0:
    try:
        selection = int(input("Selection: "))
        hwnd = windows[selection - 1]
    except KeyboardInterrupt:
        quitProgram()
    except:
        print("Incorrect selection. Please try again")
        print()

clearScreen()

while True:
    try:
        print("Press enter to display title, c to display and copy to the clipboard and s to change display settings")
        userInput = input("Selection: ")
        clearScreen()
        windowText = GetWindowText(hwnd)

        if " - " not in windowText:
            print("Song could not be found")
            continue

        songArtist, songTitle = windowText.split(" - ", 1)
        songText = getSongText(songTitle, songArtist, config)
        match userInput:
            case "":
                print(songText)

            case "c":
                print(songText)
                textToClipboard(songText)

            case "s":
                changeDisplaySettings(config)

            case _:
                print("Incorrect Selection. Please try again")
        print()

    except KeyboardInterrupt:
        quitProgram()
        