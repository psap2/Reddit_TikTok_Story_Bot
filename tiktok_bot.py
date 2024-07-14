from selenium import webdriver
import time, requests, csv, random, queue, threading, logging
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
from get_proxies import get_free_proxies


def load_videos_data(filename):
    video_links = []
    with open(filename, 'r') as tiktok_data:
        csv_reader = csv.reader(tiktok_data)
        next(csv_reader) #skips the header

        for line in csv_reader:
            video_links.append(line[45])
    
    return video_links

def downloadVideo(link, id):
    cookies = {
        '_ga': 'GA1.1.1380945801.1715998694',
        '_ga_ZSF3D6YSLC': 'GS1.1.1715998694.1.1.1715998888.0.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,tr;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.1380945801.1715998694; _ga_ZSF3D6YSLC=GS1.1.1715998694.1.1.1715998888.0.0.0',
        'dnt': '1',
        'hx-current-url': 'https://ssstik.io/',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'eGo3bjQ1',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]

    mp3File = urlopen(downloadLink)
    with open("videos/{id}.mp3", "wb") as output:
        while True:
            data = mp3File.read(4096)
            if data: 
                output.write(data)
            else:
                break

video_links = load_videos_data("tiktokWebscraped.csv")

#overcome TikTok human verification with ip rotation
proxies = get_free_proxies()

#validate proxies
q = queue.Queue()
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


def random_proxy(list_proxies):
    i = random.randrange(0,len(list_proxies))
    return proxies[i]


video_id = 0

for link in video_links:
    video_id += 1 
    #waiting for first proxy validation
    time.sleep(15)
    proxy = random_proxy(working_proxies)
    options = webdriver.ChromeOptions()
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    # Check for human verfication
    time.sleep(13)
    try:
        if driver.find_element(By.CLASS_NAME, value="verify-bar-close sc-chPdSV PffVT"):
            x_button = driver.find_element(By.ID, "verify-bar-close")
            x_button.click()
    except:
        pass
    soup = BeautifulSoup(driver.page_source, "html.parser")
    downloadVideo(link, video_id)
    time.sleep(10)