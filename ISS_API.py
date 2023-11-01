import requests
from datetime import datetime
import smtplib
import math
import time

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

longitude = data["iss_position"]["longitude"]
longitude = float(longitude)

latitude = float(data["iss_position"]["latitude"])


my_lat = 40.656586
my_lng = -7.912471

parameters = {
    "lat": 40.656586,
    "lng": -7.912471,
    "formatted" : 0
}
sun = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
sun.raise_for_status()
sunrise = sun.json()["results"]["sunrise"]
sunrise = sunrise.split("T")
sunrise = sunrise[1]
sunrise = sunrise.split(":")
sunrise = sunrise[0]
sunset = sun.json()["results"]["sunset"]
sunset = sunset.split("T")[1].split(":")[0]

time_now = datetime.now()

# is it night ?
is_night = None
if str(time_now.hour) >= sunset or str(time_now.hour) <= sunrise:
    is_night = True
else:
    is_night = False

# Is the ISS Close?
iss_close = False
if math.isclose(my_lat, latitude, abs_tol=0.2) == True \
    and math.isclose(my_lng, longitude, abs_tol=0.2) == True:
    iss_close = True

# send email
my_email = "mightypython8@gmail.com"
with open("mail,pass.txt") as p:
    password = p.readlines()[1].split('"')[1]


while True:
    time.sleep(120)
    if is_night and iss_close:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()

            connection.login(user=my_email, password=password)

            connection.sendmail(from_addr=my_email, to_addrs=my_email,
                                msg=f"Subject:Look Up\n\nThe ISS is close, look up! :) ")


