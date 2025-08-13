from bs4 import BeautifulSoup
import smtplib
import requests
import os
from dotenv import load_dotenv

# Load all of the environment variables
load_dotenv()

LINK = "https://www.amazon.com/dp/B075CYMYK6?th=1"

# change the parameters for your browser, you can also add some more parameters if you want to (check your header here: https://myhttpheader.com/)
header = {"User-Agent": "",
          "Accept-Language": ""}

response = requests.get(LINK,headers=header)


soup = BeautifulSoup(response.text,"html.parser")
# print(soup.prettify())

# If it doesen't work, inspect the page and check if the class has changed or the price has been moved somewhere else
price = str(soup.find(name="span",class_="a-offscreen").text)
price = float(price.replace("$",""))

# Set your target price if needed
if price < 100:
    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
        connection.sendmail(from_addr=os.environ["EMAIL_ADDRESS"],to_addrs=os.environ["EMAIL_ADDRESS"],msg=f"Subject: Amazon price alert\nInstant pot is now {price}$\nlink: {LINK}")

