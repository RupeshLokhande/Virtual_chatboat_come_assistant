# Not added ChatGPT
from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser

app = Flask(__name__)

# RASA

def speak(text):
    print(text)
    tts = gTTS(text=text, lang='en')
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_file = f'static/audio/output_{timestamp}.mp3'
    audio_file = output_file
    tts.save(audio_file)

    return audio_file

def wishme():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
         return "Good morning rupesh!, I am Lily. Please tell me how may I help you"
    elif 12 <= hour < 16:
        return "Good Afternoon rupesh!, I am Lily. Please tell me how may I help you"
    elif 16 <= hour < 20:
        return "Good evening rupesh!, I am Lily. Please tell me how may I help you" 
    else:
        return "Good night rupesh!, I am Lily. Please tell me how may I help you"
    

def sendEmail(to, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('rpesh889676@gmail.com', "sowrujkdvlozwzvi")
    email_message = f"Subject: {subject}\n\n{content}"
    server.sendmail("rpesh889676@gmail.com", to, email_message)
    server.close()

@app.route('/')
def index():
    message = wishme()
    audio_file = speak(message)
    return render_template('first.html', audio_file=audio_file,message=message, text=True)


@app.route('/process', methods=['POST'])
def process():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5)

    try:
        text = r.recognize_google(audio)
        query = text.lower()
        if "wikipedia" in query:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            audio_file = speak("According to Wikipedia" + results)
            return render_template('first.html', audio_file=audio_file,text=True)
        
        elif "youtube" in query:
            bannedWord = ['open', 'on', 'youtube']
            url = ' '.join(i for i in query.split() if i not in bannedWord)
            youtubeURL = 'https://www.youtube.com/results?search_query=' + url.lower().replace(" ", "")
            audio_file = speak(f'Opening {url} on Youtube')
            webbrowser.open(youtubeURL)
            return render_template('first.html', audio_file=audio_file,text=True)
        
        elif "google" in query:
            bannedWord = ['open', 'on', 'google']
            url = ' '.join(i for i in query.split() if i not in bannedWord)
            audio_file = speak(f'Opening {url} on Google')
            webbrowser.open(url)
            return render_template('first.html', audio_file=audio_file,text=True)

        elif "open stackoverflow" in query:
            audio_file = speak("Opening stackoverflow")
            webbrowser.open("https://stackoverflow.com")
            return render_template('first.html', audio_file=audio_file,text=True)

        elif "open telegram" in query:
            audio_file = speak("Opening telegram")
            webbrowser.open("https://telegram.org")
            return render_template('first.html', audio_file=audio_file,text=True)

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            audio_file = speak(f"Sir, the time is {strTime}")
            return render_template('first.html', audio_file=audio_file,text=True)

    except Exception as e: 
         audio_file = speak("Sorry, I couldn't understand.")
         return render_template('first.html', audio_file=audio_file,text=True)
    
    audio_file = speak("Sorry, I couldn't understand.")
    return render_template('first.html', audio_file=audio_file,text=True)


@app.route('/play')
def play():
    audio_file = request.args.get('file')
    if audio_file:
        return send_file(audio_file, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True)
