import pyaudio
import pocketsphinx
import os

# Set up PocketSphinx
# This is the path to the model folder on the raspberry pi
model_dir = "/usr/share/pocketsphinx/model/en-us"

"""
-hmm specifies the path to the acoustic model to use
An acoustic model is a statistical model of the acoustic characteristics
of sounds of a particular language or dialect, and it is used by
pocketsphinx to recognize speech

lm means language model
A language model is a statistical model of the structure and probability
of a particular language, and is used here to help recognize speech by 
taking into account the context and grammatical structure of the words
being spoken

dict means the pronunciation dictionary
This is a list of words and their corresponding phonetic transcriptions
"""

hmmd = os.path.join(model_dir, 'en-us')
lmd = os.path.join(model_dir, 'en-us.lm.bin')
dictd = os.path.join(model_dir, 'cmudict-en-us.dict')

# Create decoder with these config settings
decoder = pocketsphinx.Decoder(hmm=hmmd, lm=lmd, dict=dictd)

# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(
				format=pyaudio.paInt16,
				channels=1,
				rate=16000,
				input=True,
				frames_per_buffer=1024
				)

stream.start_stream()

"""
Process audio stream

Used to process the audio data from the microphone and feed it to 
PocketSphinx for decoding.

The stream object is an instance of the Stream class from the pyaudio 
module, which represents a streaming audio input or output. The read() 
method is a method of the Stream class that reads audio data from the 
stream. In this case, the read() method is called with a parameter of 
1024, which specifies the number of samples to read from the stream. 
The buf variable is used to store the read data.

The decoder object is an instance of the Decoder class from the 
pocketsphinx module, which represents a PocketSphinx decoder 
configuration. The process_raw() method is a method of the Decoder class 
that processes raw audio data and feeds it to PocketSphinx for decoding. 
In this case, the process_raw() method is called with three parameters:

1. buf: The raw audio data to be processed, which is passed as the buf 
   variable containing the data read from the stream object.
2. False: A boolean flag indicating whether the end of the audio data has 
   been reached. This is set to False because the code is intended to 
   process an ongoing stream of audio data, rather than a fixed audio file.
3. False: A boolean flag indicating whether the audio data is being passed 
   in full-bandwidth (i.e., not downsampled). This is set to False because 
   the code is not downsampling the audio data.
	
The process_raw() method processes the raw audio data and updates the 
internal state of the PocketSphinx decoder. When PocketSphinx detects a 
complete speech utterance, the hyp() method can be called to retrieve the 
decoder's current hypothesis (i.e., the transcribed text of the speech 
utterance).

The hyp() method is a method of the Decoder class that returns the 
current hypothesis (i.e., the transcribed text of the most recently 
detected speech utterance).

The if statement checks whether the hyp() method returns a non-None 
value, which indicates that a complete speech utterance has been detected 
and transcribed by PocketSphinx. If a speech utterance has been detected, 
the print() function is called to print the transcribed text to the console.
The hypstr attribute of the Hypothesis object returned by the hyp() 
method contains the transcribed text as a string.

This code is set up to continuously process audio data from the 
microphone and print the transcribed text of any speech utterances 
detected by PocketSphinx.

Need to have start and stop utterance on either side
"""
decoder.start_utt()
while True:
	buf = stream.read(1024)
	decoder.process_raw(buf, False, False)
	if decoder.hyp() is not None:
		print(decoder.hyp().hypstr)
decoder.end_utt()
		
stream.stop_stream()
stream.close()
p.terminate()



