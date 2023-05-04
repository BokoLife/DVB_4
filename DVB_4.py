import json, os
import pyttsx3, vosk, pyaudio, requests
tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Microsoft David Desktop - English (UnitedStates)':
        tts.setProperty('voice', voice.id)
model = vosk.Model('vosk-model-small-ru-0.4')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']
def speak(say):
    tts.say(say)
    tts.runAndWait()

print('start')
pwd = ''
for text in listen():
    req = requests.get("https://www.boredapi.com/api/activity")
    data = req.json()
    if text == 'закрыть':
        quit()
    elif text == 'активность':
        pwd = data['activity']
        print(pwd)
    elif text == 'тип':
        pwd = data['type']
        print(pwd)
    elif text == 'количество участников':
        pwd = data['participants']
        print(pwd)
    elif text == 'стоимость':
        pwd = data['price']
        print(pwd)
    elif text == 'сохранить':
        if pwd:
            with open('result.txt', 'a') as f:
                f.write("\n")
                f.write(pwd)
                speak('recorded')
        else:
            speak('nothing to record')
    else:
        print(text)
