import time
import calendar
import threading
from weather import Test as WeatherClass

try:
    #python3
    import tkinter as tk
except:
    #python2
    import Tkinter as tk

time1 = time.localtime(time.time())

class LiveTime:
    pass

class Application(tk.Frame):

    def createTime(self):
        self.Time = tk.Label(self.top_right, text=time.asctime(self.localtime), background='black', fg = 'white')
        self.Time.pack(side='right')

    def createCal(self):
        self.Cal = tk.Text(self.bottom_right,height=8,width=0,background='black', fg = 'white')
        self.Cal.insert(tk.INSERT, calendar.month(self.localtime[0], self.localtime[1]))
        self.Cal.pack(side='left',fill='both',expand=True)

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.localtime = time.localtime(time.time())

        self.main_container = tk.Frame(master, background='black')
        self.main_container.pack(side='top',fill='both',expand=True)
        master.minsize(width=1000,height=300)

        self.top_frame = tk.Frame(self.main_container,background='green')
        self.top_frame.pack(side='top',fill='x',expand=False)

        self.bottom_frame = tk.Frame(self.main_container,background='yellow')
        self.bottom_frame.pack(side='bottom',fill='x',expand=False)

        self.top_left = tk.Frame(self.top_frame, background="pink")
        self.top_left.pack(side="left", fill="x", expand=True)

        self.top_right = tk.Frame(self.top_frame, background="blue")
        self.top_right.pack(side="right", fill="x", expand=True)

        self.bottom_right = tk.Frame(self.bottom_frame,background='red')
        self.bottom_right.pack(side='right',fill='x',expand=True)

        self.bottom_left = tk.Frame(self.bottom_frame,background='orange')
        self.bottom_left.pack(side='left',fill='x',expand=True)

        self.createTime()
        self.createCal()

        self.top_left_label = tk.Label(self.top_left, text="Top Left")
        self.top_left_label.pack(side="left")

        self.bottom_left_label = tk.Label(self.bottom_left,text='Bottom Left')
        self.bottom_left_label.pack(side='left')

root = tk.Tk()
root.title('Smart Mirror')
app = Application(root)

#Display live time
def tick():
    global time1
    time2 = time.localtime(time.time())
    if time2 != time1:
        time1 = time2
        app.Time.config(text=time.asctime(time1))
    app.Time.after(200, tick)


'''Draw weather results'''
weatherClassObject = WeatherClass()#Create object of our WeatherClass()
#initialize the weather widgets
imageWidget = tk.Label(root)
labelfont = ('Courier', 20, 'bold')

imageWidget.pack(side="right")
textWidget = tk.Label(root)
textWidget.config(bg='black', fg='white')
textWidget.config(font=labelfont)
textWidget.config(height=3, width=16)
textWidget.pack(expand=tk.NO, fill=tk.BOTH, side='right')

def draw_Weather():
    weatherImage = weatherClassObject.weatherImage
    weatherInfo = str(weatherClassObject.currentWeather) + '\n' + str(weatherClassObject.currentTemperature + 'F')#Get description of weather/ temperature
    imageWidget.config(image=weatherImage) #update image

    textWidget.config(text = weatherInfo) #update text

    print('Updating..')#Testing
    threading.Timer(5, draw_Weather).start()#Updates every x seconds

tick()
draw_Weather()

app.mainloop()
