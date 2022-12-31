# Can't get this to work - going to build on my own

# Import pyaudio module
import pyaudio

# First, we will listen
# We need to set some parameters
# Buffer chunk size in bytes
CHUNK = 1024 # (Frames per buffer)
# The audio format
FORMAT = pyaudio.paInt16
# The number of channels to record on
CHANNELS = 1
# The sample rate, 44.1kHz
RATE = 44100
# The number of seconds to record for
RECORD_SECS = 5

# Next, create a pyaudio object
p = pyaudio.PyAudio()

# We need a stream to record from
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
				input=True, frames_per_buffer=CHUNK)
				
# We can now record into a temporary buffer
frames = []
for i in range(0, int(RATE / CHUNK + RECORD_SECS)):
	data = stream.read(CHUNK)
	frames.append(data)
	
# We can now shut everything down
stream.stop_stream()
stream.close()
p.terminate()


# If we want to play a .wav file, we will need the wave module

import wave

# We can open it, give it a filename
wf = wave.open("filename.wav", "rb")

# We need a new pyaudio object
p = pyaudio.PyAudio()

# We will open a stream, using the setting from the wav file
stream = p.open(format=p.get_format_from_width(wf.getsamplewidth()),
				channels=wf.getnchannels(), rate=wf.getframerate(),
				output=True)
				
# We can now read from the file and play it out loud
data = wf.readframes(CHUNK)
while data != '':
	stream.write(data)
	data = wf.readframes(CHUNK)
	
# Now, shut everything down again
stream.stop_stream()
stream.close()
p.terminate


