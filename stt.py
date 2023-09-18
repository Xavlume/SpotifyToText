import PySimpleGUI as sg

from PIL import ImageGrab
from pytesseract import pytesseract
from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, CloseClipboard
from pyautogui import position
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

coords = config["Coordinates"]
x1, y1, x2, y2, x3, y3, x4, y4 =  int(coords['x1']), int(coords['y1']), int(coords['x2']), int(coords['y2']), int(coords['x3']), int(coords['y3']), int(coords['x4']),int(coords['y4'])

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = config["Path"]["tesseract"]
pytesseract.tesseract_cmd = path_to_tesseract

debug = config.getboolean("Other", "debug")
saveToLog = config.getboolean("Other", "saveToLog")
saveToClipboard = config.getboolean("Other", "saveToClipboard")

prefix, linker, suffix =  config["Text"]["prefix"], config["Text"]["linker"], config["Text"]["suffix"]

def validValues(xyValues: list[int]) -> bool:
    if xyValues[0] >= xyValues[2] or xyValues[1] >= xyValues[3]:
        sg.popup_error("Invalid Title Coordinates")
        return False
    if xyValues[4] >= xyValues[6] or xyValues[5] >= xyValues[7]:
        sg.popup_error("Invalid Artist Coordinates")
        return False
    
    return True

def getText(firstBox, secondBox, prefix: str = "", linker = " - ", suffix: str = "", debug: bool = False) -> str:

    img = ImageGrab.grab(all_screens=True)
    img1 = img.crop(firstBox)
    img2 = img.crop(secondBox)

    if debug:
        img1.save("title.png")
        img2.save("artist.png")
    # Providing the tesseract executable
    # location to pytesseract library

    
    title = pytesseract.image_to_string(img1)
    artist = pytesseract.image_to_string(img2)

    title = title.replace("\n", "")
    title = title.replace("  ", "")

    artist = artist.replace("\n", "")
    artist = artist.replace("  ", "")

    text = prefix + " " + title + " "  + linker + " "  + artist + suffix

    return text
    # Displaying the extracted text

def textToClipboard(text: str):
    OpenClipboard()
    EmptyClipboard()
    SetClipboardText(text)
    CloseClipboard()

sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [
            [sg.Text('Current Mouse Position: (  ,  )', key="mouseLabel")],

            [sg.Text('')],

            [sg.Text('Title Coordinates: ')],
            [sg.Text('Top Left x and y: ALT-F5', size=(25, 1)), sg.InputText(x1, key='x1',size=(10, 1)), sg.InputText(y1, key='y1', size=(10, 1))],
            [sg.Text('Bottom right x and y: ALT-F6', size=(25, 1)), sg.InputText(x2, key='x2',size=(10, 1)), sg.InputText(y2, key='y2', size=(10, 1))],

            [sg.Text('Artist Coordinates: ')],
            [sg.Text('Top Left x and y: ALT-F7', size=(25, 1)), sg.InputText(x3, key='x3',size=(10, 1)), sg.InputText(y3, key='y3', size=(10, 1))],
            [sg.Text('Bottom right x and y: ALT-F8', size=(25, 1)), sg.InputText(x4, key='x4',size=(10, 1)), sg.InputText(y4, key='y4', size=(10, 1))],

            [sg.Text('')],

            [sg.Text('Prefix: ', size=(15, 1)), sg.InputText(prefix, key='prefix',size=(20, 1))],
            [sg.Text('Linker: ', size=(15, 1)), sg.InputText(linker, key='linker',size=(20, 1))],
            [sg.Text('Suffix: ', size=(15, 1)), sg.InputText(suffix, key='suffix',size=(20, 1))],

            [sg.Checkbox("Debug", default=debug, key="debug"), sg.Checkbox("Save Output To Log File",default=saveToLog, key="saveToLog"), sg.Checkbox("Save Output To Clipboard",default=saveToClipboard, key="saveToClipboard")],

            [sg.Text('')],

            [sg.Button("Apply"), sg.Button("Save to Config")],

            [sg.Text('')],

            [sg.Text('Output: ', key="output")]
            ]

window = sg.Window('Spotify To Text', layout, finalize=True)

window.bind("<Alt_L><F5>", "ALT-f5")
window.bind("<Alt_L><F6>", "ALT-f6")
window.bind("<Alt_L><F7>", "ALT-f7")
window.bind("<Alt_L><F8>", "ALT-f8")

while True:
    event, values = window.read(timeout=20)

    mousePosition = position()
    mousePositionText = f"( {mousePosition[0]} , {mousePosition[1]} )"
    mousePositionText = "Current Mouse Position: " + mousePositionText
    window["mouseLabel"].update(mousePositionText)

    if event == sg.WIN_CLOSED:
        break
    
    if event == "__TIMEOUT__":
        continue

    if event != "Apply" and event != "Save to Config" and "ALT" not in event:
        continue

    try:
        debug = window["debug"].Get()
        saveToLog = window["saveToLog"].Get()
        saveToClipboard = window["saveToClipboard"].Get()

        prefix, linker, suffix = values['prefix'], values['linker'], values['suffix']

        xyValues =  [values['x1'], values['y1'], values['x2'], values['y2'], values['x3'], values['y3'], values['x4'], values['y4']]

        invalid = False
        for coord in xyValues:
            if not coord.isdigit():
                sg.popup_error(f"invalid coord: {coord}")
                invalid = True
                
        if invalid:
            continue

        xyValues = [int(value) for value in xyValues]

        if "ALT" in event:
            if "f5" in event:
                window["x1"].update(mousePosition[0])
                window["y1"].update(mousePosition[1])
            if "f6" in event:
                window["x2"].update(mousePosition[0])
                window["y2"].update(mousePosition[1])
            if "f7" in event:
                window["x3"].update(mousePosition[0])
                window["y3"].update(mousePosition[1])
            if "f8" in event:
                window["x4"].update(mousePosition[0])
                window["y4"].update(mousePosition[1])
            continue

        if not validValues(xyValues):
            continue

        if event == "Save to Config":
            if sg.popup_yes_no('Do you really want to save to config?') == 'Yes':
                config["Path"]["tesseract"] = path_to_tesseract
                config["Other"]["debug"] = str(debug)
                config["Other"]["saveToLog"] = str(saveToLog)
                config["Other"]["saveToClipboard"] = str(saveToClipboard)
                config["Text"]["prefix"], config["Text"]["linker"], config["Text"]["suffix"] = prefix, linker, suffix

                xyStringValues = [str(value) for value in xyValues]

                for index, key in enumerate(config["Coordinates"].keys()):
                    config["Coordinates"][key] = xyStringValues[index]

                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

            continue


        titleBbox = (xyValues[0], xyValues[1], xyValues[2], xyValues[3])
        artistBbox = (xyValues[4], xyValues[5], xyValues[6], xyValues[7])
        
        text = getText(titleBbox, artistBbox, prefix, linker, suffix, debug)

        window["output"].update("Output: " + text)

        if saveToLog:
            with open("log.txt", 'a') as f:
                f.write(text + "\n")

        if saveToClipboard:
            textToClipboard(text)
    except Exception as error:
        sg.popup_error(str(error))


window.close()