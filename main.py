import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key=os.environ.get("OWN_API_KEY")
account_sid="AC129856c8137db2b505da8ea6d845e856"
auth_token=os.environ.get("AUTH_TOKEN")
LAT=30.940990
LON=74.617043

parameters={
    "lat":LAT,
    "lon":LON,
    "appid":api_key,
    "exclude":"current,minutely,daily"
}
response=requests.get(url="https://api.openweathermap.org/data/2.5/onecall",params=parameters)
response.raise_for_status()
data=response.json()
hour_data=data["hourly"]

will_rain=False

for i in hour_data[:12]:
    if i["weather"][0]["id"]<700:
        will_rain=True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token,http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_="+12696821892",
        to="+91 89684 24331"
    )
    print(message.status)

