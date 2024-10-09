# c:/Users/Peter/Documents/Care-Home-4/app/SpeechRecog/voice_to_text.py

def transcribe_audio(audio_file):
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"