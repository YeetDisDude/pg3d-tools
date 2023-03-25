import os, time, sys, random, json, time, asyncio, subprocess
filepath = os.path.abspath(__file__)
filename = os.path.basename(__file__)
folderpath = os.getcwd()
operatingsys = os.name
needed = []

modules = [
    ("rich", "from rich.console import Console"),
    ("colorama", "import colorama"),
    ("httpx", "import httpx"),
    ("requests", "import requests"),
    ("pyperclip", "import pyperclip"),
    ("urllib", "import urllib"),
    ("threading", "import threading"),
    ("websockets", "from websockets import connect"),
]

needed = []
for module, import_string in modules:
    try:
        exec(import_string)
    except ImportError:
        needed.append(module)

if len(needed) != 0:
    count = 0
    for module in needed:
        count += 1
        print(f"[i] Installing Required Modules... | {count} / {len(needed)}")
        subprocess.check_call(["pip3", "install", module, "-q"])

from rich.console import Console; console = Console()
from rich.text import Text
from rich import print
from rich.panel import Panel
from colorama import Fore, init
import httpx, requests, pyperclip, urllib, threading, asyncio
from rich.progress import track
from websockets import connect


def clear():
    if operatingsys == 'nt':
        os.system("cls")
    else:
        os.system("clear")

VERSION_URL = "https://raw.githubusercontent.com/YeetDisDude/pg3d-tools/main/version.txt"
VERSION = "0.1.2"

clear()
    
banner = f"""

[indian_red]██████[light_salmon1]╗  [indian_red]██████[light_salmon1]╗ [indian_red]██████[light_salmon1]╗ [indian_red]██████[light_salmon1]╗   [indian_red]████████[light_salmon1]╗ [indian_red]█████[indian_red]╗  [indian_red]█████[light_salmon1]╗ [indian_red]██[light_salmon1]╗      [indian_red]██████[light_salmon1]╗
[indian_red]██[light_salmon1]╔══[indian_red]██[light_salmon1]╗[indian_red]██[light_salmon1]╔════╝ ╚════[indian_red]██[light_salmon1]╗[indian_red]██[light_salmon1]╔══[indian_red]██[light_salmon1]╗  ╚══[indian_red]██[light_salmon1]╔══╝[indian_red]██[light_salmon1]╔══[indian_red]██[light_salmon1]╗[indian_red]██[light_salmon1]╔══[indian_red]██[light_salmon1]╗[indian_red]██[light_salmon1]║    [indian_red] ██[light_salmon1]╔════╝
[indian_red]██████[light_salmon1]╔╝[indian_red]██[light_salmon1]║  [indian_red]██[light_salmon1]╗  [indian_red]█████[light_salmon1]╔╝[indian_red]██[light_salmon1]║  [indian_red]██[light_salmon1]║     [indian_red]██[light_salmon1]║   [indian_red]██[light_salmon1]║  [indian_red]██[light_salmon1]║[indian_red]██[light_salmon1]║  [indian_red]██[light_salmon1]║[indian_red]██[light_salmon1]║     ╚[indian_red]█████[light_salmon1]╗ 
[indian_red]██[light_salmon1]╔═══╝ [indian_red]██[light_salmon1]║  ╚[indian_red]██[light_salmon1]╗ ╚═══[indian_red]██[light_salmon1]╗[indian_red]██[light_salmon1]║  [indian_red]██[light_salmon1]║     [indian_red]██[light_salmon1]║   [indian_red]██[light_salmon1]║  [indian_red]██[light_salmon1]║[indian_red]██[light_salmon1]║  [indian_red]██[light_salmon1]║[indian_red]██[light_salmon1]║      [light_salmon1]╚═══[indian_red]██[light_salmon1]╗
[indian_red]██[light_salmon1]║     [light_salmon1]╚[indian_red]██████[light_salmon1]╔╝[indian_red]██████[light_salmon1]╔╝[indian_red]██████[light_salmon1]╔╝     [indian_red]██[light_salmon1][light_salmon1]║   ╚[indian_red]█████[light_salmon1][light_salmon1]╔╝╚[indian_red]█████[light_salmon1][light_salmon1]╔╝[indian_red]███████[light_salmon1][light_salmon1]╗[indian_red]██████[light_salmon1]╔╝
[light_salmon1]╚═╝      ╚═════╝ ╚═════╝ ╚═════╝      ╚═╝    ╚════╝  ╚════╝ ╚══════╝╚═════╝[/]"""

