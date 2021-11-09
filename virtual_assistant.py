import speech_recognition as sr
import pyttsx3
from datetime import datetime
import requests
import json
import wikipedia
import pyaudio
import os
from googlesearch import search
import subprocess
import webbrowser




# Access weather api
api_key = '517940e716cd982f5f49a780ce60aec4'
lat = '40.66836102311049'
long = '-111.89316523685606'
url = 'https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial' % (
    lat, long, api_key)

# Voice regonition
listener = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)


def start_jarvis():
    engine.say(time_and_weather())
    engine.runAndWait()
    get_command()


def get_command():
    engine.say('what can i help you with today sir.')
    engine.runAndWait()
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis search wikipedia' in command:
                command = command.replace('jarvis search wikipedia for ', '')
                engine.say(wikipedia_command(command))
                engine.runAndWait()
            if 'open' in command:
                command = command.replace('open ','')
                open_application(shortcuts(command))
            if 'search google' in command:
                command = command.replace('search google for ','')
                google_command(command)
    except:
        pass


def open_application(shortcut):
    os.startfile(shortcut)


def wikipedia_command(command):
    search_results = wikipedia.summary(command, sentences = 2)
    return search_results

def google_command(command):
    urls_to_speak = ''
    urls = search(command)
    while len(urls) > 0:

        engine.say(urls[0])
        engine.runAndWait()
        try:
            with sr.Microphone() as source:
                print('yes or no')
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
        except:
            pass
        if command == 'yes':
            webbrowser.open(urls[0],new=1)
            break
        if command == 'no':
            urls.pop(0)

            engine.say('do you want to hear more options')
            engine.runAndWait()
            try:
                with sr.Microphone() as source:
                    print('yes or no')
                    voice = listener.listen(source)
                    command = listener.recognize_google(voice)
            except:
                pass
            if command == 'yes':
                pass
            else:
                break
            


def shortcuts(command):
    if 'battlenet' in command:
        battlenet = 'C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe'
        return battlenet
    elif 'steam' in command:
        steam = "C:\Program Files (x86)\Steam\Steam.exe"
        return steam
    elif 'google' in command:
        google = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        return google
    elif 'slack' in command:
        slack = "C:\Program Files\slack\slack.exe"
        return slack
    elif 'notepad' in command:
        notepad = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\\Notepad"
        return notepad
    elif 'snipping tool' in command:    
        snipping_tool = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\\Snipping Tool"
        return snipping_tool


def get_weather():
    response = requests.get(url)
    data = json.loads(response.text)
    current = round(data['current']['temp'])
    return current


def time_and_weather():
    now = datetime.now()
    current_time = now.strftime('%H%M')
    hours = int(current_time[:2])
    if hours > 13:
        hours -= 12
    minutes = current_time[2:]
    if minutes[0] == '0':
        minutes = 'O' + str(minutes[1])

    if int(current_time) > 1800:
        current_time = current_time - 1200
        return f'Good evening Mr. Stark, it is currently {hours} {minutes} pm, and {get_weather()} degrees outside.'
    elif int(current_time) > 1200:
        return f'Good afternoon Mr. Stark, it is currently {hours} {minutes} pm, and {get_weather()} degrees outside.'
    else:
        return f'Good morning Mr. Stark, it is currently {hours} {minutes} am, and {get_weather()} degrees outside.'


start_jarvis()