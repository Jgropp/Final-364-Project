import requests
import sqlite3
response = requests.get("https://api.usa.gov/crime/fbi/ucr/ct/count/national/location_name?page=1&per_page=10&output=json&api_key=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv")
data=response.json()

print(((data["results"])[0])['count'])