console_text = f"""
 [bold deep_sky_blue1][1][/] Check ban                                │               [bold deep_sky_blue1][11][/] Find Weapon ID                         │
 [bold deep_sky_blue1][2][/] Download Dump.cs files                   │               [bold deep_sky_blue1][12][/] Find Wear ID                           │
 [bold deep_sky_blue1][3][/] Download Assembly-CSharp.dll files       │               [bold deep_sky_blue1][13][/] Find Item Record                       │
 [bold deep_sky_blue1][4][/] Get Cheater Currency Threshold           │               [bold deep_sky_blue1][14][/] Search Websocket Commands              │
 [bold deep_sky_blue1][5][/] Update Player Logs                       │               [bold deep_sky_blue1][15][/]                                        │
 [bold deep_sky_blue1][6][/] Spam Lightmap Contacts                   │               [bold deep_sky_blue1][16][/]                                        │
 [bold deep_sky_blue1][7][/] Make Unsearchable Username               │               [bold deep_sky_blue1][17][/]                                        │
 [bold deep_sky_blue1][8][/] iOS Skin Plist Generator                 │               [bold deep_sky_blue1][18][/]                                        │
 [bold deep_sky_blue1][9][/] Get All Scene Names                      │               [bold deep_sky_blue1][19][/]                                        │
 [bold deep_sky_blue1][10][/] Send Websocket Commands                 │               [bold deep_sky_blue1][20][/]                                        │

 [bold deep_sky_blue1][0][/] Exit [bold deep_sky_blue1][C][/] Credits
    """

def checkUpdate():
    tab_title = 'echo "\033]0;%s\007"' % f"Checking for Update..."; os.system(tab_title); clear()
    console.print(banner, justify="center"); console.print("Checking for updates...", justify="center")
    r = httpx.get(VERSION_URL)
    r.raise_for_status()
    latest_version = r.text.strip()
    if latest_version != VERSION:
        console.print(f"[red][!][/] PG3D Tools version [underline bold]{VERSION}[/] is outdated. Please download the new version from GitHub.\n[underline]https://github.com/YeetDisDude/pg3d-tools[/] Latest | version {r.text}", highlight=False)
        exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")
        sys.exit()
    else:
        console.print(f"[green][+][/][underline bold] PG3D Tools is up-to-date.[/]")

def hyperlink(url: str):
    return f"\033]8;;{url}\033\\{url}\033]8;;\033\\"

def panel():
    clear()
    console.print(Panel.fit(console_text, title=f"Pixel Gun 3D Tools [underline indian_red]{VERSION}", subtitle="[underline bold]https://yeetdisdude.xyz | discord.gg/wnr9ME7enQ"), justify="center")

def encodejsonurl(dict):
    return urllib.parse.quote(json.dumps([dict]))

checkUpdate()

