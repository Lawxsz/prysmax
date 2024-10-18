@echo off
echo Installing required Python libraries...

REM Install the required libraries, ignoring errors
pip install requests 2>nul
pip install wmi 2>nul
pip install psutil 2>nul
pip install pyarmor==7.6.1 2>nul
pip install pyinstaller 2>nul
pip install Pillow 2>nul
pip install discord-webhook 2>nul
pip install pycryptodomex 2>nul
pip install pycryptodome 2>nul
pip install pywin32 2>nul
pip install customtkinter 2>nul

echo All libraries installed. Now running setup.py...

REM Execute setup.py
python setup.py

pause