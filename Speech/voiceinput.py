import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import threading

class VoiceInput:
    def __init__(self):
        self.porcupine = None
        self.pa = None
        self.audio_stream = None
        self.voice_thread = None

    def initialize_voice(self):
        self.porcupine = pvporcupine.create(
            access_key="K3bYmOitsrCNs5ai3C0qQLkcKhWPaVd59cP5+tkpANbq0NCm1nBc7g==",
            keyword_paths=['Speech/badger.ppn'],
            keywords=['Oi Badger']
        )
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        print("Voice initialized")

    def process_voice_input(self):
        while True:
            pcm = self.audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                print("I heard my name")
                text = self.audio_to_text()
                return(text)

    def audio_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.non_speaking_duration = 0.5
            audio = recognizer.listen(source,timeout=7, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            print("Voice input:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand.")
        except sr.RequestError as e:
            print("There was an error processing the voice input:", str(e))


voiceinput = VoiceInput()