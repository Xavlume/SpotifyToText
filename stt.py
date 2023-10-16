import pymem
import requests
import html
import configparser
from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardText, CloseClipboard

config = configparser.ConfigParser()
config.read('config.ini')

saveToLog = config.getboolean("Config", "saveToLog")
saveToClipboard = config.getboolean("Config", "saveToClipboard")

prefix, linker, suffix =  config["Text"]["prefix"], config["Text"]["linker"], config["Text"]["suffix"]

def getTitleAndArtistFromHtml(html: str):
    title = ""
    artist = ""
    html = html.split("</title>")[0]
    html = html.split("<title>")[1] 
    title, artist = html.split("song and lyrics")
    title = title[:-3]
    artist = artist[4:]
    artist = artist.replace(" | Spotify", "")
    
    return (title, artist)

#chrome_elf.dll+14FA3E string
pm = pymem.Pymem('Spotify.exe', exact_match=True)
client = pymem.process.module_from_name(pm.process_handle, "chrome_elf.dll").lpBaseOfDll
headers = {'Accept-Encoding': 'identity'}

def getStuffs():
    songthing = pm.read_string(client + 0x14FA3E)
    link = "https://open.spotify.com/track/" + songthing
    r = requests.get(link, headers=headers)
    content = r.content[:1000]
    content = str(content.decode('utf-8')) 
    content = html.unescape(content)
    # content = content.replace("&#x27;", "'")
    # content = content.replace("&quot;", "\"")

    title, artist = getTitleAndArtistFromHtml(content)

    return title, artist

def textToClipboard(text: str):
    OpenClipboard()
    EmptyClipboard()
    SetClipboardText(text)
    CloseClipboard()

import PySimpleGUI as sg

sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [
            [sg.Text('Spotify To Text')],

            [sg.Text('')],

            [sg.Text('Prefix: ', size=(15, 1)), sg.InputText(prefix, key='prefix',size=(20, 1))],
            [sg.Text('Linker: ', size=(15, 1)), sg.InputText(linker, key='linker',size=(20, 1))],
            [sg.Text('Suffix: ', size=(15, 1)), sg.InputText(suffix, key='suffix',size=(20, 1))],

            [sg.Checkbox("Save Output To Log File",default=saveToLog, key="saveToLog"), sg.Checkbox("Save Output To Clipboard",default=saveToClipboard, key="saveToClipboard")],

            [sg.Text('')],

            [sg.Button("Get Text"), sg.Button("Save to Config")],

            [sg.Text('')],

            [sg.Text('Output: ', key="output")]
            ]

window = sg.Window('Spotify To Text', layout, finalize=True)

while True:
    event, values = window.read(timeout=20)
    if event == sg.WIN_CLOSED:
        break
    
    if event == "__TIMEOUT__":
        continue

    if event != "Get Text" and event != "Save to Config":
        continue

    try:
        saveToLog = window["saveToLog"].Get()
        saveToClipboard = window["saveToClipboard"].Get()

        prefix, linker, suffix = values['prefix'], values['linker'], values['suffix']


        if event == "Save to Config":
            if sg.popup_yes_no('Do you really want to save to config?') == 'Yes':
                config["Config"]["saveToLog"] = str(saveToLog)
                config["Config"]["saveToClipboard"] = str(saveToClipboard)
                config["Text"]["prefix"], config["Text"]["linker"], config["Text"]["suffix"] = prefix, linker, suffix

                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

            continue

        title, artist = getStuffs()
        
        text = prefix + " " + title + " "  + linker + " "  + artist + suffix

        text = str(text)

        window["output"].update("Output: " + text)

        if saveToLog:
            with open("log.txt", 'a', encoding="utf-8") as f:
                f.write(text + "\n")

        if saveToClipboard:
            textToClipboard(text)
    except Exception as error:
        sg.popup_error(str(error))


window.close()