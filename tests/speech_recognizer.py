import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.AudioFile("output.wav") as source:
	audio_data = recognizer.record(source)
	
# Transcribe using Google's Speech-to-Text API
transcription = recognizer.recognize_google(audio_data)

# Transcribe using IBM's Watson Speech-to-Text API
#transcription = recognizer.recognize_watson(audio_data)

# Transcribe using CMU Sphinx
#transcription = recognizer.recognize_sphinx(audio_data)
