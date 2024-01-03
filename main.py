import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, Scale

import os
import requests
import datetime as dt
import database as db

Time = dt.datetime.now().strftime("%I:%M %p")
day = dt.datetime.now().strftime("%I:%M %c").split()[1]
Date = dt.datetime.now().strftime('%d-%m-%Y')
API_KEY = os.environ["API_KEY"]

bac = "#009DFF"

Celsius = '°C'
BACKGROUND_CANVAS = bac
BACKGROUND = "#1297BD"
BACKGROUND2 = "#B6FFFA"
FONT = "Cascadia Mono", 20, "normal"
FONT2 = "Cascadia Mono", 10, "normal"
CityName = ""
Temperature = 0
feels_like = 0
Pressure = 0
Humidity = 0
Visibility = 0
wind_speed = 0
DESCRIPTION = 0
x_pos_footer = 55
y_pos_footer = 95
FILL_TEXT = BACKGROUND
x = 1


def Backend():
    databa = db.DataBase()
    # databa.createTable()
    # databa.insertData(Date, CityName, Temperature, Humidity, DESCRIPTION, wind_speed, Visibility, Pressure)
    # databa.deleteAllRecords()
    databa.viewData()
    # databa.deleteAllRecords()
    databa.close()


def Fetch_data():
    global Temperature, Humidity, Pressure, Visibility, wind_speed, feels_like, DESCRIPTION, CityName
    CityName = entry.get()
    if len(CityName) == 0:
        messagebox.showerror(message="City name should not be empty")
    else:
        try:
            ENDPOINT = f"https://api.openweathermap.org/data/2.5/weather?q={CityName}&appid={API_KEY}&units=metric"
            res = requests.get(ENDPOINT)
            if res.status_code == 200:
                weather = res.json()
                CityName = weather['name']
                Temperature = round(weather['main']['temp'])
                feels_like = weather['main']['feels_like']
                wind_speed = weather['wind']['speed']
                Humidity = weather['main']['humidity']
                Pressure = weather['main']['pressure']
                Visibility = weather['visibility']
                DESCRIPTION = str(weather['weather'][0]["description"]).capitalize()
                Updating()
            else:
                messagebox.showerror(title="Error", message=f"{CityName} Not Found", font=("Monospace", 10))
        except:
            messagebox.showerror(title="Error", message="𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙛𝙚𝙩𝙘𝙝 𝙩𝙝𝙚 𝙙𝙖𝙩𝙖")


def Updating():
    canvas_temp.itemconfig(temp_text, text=f"     {Temperature}{Celsius}\nFeelsLike:{feels_like}{Celsius}")
    temperature.itemconfig(t, text=f"{Temperature}{Celsius}")
    canvas_pressure.itemconfig(pressure_text, text=f"{Pressure} pas")
    canvas_wind.itemconfig(wind_text, text=f"{wind_speed} km/h")
    canvas_humidity.itemconfig(humidity_text, text=f"{Humidity} g/kg")
    canvas_uv_index.itemconfig(visibility_text, text=f"{Visibility} m")
    des_can.itemconfig(des, text=DESCRIPTION)
    Backend()


def Exit():
    window.destroy()


# ---------------UI AREA--------------------- #
window = tk.Tk()
window.geometry("600x610")
window.title("Weather App")

image_ori = Image.open("Assets/weather_background.png")
resize = image_ori.resize((600, 600))
photo = ImageTk.PhotoImage(resize)
canvas = tk.Canvas(width=600, height=600)
canvas.create_image(300, 300, image=photo)
canvas.place(x=0, y=0)

menu = Image.open('Assets/menu.png')
resize_menu = menu.resize((10, 10))
menu1 = ImageTk.PhotoImage(image=resize_menu)
Menubar = tk.Menu(window, bg='red')
file_menu = tk.Menu(Menubar, tearoff=0)
file_menu.add_command(label='to')
Menubar.add_cascade(menu=file_menu, font=FONT2, label="Menu bar")
window.config(menu=Menubar)

# -----------------IMAGES SECTION -----------------#

thermo = Image.open("Assets/thermometer.png")
resize_thermo = thermo.resize((60, 60))
thermo_photo = ImageTk.PhotoImage(resize_thermo)

wind = Image.open("Assets/wind_speed.png")
resize_wind = wind.resize((60, 60))
wind_ima = ImageTk.PhotoImage(resize_wind)

humidity = Image.open("Assets/humidity.png")
resize_humidity = humidity.resize((60, 60))
humidity_img = ImageTk.PhotoImage(resize_humidity)

pressure = Image.open("Assets/pressure.png")
resize_pressure = pressure.resize((60, 60))
pressure_img = ImageTk.PhotoImage(resize_pressure)

