# import pyaudio
# print("✅ PyAudio is working correctly!")

# import speech_recognition as sr

# print("Available microphones:")
# for i, mic in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"{i}: {mic}")


import speech_recognition as sr

def listen_and_convert():
    recognizer = sr.Recognizer()

    # check microphones
    mics = sr.Microphone.list_microphone_names()
    if not mics:
        print("❌ No microphone detected. Please check your input settings.")
        return
    print(f"🎤 Using microphone: {mics[0]}")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎙 Speak now...")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("🔄 Converting speech to text...")
            text = recognizer.recognize_google(audio)
            print("✅ You said:", text)

        except sr.WaitTimeoutError:
            print("⌛ Listening timed out. No speech detected.")
        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
        except sr.RequestError as e:
            print(f"⚠ API Error: {e}")

listen_and_convert()
