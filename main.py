# Added ChatGPT

from flask import Flask, render_template, request, send_file
from gtts import gTTS
import openai
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
from api_secret import API_KEY

app = Flask(__name__)

openai.api_key = API_KEY
engine = pyttsx3.init()

r = sr.Recognizer()
mic = sr.Microphone()
print(sr.Microphone.list_microphone_names())

user_name = "Rupesh"


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
    
def openWikipedia(query):
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    return results

def openYoutube(query):
    bannedWord = ['open', 'on', 'youtube']
    url = ' '.join(i for i in query.split() if i not in bannedWord)
    youtubeURL = 'https://www.youtube.com/results?search_query=' + url.lower().replace(" ", "")
    webbrowser.open(youtubeURL)
    return url

def openGoogle(query):
    bannedWord = ['open', 'on', 'google']
    url = ' '.join(i for i in query.split() if i not in bannedWord)
    webbrowser.open(url)  
    return url 


@app.route('/')
def index():
    message = wishme()
    audio_file = speak(message)
    return render_template('first.html', audio_file=audio_file,message=message, text=True)

@app.route('/process', methods=['POST'])
def process():
    conversation = ''
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("No longer listening")

    try:
        user_input = r.recognize_google(audio)
        print("User input: " + user_input)
    
        query = user_input.lower()
        if "wikipedia" in query:
            results = openWikipedia(query)
            audio_file = speak("According to Wikipedia" + results)
            return render_template('first.html', audio_file=audio_file,text=True, response=results)
        
        elif "youtube" in query:
            youtubeUrl = openYoutube(query)
            audio_file = speak(f'Opening {youtubeUrl} on Youtube')
            return render_template('first.html', audio_file=audio_file,)

        
        elif "google" in query:
            searchUrl = openGoogle(query)
            audio_file = speak(f'Opening {searchUrl} on Google')
            return render_template('first.html', audio_file=audio_file)


        elif "thank you" in query:
            audio_file = speak("You're welcome sir, it's been a great time with you")
            return render_template('first.html', audio_file=audio_file)

    
        elif user_input != '' :
            prompt = user_name + ":" + user_input + "\nBot"
            conversation += prompt
            response = openai.Completion.create(engine='text-davinci-001', prompt=conversation, max_tokens=50)
            response_str = response.choices[0].text.replace("\n", "").replace(",", "")
            if user_name + ":" in response_str and "Bot:" in response_str:
                response_str = response_str.split(user_name + ":", 1)[1].split("Bot:", 1)[0]

            conversation += response_str + "\n"
            audio_file = speak(response_str)
            return render_template('first.html', audio_file=audio_file, response=response_str)
    
    except Exception as e:
        print(e)
        audio_file = speak("Sorry, I couldn't understand.")
        return render_template('first.html', audio_file=audio_file)
     
@app.route('/play')
def play():
    audio_file = request.args.get('file')
    if audio_file:
        return send_file(audio_file, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
   