import pyttsx3
engine = pyttsx3.init()


engine.setProperty('rate', 150) 

# voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice.id)
#    engine.setProperty('voice', voice.id)
#    engine.say("I will speak this text")

engine.setProperty('voice', 'english_north')
engine.say("Hi, I'm Jarvis")
engine.runAndWait()