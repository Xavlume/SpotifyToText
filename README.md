
# Spotify To Text

Captures an image from your desktop and converts it to text. Made using [Pillow](https://python-pillow.org/) to take a screenshot of the dekstop, [Python-tesseract](https://github.com/madmaze/pytesseract) for the image processing into text and [PySimpleGUI](https://www.pysimplegui.org/en/latest/) for the gui.







## Usage

1. Download and install [Tesseract-OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html), for [Windows](https://github.com/UB-Mannheim/tesseract/wiki). Make sure to remember the installation location.
2. Download the latest [release](https://github.com/Xavlume/SpotifyToText/releases) and extract the contents of the zip file.
3. Open the config.ini file and change the installation location for tesseract. Replace single backspaces by doubles. E.G.:
```
tesseract = C:\Program Files\Tesseract-OCR\tesseract.exe
```
to 
```
tesseract = C:\\Program Files\\Tesseract-OCR\\tesseract.exe
```
Save and exit.

4. Run stt.exe.
5. Change the coordinates to match a box around where the title is and where the artists are on spotify.
6. Run.