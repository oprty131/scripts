import ssl
import time
import queue
import threading
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
from http import cookiejar
import requests
from flask import Flask, render_template, request, redirect, url_for

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
r = requests.Session()
countQueue = queue.Queue()
sentRequests = 0
completed = False

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

r.cookies.set_policy(BlockCookies())

# Simulated Data for UserAgent and Device Types
UserAgent = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Nexus 5X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]
DeviceTypes = ["iPhone", "Android", "iPad"]
Platforms = ["android", "ios", "web"]
Channel = ["tiktok_web", "musically_go"]
ApiDomain = ["api.tiktok.com"]

def sendView(itemID):
    proxy = {f'{proxyType}': f'{proxyType}://{choice(proxyList)}'}
    platform = choice(Platforms)
    osVersion = randint(1, 12)
    DeviceType = choice(DeviceTypes)
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": choice(UserAgent)
    }
    appName = choice(["tiktok_web", "musically_go"])
    Device_ID = randint(1000000000000000000, 9999999999999999999)
    apiDomain = choice(ApiDomain)
    channelLol = choice(Channel)
    URI = f"https://{apiDomain}/aweme/v1/aweme/stats/?channel={channelLol}&device_type={DeviceType}&device_id={Device_ID}&os_version={osVersion}&version_code=220400&app_name={appName}&device_platform={platform}&aid=1988"
    data = f"item_id={itemID}&play_delta=1"

    try:
        req = r.post(URI, headers=headers, data=data, proxies=proxy, timeout=5, verify=False)
        return True
    except Exception as e:
        print(f"Error in sendView: {e}")
        return False

def sendShare(itemID):
    proxy = {f'{proxyType}': f'{proxyType}://{choice(proxyList)}'}
    platform = choice(Platforms)
    osVersion = randint(1, 12)
    DeviceType = choice(DeviceTypes)
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": choice(UserAgent)
    }
    appName = choice(["tiktok_web", "musically_go"])
    Device_ID = randint(1000000000000000000, 9999999999999999999)
    apiDomain = choice(ApiDomain)
    channelLol = choice(Channel)
    URI = f"https://{apiDomain}/aweme/v1/aweme/stats/?channel={channelLol}&device_type={DeviceType}&device_id={Device_ID}&os_version={osVersion}&version_code=220400&app_name={appName}&device_platform={platform}&aid=1988"
    data = f"item_id={itemID}&share_delta=1"

    try:
        req = r.post(URI, headers=headers, data=data, proxies=proxy, timeout=5, verify=False)
        return True
    except Exception as e:
        print(f"Error in sendShare: {e}")
        return False

def clearURL(link):
    parsedURL = urlparse(link)
    host = parsedURL.hostname.lower()
    if "vm.tiktok.com" == host or "vt.tiktok.com" == host:
        UrlParsed = urlparse(r.head(link, verify=False, allow_redirects=True, timeout=5).url)
        return UrlParsed.path.split("/")[3]
    else:
        UrlParsed = urlparse(link)
        return UrlParsed.path.split("/")[3]

def processThread(sendProcess, itemID):
    while not completed:
        if sendProcess(itemID):
            countQueue.put(1)

def countThread(amount):
    global sentRequests, completed
    while True:
        countQueue.get()
        sentRequests += 1
        if amount > 0 and sentRequests >= amount:
            completed = True

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        amount = int(request.form['amount'])
        send_type = int(request.form['send_type'])  # 0 for views, 1 for shares

        itemID = clearURL(video_url)

        # Start processing threads
        global proxyList
        proxyList = []  # You need to implement your proxy loading logic here
        proxyChoose = True
        while proxyChoose:
            proxyType = request.form.get('proxy_type')
            if proxyType in ["http", "socks4", "socks5"]:
                proxyChoose = False

        if send_type == 0:
            sendProcess = sendView
        elif send_type == 1:
            sendProcess = sendShare

        threading.Thread(target=countThread, args=(amount,)).start()
        for n in range(10):  # Number of threads
            threading.Thread(target=processThread, args=(sendProcess, itemID)).start()

        return redirect(url_for('progress'))

    return render_template('index.html')

@app.route('/progress')
def progress():
    return f"Sent Requests: {sentRequests}, Completed: {completed}"

if __name__ == "__main__":
    app.run(debug=True)
