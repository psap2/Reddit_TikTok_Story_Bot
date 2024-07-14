import requests, queue, threading, time
from get_proxies import get_free_proxies

q = queue.Queue()
proxies = get_free_proxies()
working_proxies = []


for proxy in proxies:
    q.put(proxy)

def check_proxies():
    global q, working_proxies
    while not q.empty():
        proxy = q.get()
        try:
            response = requests.get("http://ipinfo.io/json", 
                                    proxies={"http": proxy,
                                            "https": proxy})
        except:
           continue

        if response.status_code == 200:
            working_proxies.append(proxy)
            
for t in range(10):
     threading.Thread(target=check_proxies).start()
