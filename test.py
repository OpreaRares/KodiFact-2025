import pyaudio
import speech_recognition as sr
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    print(f"{i}: {dev_info['name']}")
p.terminate()



recognizer = sr.Recognizer()
print(" SpeechRecognition is working!")