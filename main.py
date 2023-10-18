import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import requests
import datetime as dt

Time = dt.datetime.now().strftime("%I:%M %p")
day = dt.datetime.now().strftime("%I:%M %c").split()[1]
Date = dt.datetime.now().strftime('%d-%m-%Y')

Celsius = '°C'
BACKGROUND_CANVAS = "#279EFF"
BACKGROUND = "#1297BD"
BACKGROUND2 = "#B6FFFA"
FONT = "Cascadia Mono", 20, "normal"
FONT2 = "Cascadia Mono", 10, "normal"
API_KEY = os.environ["API_KEY"]
Temperature = 0
feels_like = 0
Pressure = 0
Humidity = 0
Visibility = 0
wind_speed = 0
x_pos_footer = 55
y_pos_footer = 95
FILL_TEXT = BACKGROUND


def Fetch_data():
    CITY = entry.get()
    global Temperature, Humidity, Pressure, Visibility, wind_speed, feels_like
    ENDPOINT = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    print(CITY)
    try:
        res = requests.get(ENDPOINT)
        if res.status_code == 200:
            weather = res.json()
            Temperature = round(weather['main']['temp'])
            feels_like = weather['main']['feels_like']
            wind_speed = weather['wind']['speed']
            wind_deg = weather['wind']['deg']
            Humidity = weather['main']['humidity']
            Pressure = weather['main']['pressure']
            Visibility = weather['visibility']
            Updating()
        else:
            messagebox.showerror(title="Error", message=f"{CITY} Not Found")
    except:
        messagebox.showerror(title="Error", message="Failed to fetch the data")


def Updating():
    canvas_temp.itemconfig(temp_text, text=f"     {Temperature}{Celsius}\nFeelsLike:{feels_like}{Celsius}")
    canvas_pressure.itemconfig(pressure_text, text=f"{Pressure} pas")
    canvas_wind.itemconfig(wind_text, text=f"{wind_speed} km/h")
    canvas_humidity.itemconfig(humidity_text, text=f"{Humidity} g/kg")
    canvas_uv_index.itemconfig(visibility_text, text=f"{Visibility} m")


# ---------------UI AREA---------------------
window = tk.Tk()
window.geometry("600x600")
window.title("Weather App")

image_ori = Image.open("Assets/weather_backg.png")
resize = image_ori.resize((600, 600))
photo = ImageTk.PhotoImage(resize)
canvas = tk.Canvas(width=600, height=600)
canvas.create_image(300, 300, image=photo)
canvas.place(x=0, y=0)

thermo = Image.open("Assets/thermometer.png")
resize_thermo = thermo.resize((60, 60))
thermo_photo = ImageTk.PhotoImage(resize_thermo)

wind = Image.open("Assets/windspeed.png")
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

entry = tk.Entry()
entry.config(font=FONT, bg=BACKGROUND_CANVAS, fg="white", width=20)
entry.place(x=15, y=15)

button = tk.Button(text="Search", width=15, bg=BACKGROUND_CANVAS, pady=5, font=("Arial", 12, "normal"),
                   command=Fetch_data)
button.place(x=380, y=15)

canvas_temp = tk.Canvas(width=150, height=150, background=BACKGROUND_CANVAS, highlightthickness=0)
canvas_temp.place(x=8, y=80)
canvas_temp.create_image(75, 35, image=thermo_photo)
temp_text = canvas_temp.create_text(85, 95, text=f"waiting..", font=FONT2, fill="white")

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

canvas_date_time = tk.Canvas(width=150, height=150, background=BACKGROUND_CANVAS, highlightthickness=0)
canvas_date_time.place(x=430, y=80)
canvas_date_time.create_text(x_pos_footer + 8, 20, text=f"{Time}", font=("Cascadia Mono", 20, "bold"), fill="white")
canvas_date_time.create_text(22, 60, text=f"{day}", font=("Cascadia Mono", 15, "bold"), fill="white")
canvas_date_time.create_text(x_pos_footer + 3, 100, text=f"{Date}", font=("Cascadia Mono", 15, "bold"), fill="white")

window.mainloop()

# -------------getting data ---------------#
