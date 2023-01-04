import speech_recognition as sr
import pyaudio
import requests
import os
import openai
from gtts import gTTS

# The endpoint for the ChatGPT3 API is constant
api_endpoint = "https://api.openai.com/v1/chat"

# My OpenAI API Key
openai.api_key = os.environ["API_KEY"]

recognizer = sr.Recognizer()
microphone = sr.Microphone()

while True:
	with microphone as source:
		audio = recognizer.listen(source)
		try:
			transcription = recognizer.recognize_google(audio)
			print(f"Input text: {transcription}")
			
			# Send the transcribed text to the ChatGPT3 API
			
			response = openai.Completion.create(
			engine="text-davinci-003",
			prompt=transcription,
			temperature=0.9,
			max_tokens=512,
			top_p=1,
			presence_penalty=0.6
			)

			# Get the response text from the ChatGPT3 API
			response_text = response.choices[0].text

			# Print the response from the ChatGPT3 API
			print(f"Response text: {response_text}")

			# Generate an audio file from the response text
			tts = gTTS(response_text)

			# Build the file path for the audio file
			file_path = os.path.join(os.path.abspath(os.pardir), 'sound_files', 'response.mp3')

			# Save the audio file to a file called 'response.mp3'
			tts.save(file_path)

			# Play the audio using the system's default media player
			os.system(f'mpg123 {file_path}')
			
		except sr.UnknownValueError:
			print("Unable to transcribe audio")
		break

# Can run in terminal with following command to suppress errors:
# python jarvis.py 2>/dev/null
