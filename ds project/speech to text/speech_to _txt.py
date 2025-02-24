import speech_recognition as sr
# import pyttsx3
# import pyaudio
# initialization of recognizer
reco = sr.Recognizer()
def record_text():
    while(1):
        try:
            # Use the micro phonefor input
            with sr.Microphone() as source2:
                # prepare recognizer to resive input
                reco.adjust_for_ambient_noise(source2, duration= 0.2 )

                # Listion's for the user's input
                audio2 = reco.listen(source2)

                # Using Google to recognize audio
                my_text = reco.recognize_google(audio2)

                return my_text
        except sr.RequestError as e :
            print( "Could nod request resuelt; {0}" . format(e))
        except sr.UnknownValueError:
            print("Unknown Error Occurred")
    return
def outpt_text(text):
    file = open("output.txt", "a")
    file.write(text)
    file.write("\n")
    file.close()
    return
while(1):
    text = record_text()
    outpt_text(text)
    print("wrote text  ")