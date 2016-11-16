import time
import calendar

try:
    from weather import WeatherClass
except ImportError:
    from fake_weather import WeatherClass

try:
    #python3
    import tkinter as tk
except ImportError:
    #python2
    import Tkinter as tk

#constants get ALL_CAPS names and go at the top of the file
LABEL_FONT = ('Courier', 20, 'bold')

WIDGET_DEFAULTS = {
    'background': 'black',
    'fg': 'white',
    'borderwidth': 0,
    'highlightthickness': 0}

class Label(tk.Label):
    '''Define a custom Label (different from tk.Label) with the default
    properties applied in a way that can be overridden'''
    def __init__(self, master, **kwargs):
        defaults = WIDGET_DEFAULTS.copy()
        defaults.update(kwargs)
        tk.Label.__init__(self, master, **defaults)

class Calendar(tk.Text):
    def __init__(self, master):
        tk.Text.__init__(self, master, width=40, **WIDGET_DEFAULTS)
        self.update_cal()

    def update_cal(self):
        time1 = time.localtime(time.time())
        cal_text = calendar.month(time1.tm_year, time1.tm_mon)
        self.insert(tk.INSERT, cal_text)
        #perhaps add code to calculate how many milliseconds till the end of the month


class LiveTime(Label):
    def __init__(self, master):
        Label.__init__(self, master)
        self.update_time()

    def update_time(self):
        self.config(text = time.asctime())
        #calculate how many milliseconds are left in this second
        wait_for = int((1 - time.time()%1) * 1000) or 1000
        #wait that long and then run this method again.
        self.after(wait_for, self.update_time)


class WeatherWidgets(tk.Frame):
    '''Draw weather results'''
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.weatherClassObject = WeatherClass()#Create object of our WeatherClass()

        self.textWidget = Label(self)
        self.textWidget.config(font=LABEL_FONT)
        self.textWidget.config(height=3, width=16)
        self.textWidget.pack(anchor=tk.CENTER, side='left', fill=tk.BOTH, expand=True)

        self.imageWidget = Label(self)
        self.imageWidget.pack()

        self.update_weather()

    def update_weather(self):
        self.weatherClassObject.update()

        #Get description of weather/ temperature
        weatherInfo = str(self.weatherClassObject.currentWeather)
        weatherInfo += '\n'
        weatherInfo += str(self.weatherClassObject.currentTemperature + 'F')
        self.textWidget.config(text = weatherInfo) #update text

        # It's not strictly needed to make this an instance variable (starts with 'self.')
        # but due to an ancient bug in Tkinter you have to keep a reference somewhere, so
        # it's tradition to make the image an instance variable.
        self.weatherImage = self.weatherClassObject.weatherImage
        self.imageWidget.config(image=self.weatherImage) #update image

        print('Updating..')#Testing
        self.after(5000, self.update_weather) #Updates every x milliseconds


class PinkFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg='pink')

        text = Label(self, text="Top Left")
        text.pack()


class YellowFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg='yellow')

        # here we use tkinters version of Label, so we don't get the background
        text = tk.Label(self, text='Bottom Left')
        text.pack()


class TopRow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg='black')

        pink = PinkFrame(self)
        pink.pack(side='left', fill=tk.BOTH, expand=True)

        cal = Calendar(self)
        cal.pack(side='left')

        time = LiveTime(self)
        time.pack(side='left', anchor='n')


class BottomRow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        yellow = YellowFrame(self)
        yellow.pack(side='left', fill=tk.BOTH, expand=True)

        weather = WeatherWidgets(self)
        weather.pack()


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        top_row = TopRow(self)
        top_row.pack(fill=tk.X, expand=True)

        bottom_row = BottomRow(self)
        bottom_row.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Smart Mirror')
    app = Application(root) # change this to any subframe to test that subframe only
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


