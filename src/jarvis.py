import time
import speech_recognition as sr
import os
import openai
import pyttsx3

# Function to transcribe audio, send to ChatGPT, and read aloud
def listen_and_respond(after_prompt=True):
	"""
	Transcribes audio, sends to ChatGPT, and responds in speech
	
	Args:
	after_prompt: bool, whether the response comes directly
	after the user says "Hey, Jarvis!" or not
	
	"""
	# Default is don't start listening, until I tell you to
	start_listening = False

	with microphone as source:

		if after_prompt:
			recognizer.adjust_for_ambient_noise(source)
			print("Say 'Hey, Jarvis!' to start")
			audio = recognizer.listen(source, phrase_time_limit=5)
			try:
				transcription = recognizer.recognize_google(audio)
				if transcription.lower() == "hey jarvis":
					start_listening = True
				else:
					start_listening = False
			except sr.UnknownValueError:
				start_listening = False
		else:
			start_listening = True
		
		if start_listening:
			try:
				print("Listening for question...")
				audio = recognizer.record(source, duration=5)
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

				#  Say the response
				engine.say(response_text)
				engine.runAndWait()
	
			except sr.UnknownValueError:
				print("Unable to transcribe audio")


# pyttsx3 engine paramaters
engine = pyttsx3.init()
engine.setProperty('rate', 150) 
engine.setProperty('voice', 'english_north')

# My OpenAI API Key
openai.api_key = os.environ["API_KEY"]

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# First question
first_question = True

# Initialize last_question_time to current time
last_question_time = time.time()

# Set threshold for time elapsed before requiring "Hey, Jarvis!" again
threshold = 60 # 1 minute

while True:
	if (first_question == True) | (time.time() - last_question_time > threshold):
		listen_and_respond(after_prompt=True)
		first_question = False
	else:
		listen_and_respond(after_prompt=False)