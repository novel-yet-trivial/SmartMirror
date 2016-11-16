
'''for testing only'''


try:
    #python3
    from tkinter import PhotoImage
except ImportError:
    #python2
    from Tkinter import PhotoImage

class WeatherClass:
    def __init__(self):
        self.currentTemperature = "78"
        self.todaysForecast = "99"
        self.currentWeather = "cloudy"
        self.weatherImage = PhotoImage(file="ClearSkyDay.png")

    def update(self):
        pass
