from django.shortcuts import render
import json
import urllib.request
import speech_recognition as sr
from .config import OPENWEATHERMAP_API_KEY

# Create your views here.
def get_weather_data(city):
    res = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid='+OPENWEATHERMAP_API_KEY).read()
    json_data = json.loads(res)
    data = {
        "country_code": str(json_data['sys']['country']),
        "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
        "temp": str(json_data['main']['temp']) + 'k',
        "pressure": str(json_data['main']['pressure']),
        "humidity": str(json_data['main']['humidity']),
    }
    return data

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        print(city)
        data = get_weather_data(city)
        context = {'city': city, 'data': data}
    else:
        city = ''
        data = {}
        context = {}
    return render(request, 'index.html', context)

def speechToTextMicrophone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        # listen for 5 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=5)
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("You said: " + r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "Could not request results from Google Speech Recognition service; {0}".format(e)


def voice(request):
    city=speechToTextMicrophone()
    data = get_weather_data(city)
    context = {'city': city, 'data': data}
    return render(request, 'index.html', context)