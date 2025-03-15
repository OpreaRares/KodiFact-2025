import speech_recognition as sr

#testeaza daca exista mic input
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")