while True:
    tab_title = 'echo "\033]0;%s\007"' % f"PG3D Tools {VERSION}"; os.system(tab_title)
    panel()
    choice = input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Enter your choice: ")
    if choice == "0":
        clear(); console.print(f"Exiting...", style="bold", justify="center"); sys.exit()

    if choice == "c" or choice == "C":
        tab_title = 'echo "\033]0;%s\007"' % f"Credits"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Credits", justify="center")
        console.print(f"""
[underline]YeetDisDude#0001[/] - Making this | {hyperlink("https://github.com/YeetDisDude")}
[underline]Pulsed#1874[/] - Making Import Handler & Websocket Feature | {hyperlink("https://github.com/ChrxnZ")}
[underline]TonicBoomerKewl[/] - Item Record and ws cmds | {hyperlink("https://github.com/TonicBoomerKewl")}\n""", highlight=False)
        input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")

    if choice == "1":               # check ban
        tab_title = 'echo "\033]0;%s\007"' % f"Ban Checker"; os.system(tab_title)
        clear()
        console.print(banner, justify="center"); console.print("Download Ban Checker", justify="center")
        console.print("Enter [underline bold]0[/] to exit.", highlight=False, justify="center")
        while True:
            id = str(input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Enter the ID of the user: "))
            if id == "0":
                break
            try:
                checkforexception = int(id)
                response = httpx.post("https://secure.pixelgunserver.com/pixelgun3d-config/getBanList.php", data={'type_device': int(random.random() * 69), 'id': id}).text
                if response == "1":
                    console.print(f"[red][!][/] ID [underline bold]{id}[/] Is Banned.", highlight=False)
                else:
                    console.print(f"[green][!][/] ID [underline bold]{id}[/] Is Not Banned.", highlight=False)
            except ValueError:
                console.print(f'[red][!][/] ID "[red]{id}[/]" Is Not Valid.', highlight=False)


    if choice == "2":                # download dump.cs
        tab_title = 'echo "\033]0;%s\007"' % f"Download dump.cs"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Download Dump.cs", justify="center")
        try:
            response = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/dumpcs.json")
        except httpx.NetworkError:
            console.print("[red][!][/] Something went wrong while fetching the versions list, please make sure you have an internet connection.", highlight=False); sys.exit()
        else:
            data = json.loads(response.text)
            console.print("Available Versions:", highlight=False)
            for version in data['versions']:
                console.print(version, highlight=False)
            version_to_download = input(f"{Fore.LIGHTCYAN_EX}[!]{Fore.RESET} Enter the version you want to download from the list above: ")
            if version_to_download in data['versions']:
                console.print(f"[green][!][/] Version {version_to_download}'s dump.cs is available for download.", highlight=False)
                download = input(f"{Fore.GREEN}[i]{Fore.RESET} Download? (Y/N) : ")
                if download == "Y" or download == "y" or download == "yes" or download == "Yes":
                    data = response.json()
                    key = version_to_download
                    url = data["versions"][key]
                    response = requests.get(url, stream=True)

                    file_size = int(response.headers.get("Content-Length", 0))
                    os.makedirs("downloads", exist_ok=True)
                    with open(f"downloads/{version_to_download}.cs", "wb") as f:
                        for chunk in track(response.iter_content(chunk_size=1024), total=file_size//1024 + 1, description="Downloading..."):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                    exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Download Completed, press enter to exit... | Saved to {folderpath}\downloads\{version_to_download}.cs")
                else:
                    exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")
            else:
                console.print(f"[red][!][/] Version {version_to_download}'s dump.cs is not available for download.", highlight=False); exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")


    if choice == "3":                # download assembly-csharp.dll
        tab_title = 'echo "\033]0;%s\007"' % f"Download Assembly-CSharp.dll"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Download Assembly-CSharp.dll", justify="center")
        try:
            response = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/assembly-csharp.json")
        except httpx.NetworkError:
            console.print("[red][!][/] Something went wrong while fetching the versions list, please make sure you have an internet connection.", highlight=False); sys.exit()
        else:
            data = json.loads(response.text)
            console.print("Available Versions:", highlight=False)
            for version in data['versions']:
                console.print(version, highlight=False)
            version_to_download = input(f"{Fore.LIGHTCYAN_EX}[!]{Fore.RESET} Enter the version you want to download from the list above: ")
            if version_to_download in data['versions']:
                console.print(f"[green][!][/] Version {version_to_download}'s assembly is available for download.", highlight=False)
                download = input(f"{Fore.GREEN}[i]{Fore.RESET} Download? (Y/N) : ")
                if download == "Y" or download == "y" or download == "yes" or download == "Yes":
                    data = response.json()
                    key = version_to_download
                    url = data["versions"][key]
                    response = requests.get(url, stream=True)

                    file_size = int(response.headers.get("Content-Length", 0))
                      
                    with open(f"downloads/{version_to_download}.dll", "wb") as f:
                        for chunk in track(response.iter_content(chunk_size=1024), total=file_size//1024 + 1, description="Downloading..."):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                    exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Download Completed, press enter to exit... | Saved to {folderpath}\downloads\{version_to_download}.dll")
                else:
                    exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")
            else:
                console.print(f"[red][!][/] Version {version_to_download}'s assembly is not available for download.", highlight=False); exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")

        
    if choice == "4":
        tab_title = 'echo "\033]0;%s\007"' % f"Get Currency Threshold"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Get Currency Threshold", justify="center")
        platform = input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Select a platform\n     {Fore.LIGHTBLUE_EX}[1]{Fore.RESET} iOS\n     {Fore.LIGHTBLUE_EX}[2]{Fore.RESET} Android\n")
        if platform == "1": # iOS
            console.print("[green][!][/] Sending Request to Pixel Gun 3D Servers...", highlight=False)
            r = httpx.get("https://secure.pixelgunserver.com/pixelgun3d-config/advert-v2/advert-ios.json")
            j = r.json()
            console.print(f"\n[underline]iOS[/] Currency Threshold:\n     Gems  : {j['cheater']['gemThreshold']}\n     Coins : {j['cheater']['coinThreshold']}\n", highlight=False); exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")
        if platform == "2": # Android
            console.print("[green][!][/] Sending Request to Pixel Gun 3D Servers...")
            r = httpx.get("https://secure.pixelgunserver.com/pixelgun3d-config/advert-v2/advert-android.json")
            j = r.json()
            console.print(f"\n[underline]Android[/] Currency Threshold:\n     Gems  : {j['cheater']['gemThreshold']}\n     Coins : {j['cheater']['coinThreshold']}\n", highlight=False); exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")


    if choice == "5": # update player logs
        tab_title = 'echo "\033]0;%s\007"' % f"Update Player Log"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Update Player Logs", justify="center")
        url = "https://pixelgun-cl-stat.pixelgunserver.com/event_stat_add_pl.php"
        id = int(input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Enter User ID: "))
        currency = input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Available Currenies: (ClanSilver, GemsCurrency, Coins, PixelPassCurrency, RouletteAdsCurrency, Coupons, AdventNyCurrency)\nChoose a currency: ")
        amount = int(input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Enter Amount: "))
        times = int(input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Amount of times to send: "))
        parameters = encodejsonurl({"cmid":3783,"eid":1012,"uid": str(id),"dev":1,"c":"NIG","p":1,"v":"69.0.0","r":1,"cid":"1","t":1,"reg":1,"pl":0,"ip1":amount,"sp1":currency,"sp2":"YeetDisDude","ip2":1})

        count = 0
        try:
            for _ in range(times):
                count += 1
                r = requests.post("https://pixelgun-cl-stat.pixelgunserver.com/event_stat_add_pl.php", params=f'muid={str(id)}&events={parameters}')
                console.print(f"[green][!][/] {count} / {times} | Status: [underline]{r.status_code}[/] | Response: [underline]{(r.text.strip())}[/]", highlight=False)
        except requests.exceptions.RequestException:
            console.print("[red][!][/] Something went wrong while sending the request. Please check your internet connection.", highlight=False); sys.exit()
        exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Done. Press enter to exit...")


    if choice == "6": # spam lightmap applications
        tab_title = 'echo "\033]0;%s\007"' % f"Spam Applications"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Spam Lightmap Applications", justify="center")
        name = input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Enter a Name: ")
        message = input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} Enter Message to Spam: ")
        numthreads = int(input(f"{Fore.LIGHTCYAN_EX}[i]{Fore.RESET} (Recommended: 500) Enter Threads: "))
        emails = ["mrbaest@gmail.com", "admin@fbi.gov", "niggerlover69@gmail.com", "admin@niggerprevention.org", "hermesis@nigga.gov", "higuys@yahoo.com", "byeguyshangout@nigga.gov", "blacklivesdontmatter@fbi.gov", "fuck@fuck.com", "abc@defg.hijk", "abc@cba.abc"]
        url = "https://lightmap.com/contact_form"
        def send_request(payload):
            with httpx.Client() as client:
                response = client.post("https://lightmap.com/contact_form", data=payload)
                console.print(f"[green][!][/] Sent | Status: [underline bold]{response.status_code}[/] | Response: [underline bold]{response.text}[/]", highlight=False)
        payload = {"name": name, "email": random.choice(emails), "message": message }
        threads = []
        for i in range(numthreads):
            t = threading.Thread(target=send_request, args=(payload,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Finished Spamming. Press enter to exit...")



    if choice == "7": # make un searchable username
        tab_title = 'echo "\033]0;%s\007"' % f"Make Unsearchable Username"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Generate Unsearchable Username", justify="center")
        username = input(f"{Fore.LIGHTCYAN_EX}[>]{Fore.RESET} Enter your Pixel Gun 3D Username: ")
        if len(username) > 10:
            input(f"{Fore.RED}[!]{Fore.RED} Username must be less than 10 characters.{Fore.RESET}")
        else:
            newusername = f"⁬{username}"
            console.print(f"[green][i][/]New username: {newusername} | Copied to clipboard.")
            pyperclip.copy(newusername)
            input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")

    if choice == "8": # ios skin plist generator
        tab_title = 'echo "\033]0;%s\007"' % f"Skin Plist Generator"; os.system(tab_title); clear(); console.print(banner, justify="center"); console.print("Enter [underline bold]0[/] to exit.", highlight=False, justify="center")
        dictionary = {}
        skinname_dictionary = {}
        count = 1001
        directory = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(directory, "generated")
        if not os.path.exists(folder):
            os.makedirs(folder)
        skin_names = ["YeetDisDude", "yeetdisdude", "ig: y_etd.sdude", "YeetDisDude#0001", "Subscribe", ".gg/wnr9ME7enQ"]
        file = os.path.join(directory, "generated\dict.txt") # path for dict.txt
        formats = ["data:image/png;base64,", "data:image/jpeg;base64,", "data:image/gif;base64,", "data:image/bmp;base64,", "data:image/webp;base64,"]
        while True:
            b64 = input(f"{Fore.LIGHTCYAN_EX}Enter Base64:{Fore.RESET} ")
            if b64 == "0":
                break
            if not b64:
                print(f"[red][!] The input is blank. Please enter a valid base64 string.[/]\n")
                continue
            for format in formats:
                if format in b64:
                    print(f"[red][!][/] prefix found in string, removing...")
                    comma_index = b64.index(",")
                    b64 = b64[comma_index+1:]
                    break
            key = str(count)
            dictionary[key] = b64
            key2 = str(count)
            skinname_dictionary[key2] = random.choice(skin_names)
            count += 1
            console.print(f"[green][!][/] Saved to generated/dict.txt")
            with open(file, "w") as f:
                content = f'''Plist for skins Base64 [THIS FILE WILL BE OVERWRITTEN THE NEXT TIME YOU RUN THE SCRIPT!!!]
User Skins:
    <key>User Skins</key>
    <string>{str(dictionary)}</string>
Plist for Skin Names:
    <key>User Name Skins</key>
    <string>{str(skinname_dictionary)}</string>
Current Equiped Skin:
    <key>Name Current Skin</key>
    <string>1001</string>
\nUsage: Replace the lines in the plist with the lines generated by this script\nhttps://github.com/YeetDisDude/pixel-gun-3d/tree/main/skin%20plist%20gen\nMade by: YeetDisDude'''
                content = content.replace("'", '"')
                f.write(content)


    if choice == "9": # Get all scene names
        tab_title = 'echo "\033]0;%s\007"' % f"Get scene names"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Get Scene Names", justify="center")
        r = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/scenes.json")
        data = r.json()
        for scene in data:
            for key, value in scene.items():
                print(value)
        exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")

    

    if choice == "10":
        tab_title = 'echo "\033]0;%s\007"' % f"Connect to Websocket"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Send Websocket Message", justify="center")
        wsuri = "wss://server-v2.pixelgunserver.com:443/socket.io/?EIO=4&transport=websocket&client_ver=v2"
        async def connectAndSend(message):
            try:
                async with connect(wsuri) as ws:
                    console.print("[yellow1][!][/] Attempting To Handle Websocket Sio Queuer... (0/5)", highlight=False)
                    r = await ws.recv()
                    if r.startswith('0{"sid":'):
                        console.print("[yellow1][!][/] Recieved Session ID (1/5)", highlight=False)
                        r = await ws.recv()
                        if r == "40":
                            console.print("[yellow1][!][/] Recieved Queue Factor (2/5)", highlight=False)
                            await ws.send("40/sio")
                            console.print("[yellow1][!][/] Sent Sio Queue Factor (3/5)", highlight=False)
                            r = await ws.recv()
                            if r == "40/sio":
                                console.print("[yellow1][!][/] Recieved Sio Queue Factor (4/5)", highlight=False)
                                await ws.send('452-/sio,[{"_placeholder":true, "num":0}, {"_placeholder":true, "num":1}]')
                                console.print("[yellow1][!][/] Sent Sio Queue Placeholder Factor (5/5)", highlight=False)
                                await ws.send(message)
                                input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Successfully Sent {message} To PG3D's Servers! Press enter to exit...", highlight=False)
                            else:
                                console.print(f"\n[red][!][/] You May Have Been IP Banned: Expected [underline bold]40/sio[/] At Step 4, Recieved: [underline bold]{r}[/]", highlight=False); console.print("\n")
                                c = str(input(f"{Fore.LIGHTCYAN_EX}[>]{Fore.RESET} Would You Like To Continue? (y/n): "))
                                if c == "y" or c == "Y" or c == "yes" or c == "Yes":
                                    console.print("[yellow][!][/] Ignoring IP Ban Warning...", highlight=False)
                                    await ws.send('452-/sio,[{"_placeholder":true, "num":0}, {"_placeholder":true, "num":1}]')
                                    console.print("[yellow1][!][/] Sent Sio Queue Placeholder Factor (5/5)", highlight=False)
                                    await ws.send(message)
                                    r = await ws.recv()
                                    console.print(f"[green][!][/] Recieved [underline bold]{r}[/] from websocket.", highlight=False)
                                    exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Successfully Sent {message} To PG3D's Servers! Press enter to exit...")
                                else:
                                    exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")
                        else:
                            console.print(f"[red][i][/] An Error Occured While Trying To Handle Sio Queue: Expected 40 At Step 2, Recieved: {r}", highlight=False)
                            exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")
                    else:
                        console.print(f"[red][i][/] An Error Occured While Trying To Handle Sio Queue: Expected Sid At Step 1, Recieved: {r}", highlight=False)
                        exit = input(f"{Fore.LIGHTGREEN_EX}[!]{Fore.RESET} Press enter to exit...")
            except Exception as e:
                console.print(f"[red][i][/] An Error Occured: {r}", highlight=False)
        message = str(input(f"{Fore.LIGHTCYAN_EX}[>]{Fore.RESET} Enter The Desired Message To Send To PG3D's Websocket: "))
        console.print(f"[green][!][/] Attempting To Establish A Websocket Connection With PG3D's Servers...", highlight=False)
        asyncio.run(connectAndSend(message))



    if choice == "11": # search weapon id
        tab_title = 'echo "\033]0;%s\007"' % f"Search Weapon ID"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Search Weapon IDs", justify="center")
        console.print("Enter [underline bold]0[/] to exit.", highlight=False, justify="center")
        r = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/weapons.json")
        data = r.json()
        while True:
            search_term = input(f"\n{Fore.LIGHTCYAN_EX}[>]{Fore.RESET} Enter the weapon name/gallery number to search for: ")
            if search_term == "0":
                break
            found_weapon = False
            for weapon in data:
                if search_term.lower() in weapon['weaponname'].lower() or search_term == weapon['gallery_number']:
                    console.print(f"\nWeapon Name: [underline bold]{weapon['weaponname']}[/]\nWeapon ID: [underline bold]{weapon['weapon_id']}[/]\nGallery Number: [underline bold]{weapon['gallery_number']}[/]", highlight=False)
                    found_weapon = True
            if not found_weapon:
                console.print("\n[red]!][/] No weapon found with the given search term.", highlight=False)



    if choice == "12": # search wear id
        tab_title = 'echo "\033]0;%s\007"' % f"Search Wear ID"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Search Wear IDs", justify="center")
        console.print("Enter [underline bold]0[/] to exit.", highlight=False, justify="center")
        r = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/wears.json")
        data = r.json()
        while True:
            search_term = input(f"\n{Fore.LIGHTCYAN_EX}[>]{Fore.RESET} Enter the wear name to search for: ")
            if search_term == "0":
                break
            found_wear = False
            for wear in data:
                if search_term.lower() in wear['wearname'].lower() or search_term == wear['wearid']:
                    console.print(f"\nWear Name: [underline bold]{wear['wearname']}[/]\nWear ID: [underline bold]{wear['wearid']}[/]\n", highlight=False)
                    found_wear = True
            if not found_wear:
                console.print("\n" + "[red]!][/] No wears found with the given search term.", highlight=False)


    if choice == "13": # search item record
        tab_title = 'echo "\033]0;%s\007"' % f"Search Item Record"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Search Item Record", justify="center")
        console.print("Enter [underline bold]0[/] to exit.", highlight=False, justify="center")
        r = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/itemrecord")
        data = r.json()
        while True:
            search_term = input(f"\n{Fore.LIGHTCYAN_EX}[>]{Fore.RESET} Enter the Item Record to search for: ")
            if search_term == "0":
                break
            found_record = False
            try:
                for record_key, record_value in data.items():
                    if search_term.lower() in record_value.lower() or search_term == record_key:
                        console.print(f"\nName: [underline bold]{record_value}[/]\nItem Record ID: [underline bold]{record_key}[/]\n")
                        found_record = True
                if not found_record:
                    print("\n" + f"[red]!][/] No Item Records were found with the given search term.{Fore.RESET}")
            except Exception as e:
                input(f"[red][!][/] An error occured when searching. Please report the bug on the GitHub. Press enter to exit.\nError: [underline]{e}[/]")

    if choice == "14": # search websocket command
        tab_title = 'echo "\033]0;%s\007"' % f"Search Websocket Commands"; os.system(tab_title); clear()
        console.print(banner, justify="center"); console.print("Search Websocket Commands", justify="center")
        console.print("Enter [underline bold]0[/] to exit.", highlight=False, justify="center")
        r = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/websocketcommand.json")
        data = r.json()
        while True:
            search_term = input(f"\n{Fore.LIGHTCYAN_EX}[>]{Fore.RESET} Enter the Websocket Command to search for: ")
            if search_term == "0":
                break
            found_cmd = False
            try:
                for record_value in data:
                    if search_term.lower() in record_value.lower():
                        console.print(f"\nCommand: [underline bold]{record_value}[/]\n")
                        found_cmd = True
                if not found_cmd:
                    console.print("\n" + f"[red][!][/] No Websocket Commands were found with the given search term.{Fore.RESET}")
            except Exception as e:
                input(f"[red][!][/] An error occured when searching. Please report the bug on the GitHub. Press enter to exit.\nError: [underline]{e}[/]")
            

    if choice == "r":
        os.system(f'py "{filename}"')
