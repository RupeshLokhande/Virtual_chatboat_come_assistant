import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good morning rupesh!")
    elif 12 <= hour < 16:
        speak("Good afternoon rupesh!")
    elif 16 <= hour < 20:
        speak("Good evening rupesh!")
    else:
        speak("Good night rupesh!")
    speak("I am Jarvis. Please tell me how may I help you")



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing..")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Please say that again..")
            return "none"
        return query


def sendEmail(to, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('rpesh889676@gmail.com', "sowrujkdvlozwzvi")
    email_message = f"Subject: {subject}\n\n{content}"
    server.sendmail("rpesh889676@gmail.com", to, email_message)
    server.close()


if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "youtube" in query:
            bannedWord = ['open', 'on', 'youtube']
            url = ' '.join(i for i in query.split() if i not in bannedWord)
            youtubeURL = 'https://www.youtube.com/results?search_query=' + url.lower().replace(" ", "")
            webbrowser.open(youtubeURL)

        elif "open google" in query:
            webbrowser.open("https://google.com")

        elif "open stackoverflow" in query:
            webbrowser.open("https://stackoverflow.com")

        elif "open telegram" in query:
            webbrowser.open("https://telegram.org")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "thank you" in query:
            speak("You're welcome. Goodbye!")
            break

        elif "play music" in query:
            music_dir = 'D://music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "open code" in query:
            code_path = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2022.2.2\\bin\\pycharm64.exe"
            os.startfile(code_path)

        elif "email to omkar" in query:
            try:
                speak("What is the subject of the email?")
                subject = takeCommand()
                speak("What should I say?")
                content = takeCommand()
                to = "onkar_potdar_mech@moderncoe.edu.in"
                sendEmail(to, subject, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

        elif "email to rupesh" in query:
            try:
                speak("What is the subject of the email?")
                subject = takeCommand()
                speak("What should I say?")
                content = takeCommand()
                to = "Rupeshlokhande4954@gmail.com"
                sendEmail(to, subject, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

        elif "i want to send an email" in query:
            try:
                speak("Tell us your email name without @gmail.com?")
                to = takeCommand().lower().replace(" ", "")
                emailTo = to+"@gmail.com"
                speak("What is the subject of the email?")
                subject = takeCommand()
                speak("What should I say?")
                content = takeCommand()
                sendEmail(emailTo, subject, content)
                speak("Email has been sent.")

            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

