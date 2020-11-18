from bs4 import BeautifulSoup
import requests
import time 
import json
from datetime import datetime, timedelta
import os 
import sys 

limit = 100
# start = round(time.time())
# end = round(time.time() + 31622400)

url = f"https://ctftime.org/api/v1/events/?limit={limit}"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

r = requests.get(url=url, headers=headers)
table = r.json()

if len(sys.argv) > 2:
    dir_path = sys.argv[1]
else:
    dir_path = os.path.dirname(os.path.realpath(__file__))

print(f"\n\033[1m \033[95m [INFO] \033[0m : Reading from source \n\t\t -> {url}\n")

try:
    # name, event_type, date start, date end, sitelink
    with open(dir_path + "/table.csv", "w+") as f:
        f.write(f"name, Format, Start, End, Site\n")
        for t in table:
            #print(t)
            title = t["title"]
            start = datetime.strptime(t["start"].split('+')[0],"%Y-%m-%dT%H:%M:%S")  + timedelta(hours=1)
            start_convert = start.strftime("%d-%m-%Y %H:%M")
            end = datetime.strptime(t["finish"].split('+')[0], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=1)
            end_convert = end.strftime("%d-%m-%Y %H:%M") 
            event_type = t["format"]
            url = t["url"]

            print(f"\033[1m \033[96m [CTF] \033[0m : {title}, {event_type}, {start}, {end}, {url}")
            f.write(f"{title}, {event_type}, {start}, {end}, {url}\n")

except Exception as e:
    print(f"\033[1m \033[91m [ERROR] \033[0m : {e}")

print(f"\n\033[1m \033[92m [DONE] \033[0m : Table created at {dir_path}\n")

