import speech_recognition as sr

# create a recognizer object
r = sr.Recognizer()

# define the keyword to listen for
keyword = "hello"

# use the default microphone as the audio source
with sr.Microphone() as source:
    # adjust the energy threshold to ambient noise level
    r.adjust_for_ambient_noise(source)
    print("Listening for keyword...")

    while True:
        # listen for audio and convert it to text
        audio = r.listen(source)
        

        try:
            # recognize speech using Google Speech Recognition
            text = r.recognize_google(audio)
            print(text)
            # check if the keyword is in the recognized text
            if keyword in text.lower():
                print("Message received!")

        except sr.UnknownValueError: 
            # ignore unrecognized speech
            pass
        


# import os
# import sys
# import pocketsphinx as ps
# import pyaudio

# # Set up PocketSphinx recognizer
# config = ps.Decoder.default_config()
# config.set_string('-hmm', os.path.join(ps.Model.dir(), 'en-us'))
# config.set_string('-lm', 'test.lm')
# config.set_string('-dict', os.path.join(ps.Model.dir(), 'cmudict-en-us.dict'))
# decoder = ps.Decoder(config)

# # Set up PyAudio microphone stream
# chunk_size = 1024
# audio_format = pyaudio.paInt16
# sample_rate = 16000
# audio = pyaudio.PyAudio()
# stream = audio.open(format=audio_format, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

# # Listen for keyword
# decoder.start_utt()
# while True:
#     data = stream.read(chunk_size)
#     decoder.process_raw(data, False, False)
#     if decoder.hyp() is not None and decoder.hyp().hypstr == 'hello':
#         print('message received')
#         decoder.end_utt()
#         break