visibility = Image.open("Assets/visibility.png")
resize_vs = visibility.resize((60, 60))
visibility_img = ImageTk.PhotoImage(resize_vs)

# -----------------------ELEMENTS ---------------------#
entry = tk.Entry()
entry.config(font=FONT, bg=BACKGROUND_CANVAS, fg="white", width=25)
entry.insert(0, 'hyderabad')
entry.place(x=15, y=15)

button = tk.Button(text="Search", width=15,
                   bg=BACKGROUND_CANVAS, pady=5,
                   font=("Arial", 12, "normal"),
                   activebackground=BACKGROUND_CANVAS,
                   command=Fetch_data)
button.place(x=430, y=15)

canvas_temp = tk.Canvas(window, width=150, height=150, background=bac, highlightthickness=0)
canvas_temp.place(x=8, y=80)
canvas_temp.create_image(75, 35, image=thermo_photo)
temp_text = canvas_temp.create_text(85, 95, text=f"waiting..", font=FONT2, fill="white")

temperature = tk.Canvas(width=150, height=100, background=BACKGROUND_CANVAS, highlightthickness=0)
temperature.place(x=220, y=100)
t = temperature.create_text(75, 65, text="", font=('Arial', 50, 'normal'), fill="white")

des_can = tk.Canvas(width=260, height=35, bg=BACKGROUND_CANVAS, highlightthickness=0)
des = des_can.create_text(130, 15, text='', fill='white', font=("Cascadia Mono", 20, 'normal'))
des_can.place(x=160, y=210)

# ----------------------FOOTER DATA----------------#
canvas_wind = tk.Canvas(width=130, height=120, background=BACKGROUND2, highlightthickness=0)
canvas_wind.place(x=10, y=450)
canvas_wind.create_image(65, 35, image=wind_ima)
wind_text = canvas_wind.create_text(x_pos_footer, y_pos_footer, text=f"  waiting..", font=FONT2, fill=FILL_TEXT)
canvas_wind.create_text(60, 75, text="Wind speed", font=FONT2, fill=FILL_TEXT)

canvas_humidity = tk.Canvas(width=130, height=120, background=BACKGROUND2, highlightthickness=0)
canvas_humidity.place(x=160, y=450)
canvas_humidity.create_image(65, 35, image=humidity_img)
humidity_text = canvas_humidity.create_text(x_pos_footer, y_pos_footer, text=f"   waiting..", font=FONT2,
                                            fill=FILL_TEXT)
canvas_humidity.create_text(60, 75, text="Humidity", font=FONT2, fill=FILL_TEXT)

canvas_pressure = tk.Canvas(width=130, height=120, background=BACKGROUND2, highlightthickness=0)
canvas_pressure.place(x=310, y=450)
canvas_pressure.create_image(65, 35, image=pressure_img)
pressure_text = canvas_pressure.create_text(x_pos_footer, y_pos_footer, text=f"   waiting..", font=FONT2,
                                            fill=FILL_TEXT)
canvas_pressure.create_text(60, 75, text="Pressure", font=FONT2, fill=FILL_TEXT)

canvas_uv_index = tk.Canvas(width=130, height=120, background=BACKGROUND2, highlightthickness=0)
canvas_uv_index.place(x=460, y=450)
canvas_uv_index.create_image(65, 35, image=visibility_img)
visibility_text = canvas_uv_index.create_text(x_pos_footer, y_pos_footer, text=f"  waiting..", font=FONT2,
                                              fill=FILL_TEXT)
canvas_uv_index.create_text(60, 75, text="Visibility", font=FONT2, fill=FILL_TEXT)

# -----------------DATE ANG TIME------------------#
canvas_date_time = tk.Canvas(width=150, height=150, background=BACKGROUND_CANVAS, highlightthickness=0)
canvas_date_time.place(x=450, y=80)
canvas_date_time.create_text(x_pos_footer + 8, 20, text=f"{Time}", font=("Cascadia Mono", 20, "bold"), fill="white")
canvas_date_time.create_text(22, 60, text=f"{day}", font=("Cascadia Mono", 15, "bold"), fill="white")
canvas_date_time.create_text(x_pos_footer + 3, 100, text=f"{Date}", font=("Cascadia Mono", 15, "bold"), fill="white")

exit_button = tk.Button(background='red', text="exit", command=Exit, width=15, font=FONT2)
exit_button.place(x=240, y=575)
# Fetch_data()
# scale = Scale(window, from_=100, to=0, length=200,
#               orient='vertical',
#               tickinterval=10,
#               font=FONT2,
#               fg='white',
#               bg=BACKGROUND_CANVAS,
#               highlightthickness=0,
#               troughcolor="white"
#               )
# scale.set(feels_like)

#
# scale.place(x=0, y=200)

window.mainloop()


# scale.set(Temperature)
# scale.config(state='disabled')
