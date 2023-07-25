import pkg_resources, math, os, json, asyncio, random

installed_packages = [i.key for i in pkg_resources.working_set]

try:
    import httpx
    import requests
    import pyperclip
    import urllib
    import threading
    from websockets import connection
    import websockets
    import dearpygui.dearpygui as dpg
    from capstone import *
    from keystone import *
    from modules.keystonecapstone import *
    from modules.cpp2il import *
    from modules.il2cpp import *
except ImportError:
    count = 0
    modules = ["httpx", "requests", "pyperclip", "websockets", "dearpygui", "keystone-engine", "capstone"]
    for _ in modules:
        count += 1
        print(f"[!] Installing {_} | {count} / {len(modules)}")
        os.system(f"pip install {_} -q")
        print(f"[!] Successfully installed {_}\n")

filepath = os.path.abspath(__file__)
filename = os.path.basename(__file__)
folderpath = os.getcwd()
operatingsys = os.name
VERSION_URL = "https://raw.githubusercontent.com/YeetDisDude/pg3d-tools/main/version.txt"
VERSION = "0.2.1"

def check_update():
    dpg.set_value(f"updatetxt", "Status: Checking for updates...")
    r = httpx.get(VERSION_URL)
    if r.text.strip() != VERSION:
        dpg.set_value("updatetxt", f"Status: Version {VERSION} is Outdated! Download the latest version from github.com/YeetDisDude/Arm-Converter")
    else:
        dpg.set_value(f"updatetxt", f"Status: Pixel Gun 3D Tools version {VERSION} is up to date!")

class Connection():

    def threadFunction():
        pass
    async def handleSioQueue(ws):
        r = await ws.recv()
        if r.startswith('0{"sid":'):
            rTrim = r[len("0"):len(r)]
            loadedTrim = json.loads(rTrim)
            sid = loadedTrim["sid"]
            print(f"Session ID: {sid}")
            r = await ws.recv()
            if r == "40":
                await ws.send("40/sio")
                r = await ws.recv()
                if r == "40/sio":
                    return True, "HANDLE_SQ"
                else:
                    return False, "IP_BAN"
            else:
                return False, "INVALID_RESPONSE"
        else:
            return False, "INVALID_SID"
    async def sendMessage(ws, message):
        await ws.send('452-/sio,[{"_placeholder":true, "num":0}, {"_placeholder":true, "num":1}]')
        await ws.send(message)
        return True, "SENT"
    async def startConnection(message):
        async with websockets.connect("wss://server-v2.pixelgunserver.com:443/socket.io/?EIO=4&transport=websocket&client_ver=v2") as ws:
            t = threading.Thread(target=Connection.threadFunction(), args=(ws))
            t.start()
            res, mess = await Connection.handleSioQueue(ws)
            if res and mess == "HANDLE_SQ":
                res, mess = await Connection.sendMessage(ws, message)
                if res and mess == "SENT":
                    return res, "Success: Sent"
            elif not res and mess == "IP_BAN":
                return False, "Status: IP Banned | Failed"
            elif not res and mess == "INVALID_RESPONSE":
                return False, "Status: Invalid Server Response | Failed"
            elif not res and mess == "INVALID_SID":
                return False, "Staus: Invalid SID Response | Failed"



def encodejsonurl(dict):
    return urllib.parse.quote(json.dumps([dict]))

def checkban(sender, data):
    usrid = dpg.get_value("usrid")
    dpg.set_value("status_text", f"Status: Sending Request to Pixel Gun 3D Servers...")
    response = httpx.post("https://secure.pixelgunserver.com/pixelgun3d-config/getBanList.php", data={'type_device': int(random.random() * 69), 'id': {usrid}}).text
    if response == "1":
        dpg.set_value("status_text", f"Status: User ID {usrid} is banned!")
    else:
        dpg.set_value("status_text", f"Status: User ID {usrid} is not banned.")

def downloaddumpcs(sender, data):
    version = dpg.get_value("dumpcsvercombo")
    if version == "Select Version":
        dpg.configure_item("statustxt2", label="Status: Please select a version")
        return
    r = requests.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/dumpcs.json")
    data = json.loads(r.text)
    key = version
    url = data["versions"][key]
    dpg.configure_item("statustxt2", label=f"Status: Downloading {version}'s Dump.cs...")    
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    os.makedirs("downloads", exist_ok=True)
    with open(f"downloads/{version}.cs", "wb") as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
                downloaded += len(chunk)
                progress = math.ceil(downloaded / file_size * 100)
                dpg.set_value("statustxt2", f"Status: Downloading {version}'s Dump.cs... ({progress}%)")
    dpg.configure_item("statustxt2", label=f"Status: Downloaded {version} to {os.getcwd()}/downloads/{version}.cs")

def downloadassembly(sender, data):
    version = dpg.get_value("assemblyvercombo")
    if version == "Select Version":
        dpg.configure_item("statustxt3", label="Status: Please select a version")
        return
    r = requests.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/dumpcs.json")
    data = json.loads(r.text)
    key = version
    url = data["versions"][key]
    dpg.configure_item("statustxt3", label=f"Status: Downloading {version}'s Assembly-CSharp.dll...")    
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    os.makedirs("downloads", exist_ok=True)
    with open(f"downloads/{version}.dll", "wb") as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
                downloaded += len(chunk)
                progress = math.ceil(downloaded / file_size * 100)
                dpg.set_value("statustxt3", f"Status: Downloading {version}'s Assembly-CSharp.dll... ({progress}%)")
    dpg.configure_item("statustxt3", label=f"Status: Downloaded {version} to {os.getcwd()}/downloads/{version}.cs")

def currencythreshold(sender, data):
    dpg.set_value("coins", f"Coins: sending request...")
    dpg.set_value("gems", f"Gems: sending request...")
    if data == "iOS":
        os = "ios"
    else:
        os = "android"
    r = httpx.get(f"https://secure.pixelgunserver.com/pixelgun3d-config/advert-v2/advert-{os}.json")
    j = r.json()
    dpg.set_value("coins", f"Coins: {j['cheater']['gemThreshold']}")
    dpg.set_value("gems", f"Gems: {j['cheater']['coinThreshold']}")

def updateplayerlogs(sender, data):
    usrid = dpg.get_value("userid")
    currency = dpg.get_value("currency")
    amount = dpg.get_value("amount")
    times = dpg.get_value("times")
    parameters = encodejsonurl({"cmid":3783,"eid":1012,"uid": str(usrid),"dev":1,"c":"NIG","p":1,"v":"69.0.0","r":1,"cid":"1","t":1,"reg":1,"pl":0,"ip1":amount,"sp1":currency,"sp2":"YeetDisDude","ip2":1})

    count = 0
    try:
        for _ in range(int(times)):
            count += 1
            r = requests.post("https://pixelgun-cl-stat.pixelgunserver.com/event_stat_add_pl.php", params=f'muid={str(id)}&events={parameters}')
            dpg.set_value("statustxt", f"Status: {count} / {times} | Status: {r.status_code} | Response: {r.text.strip()}")
    except requests.exceptions.RequestException:
        dpg.set_value("statustxt", "Status: Something went wrong when sending the request...")
    dpg.set_value("statustxt", "Status: Finished sending!")

def spamcontacts():
    name = dpg.get_value("name")
    message = dpg.get_value("message")
    numthreads = dpg.get_value("threads")
    email = dpg.get_value("email")
    def send_request(payload):
        with httpx.Client() as client:
            r = client.post("https://lightmap.com/contact_form", data=payload)
            dpg.set_value("statustxt6", f"Status: {r.status_code} | Response: {r.text}s")
    payload = {"name": name, "email": random.choice(email), "message": message }
    threads = []
    for i in range(int(numthreads)):
        t = threading.Thread(target=send_request, args=(payload,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    dpg.set_value("statustxt6", f"Status: Done.")

def makeusername():
    username = dpg.get_value("username")
    newusername = f"⁬{username}"
    dpg.set_value("usernameoutput", newusername)
    dpg.set_value("statustxt7", "Status: Complete, copied to clipboard (invis char added)")
    pyperclip.copy(newusername)

def skinplist():
    skinbase64 = dpg.get_value("skinb64")
    skinname = dpg.get_value("skinname")
    print(skinbase64, skinname)
    dpg.set_value("statustxt8", "Status: Saved to generated/dict.txt")
    directory = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(directory, "generated")
    if not os.path.exists(folder):
        os.makedirs(folder)
    file = os.path.join(directory, "generated\dict.txt")
    with open(file, "w") as f:
        content = f'''
User Skins:
    <key>User Skins</key>
    <string>{{'1001': {skinbase64}}}</string>
Plist for Skin Names:
    <key>User Name Skins</key>
    <string>{{'1001': {skinname}}}</string>
Current Equiped Skin:
    <key>Name Current Skin</key>
    <string>1001</string>
\nUsage: Replace the lines in the plist with the lines generated PG3D Tools\nhttps://github.com/YeetDisDude/\nMade by: YeetDisDude'''
        content = content.replace("'", '"')
        f.write(content)

def wsMain():
    msg = str(dpg.get_value("msg"))
    res, mes = asyncio.run(Connection.startConnection(msg))
    dpg.set_value("ws_status", mes)

def searchwep(sender, data):
    searchterm = dpg.get_value("wepsearchterm")
    r = requests.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/weapons.json")
    data = r.json()
    weapon_results = []
    for weapon in data:
        if searchterm.lower() in weapon['weaponname'].lower() or searchterm == weapon['gallery_number']:
            weapon_result = f"""
Weapon Name: {weapon['weaponname']}
Weapon ID: {weapon['weapon_id']}
Gallery Number: {weapon['gallery_number']}"""
            weapon_results.append(weapon_result)
    if not weapon_results:
        weapon_results.append(f"'{searchterm}' not found")
    dpg.set_value("weaponidresult", "\n".join(weapon_results))

def searchwear(sender, data):
    searchterm = dpg.get_value("wearsearchterm")
    r = requests.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/wears.json")
    data = r.json()
    wear_results = []
    for wear in data:
        if searchterm.lower() in wear['wearname'].lower() or searchterm == wear['wearid']:
            weapon_result = f"""
Wear Name: {wear['wearname']}
Wear ID: {wear['wearid']}"""
            wear_results.append(weapon_result)
    if not wear_results:
        wear_results.append(f"'{searchterm}' not found")
    dpg.set_value("wearidresult", "\n".join(wear_results))

def searchitemrecord(sender, data):
    searchterm = dpg.get_value("itemrecordsearchterm")
    r = requests.get("https://raw.githubusercontent.com/TonicBoomerKewl/pixel-gun-3d-console-client/main/PG3D-ItemRecords.json")
    data = r.json()
    item_results = []
    for record_key, record_value in data.items():
        if searchterm.lower() in record_value.lower() or searchterm == record_key:
            item_result = f"""
Item ID: {record_key}
Item Name: {record_value}"""
            item_results.append(item_result)
    if not item_results:
        item_results.append(f"'{searchterm}' not found")
    dpg.set_value("itemrecordresult", "\n".join(item_results))

def searchwscmd(sender, data):
    searchterm = dpg.get_value("wscmdsearchterm")
    r = requests.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/websocketcommand.json")
    data = r.json()
    cmdresults = []
    for record_value in data:
        if searchterm.lower() in record_value.lower():
            item_result = f"""
Command: {record_value}"""
            cmdresults.append(item_result)
    if not cmdresults:
        cmdresults.append(f"'{searchterm}' not found")
    dpg.set_value("wscmdresult", "\n".join(cmdresults))

def getallscenes():
    r = httpx.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/scenes.json")
    data = r.json()
    scenes = []
    for scene in data:
        for key, value in scene.items():
            scenes.append(value)
    dpg.set_value("allscenes", "\n".join(scenes))



def colorpicker(sender, data):
    color = dpg.get_value(sender)
    print(color)

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("Assets/SF-Pro-Display-Semibold.ttf", 20)

def tab1(): # tools

    dpg.bind_font(default_font)

    with dpg.group():

        with dpg.collapsing_header(label="Download Dump.cs files"): # 2
            r = requests.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/dumpcs.json")
            data = json.loads(r.text)
            vers = list(data["versions"].keys())
            dpg.add_combo(items=vers, default_value="Select Version", label="Version", tag="dumpcsvercombo", width=150)
            dpg.add_button(label="Download", callback=downloaddumpcs)
            dpg.add_text("Status: ", tag="statustxt2")

        with dpg.collapsing_header(label="Download Assembly-CSharp.dll files"): # 3
            r = requests.get("https://raw.githubusercontent.com/YeetDisDude/pixel-gun-3d/main/json/assembly-csharp.json")
            data = json.loads(r.text)
            vers = list(data["versions"].keys())
            dpg.add_combo(items=vers, default_value="Select Version", label="Version", tag="assemblyvercombo", width=150)
            dpg.add_button(label="Download", callback=downloadassembly)
            dpg.add_text("Status: ", tag="statustxt3")

        with dpg.collapsing_header(label="Make Unsearchable User Name"): #7
            dpg.add_input_text(width=150, label="Username", hint="Enter a Name", tag="username")
            dpg.add_text(" ")
            dpg.add_input_text(width=150, label="Output", readonly=True, tag="usernameoutput")
            dpg.add_button(label="Make Username", callback=makeusername)
            dpg.add_text("Status: ", tag="statustxt7")

        with dpg.collapsing_header(label="iOS Skin Plist Generator"): # 8
            dpg.add_text("You can only use this once")
            items = ["YeetDisDude", "yeetdisdude", "ig: y_etd.sdude", "YeetDisDude#0001", "Subscribe", ".gg/wnr9ME7enQ", "byeguys gaming", "higuys gaming", "okand"]
            dpg.add_input_text(width=150, label="Base64", hint="Enter Base64", tag="skinb64")
            dpg.add_combo(label="Skin Name", default_value="Select A Skin Name", items=items, tag="skinname")
            dpg.add_button(label="Add", callback=skinplist)
            dpg.add_text("Status: idle", tag="statustxt8")
        
        with dpg.collapsing_header(label="Get All Scene Names"): #9
            dpg.add_button(label="Get list", callback=getallscenes)
            dpg.add_input_text(multiline=True, width=550, height=250, readonly=True, label="Scenes", tag="allscenes")

def tab2(): # api
    with dpg.group():
        with dpg.collapsing_header(label="Spam Lightmap Contacts"): # 6
            emails = ["mrbaest@gmail.com", "admin@fbi.gov", "niggerlover69@gmail.com", "admin@niggerprevention.org", "hermesis@nigga.gov", "higuys@yahoo.com", "byeguyshangout@nigga.gov", "blacklivesdontmatter@fbi.gov", "fuck@fuck.com", "abc@defg.hijk", "abc@cba.abc", "natehiggers@google.com", "admin@pixelgunserver.com", "fuckniggers@discord.com", "tonicboomerkewl@github.com", "fuckpg3d@pixelgun3d.com"]
            dpg.add_input_text(hint="Enter Name", label="Name", tag="name", width=150)
            dpg.add_input_text(hint="Enter Message", label="Message", tag="message", width=150, hexadecimal=True)
            dpg.add_combo(items=emails, default_value="Select an Email", tag="email", label="Email")
            dpg.add_input_text(hint="Enter threads", default_value="150", label="Threads", tag="threads", width=150, scientific=True)
            dpg.add_button(label="Spam", callback=spamcontacts)
            dpg.add_text("Status: Idle", tag="statustxt6")

        with dpg.collapsing_header(label="Update Player Logs"): # 5
            items = ["Coins", "GemsCurrency", "BattlePassCurrency", "CraftCurrency", "ClanCurrency", "EventCurrency", "Coupons", "ClanSilver", "ClanLootBoxPoints", "Real", "Exp", "TankKeys", "RealCoins", "RealGems", "EventChestsSuperSpin", "PixelPassExp", "PixelPassCurrency", "clan_building_black_market_point", "SmallChest", "BigChest", "EventChest", "MegaChest", "MainModeSlotTokens", "PixelBucks"]
            dpg.add_input_text(width=150, hint="Enter User ID", tag="userid", label="ID", scientific=True)
            dpg.add_combo(items=items, default_value="Select Currency", tag="currency", label="Currency")
            dpg.add_input_text(width=150, hint="Enter Amount", tag="amount", label="Amount", scientific=True)
            dpg.add_input_text(width=150, hint="Times to send", tag="times", label="Times", scientific=True)
            dpg.add_button(label="Update", callback=updateplayerlogs)
            dpg.add_text("Status: Idle", tag="statustxt")

        with dpg.collapsing_header(label="Check Ban"): # 1
            dpg.add_input_text(decimal=True, hint="User ID", width=150, tag="usrid", label="ID")
            dpg.add_button(label="Check", callback=checkban)
            dpg.add_text("Status: ", tag="status_text")

        with dpg.collapsing_header(label="Get Currency Threshold"): # 4
            dpg.add_text("Select an OS")
            dpg.add_combo(items=["iOS", "Android"], default_value="os", tag="os",callback=currencythreshold)
            dpg.add_text("Coins: ", tag="coins")
            dpg.add_text("Gems: ", tag="gems")

def tab3(): # websocket
    with dpg.group():
        with dpg.collapsing_header(label="Send Websocket A Message"):  # 10
            dpg.add_text("Warning: You will get IP Banned for 24h if you send unencrypted messages!")
            dpg.add_input_text(decimal=False, hint="Desired Message", width=300, tag="msg", label="Message")
            dpg.add_button(label="Connect & Send", callback=wsMain)
            dpg.add_text("Status: Idle (Waiting For Action)", tag="ws_status")
        with dpg.collapsing_header(label="Get websocket key & IV"):
            dpg.add_text("Coming soon")
        with dpg.collapsing_header(label="Encrypt Message"):
            dpg.add_text("Coming soon")
        with dpg.collapsing_header(label="Decrypt Message"):
            dpg.add_text("Coming soon")


def tab4(): # search
    with dpg.group():
        with dpg.collapsing_header(label="Find Weapon ID"): # 11
            dpg.add_input_text(label="Search Term", hint="weapon name, gallery num etc", width=250, tag="wepsearchterm")
            dpg.add_button(label="Search", callback=searchwep)
            dpg.add_input_text(multiline=True, width=550, height=250, readonly=True, label="Result", tag="weaponidresult")
        
        with dpg.collapsing_header(label="Find Wear ID"):
            dpg.add_input_text(label="Search Term", hint="wear name", width=250, tag="wearsearchterm")
            dpg.add_button(label="Search", callback=searchwear)
            dpg.add_input_text(multiline=True, width=550, height=250, readonly=True, label="Result", tag="wearidresult")
        
        with dpg.collapsing_header(label="Find Item Record"):
            dpg.add_input_text(label="Search Term", hint="item record", width=250, tag="itemrecordsearchterm")
            dpg.add_button(label="Search", callback=searchitemrecord)
            dpg.add_input_text(multiline=True, width=550, height=250, readonly=True, label="Result", tag="itemrecordresult")
        
        with dpg.collapsing_header(label="Search Websocket Commands"):
            dpg.add_input_text(label="Search Term", hint="websocket command", width=250, tag="wscmdsearchterm")
            dpg.add_button(label="Search", callback=searchwscmd)
            dpg.add_input_text(multiline=True, width=550, height=250, readonly=True, label="Result", tag="wscmdresult")

        dpg.add_text(" ")

def tab5(): # modding
    with dpg.group():
        with dpg.collapsing_header(label="IL2CPP"):
            dpg.add_text(" ")
            dpg.add_button(label="Select an executable", callback=1, width=170, height=30)
            dpg.add_text("Selected file: ", tag="selectedexecutable")
            dpg.add_separator()
            dpg.add_button(label="Select a metadata", callback=1, width=170, height=30)
            dpg.add_text("Selected file: ", tag="selectedmetadata")
            dpg.add_separator()
            dpg.add_button(label="Output Path:", callback=1, width=170, height=30)
            dpg.add_text("Selected output folder: ", tag="selectedoutput")
            dpg.add_button(label="Start", width=150, height=50, callback=1)
            dpg.add_text(" ")
            


        with dpg.collapsing_header(label="CPP2IL"):
            dpg.add_text(" ")
            dpg.add_button(label="Select a file", callback=selectapk, width=150, height=25)
            dpg.add_text("Selected file: ", tag="selectedapk")
            dpg.add_text(" ")

            dpg.add_separator()

            dpg.add_slider_int(label="  Analysis Level                     ", width=150, min_value=0, max_value=4, callback=analysislevel, tag="analysisleveltag", default_value=-1) # --analysis-level
            dpg.add_checkbox(label="  Skip  Analysis                       ", tag="skipanalysistag", callback=skipanalysis) # --skip-analysis
            dpg.add_checkbox(label="  Skip  Metadata  Texts                ", tag="skipmetadatatxtstag", callback=skipmetadatatxts) # --skip-metadata-txts
            dpg.add_checkbox(label="  Disable  Registration  Prompts       ", tag="disableregpromptstag", callback=disableregprompts) # --disable-registration-prompts
            dpg.add_checkbox(label="  Verbose [Recommended]                ", tag="verbosetag", callback=verbose) # --verbose
            dpg.add_checkbox(label="  IL  to  Assembly  ( Experimental )   ", tag="iltoasmtag", callback=iltoasm) # --experimental-enable-il-to-assembly-please
            dpg.add_checkbox(label="  Suppress  Attributes                 ", tag="suppressattributestag", callback=suppressattributes) # --suppress-attributes
            dpg.add_checkbox(label="  Run  Analysis  for  Assembly         ", tag="runanalysisforasmtag", callback=runanalysisforasm) # --run-analysis-for-assembly
            dpg.add_checkbox(label="  Throw  Safety  Out  of  Window       ", tag="throwsafetyoutofwindowtag", callback=throwsafetyoutofwindow) # --throw-safety-out-the-window	
            dpg.add_checkbox(label="  Analyze  All                         ", tag="analyzealltag", callback=analyzeall) # --analyze-all	
            dpg.add_checkbox(label="  Skip  Method  Dumps                  ", tag="skipmethoddumpstag", callback=skipmethoddumps) # --skip-method-dumps
            dpg.add_checkbox(label="  Parallel                             ", tag="paralleltag", callback=parallel) # --parallel	
            dpg.add_checkbox(label="  Just  Give  me  DLLs  Asap           ", tag="givemealldllstag", callback=givemealldlls) # --just-give-me-dlls-asap-dammit
            dpg.add_checkbox(label="  Simple  Attribute  Restoration       ", tag="simpleattributerestag", callback=simpleattributeres) # --simple-attribute-restoration
            dpg.add_input_text(label="Commands", readonly=True, tag="cmdslist")
            dpg.add_text(" ")
            dpg.add_button(label="Start", callback=startcpp2il, width=150, height=50)
            dpg.add_text("Status: idle", tag="cpp2ilstatustxt")

        with dpg.collapsing_header(label="Arm to Hex"):
            dpg.add_text(" ")
            dpg.add_input_text(multiline=True, width=350, height=100, tag="armtohexinput", callback=ArmToHex, label="Assembly")
            dpg.add_text(" "); dpg.add_separator(); dpg.add_text(" ")
            dpg.add_input_text(label="Arm64", multiline=True, width=350, height=100, readonly=True, tag="armtohexarm64")
            dpg.add_text(" "); dpg.add_separator(); dpg.add_text(" ")
            dpg.add_input_text(label="Armv7", multiline=True, width=350, height=100, readonly=True, tag="armtohexarmv7")
            dpg.add_text(" ")
        with dpg.collapsing_header(label="Hex to Arm"):
            dpg.add_text(" ")
            dpg.add_input_text(multiline=True, width=350, height=100, tag="hextoarminput", callback=HexToArm, uppercase=True, label="Hex")
            dpg.add_text(" "); dpg.add_separator(); dpg.add_text(" ")
            dpg.add_input_text(label="Arm64", multiline=True, width=350, height=100, readonly=True, tag="hextoarm64")
            dpg.add_text(" "); dpg.add_separator(); dpg.add_text(" ")
            dpg.add_input_text(label="Armv7", multiline=True, width=350, height=100, readonly=True, tag="hextoarmv7")
            dpg.add_text(" ")

def tabcredits(): # credits
    with dpg.group():
        dpg.add_text("Credits")
        dpg.add_text(" ")
        dpg.add_text("YeetDisDude#0001 - Creating The Script | github.com/YeetDisDude")
        dpg.add_text("Pulsed#1874 - Contributing (Websocket Message Sender) | github.com/ChrxnZ")
        dpg.add_text("TonicBoomerKewl - Item Record and Websocket Command JSON | github.com/TonicBoomerKewl")

def tabsettings(): #settings
    with dpg.group():
        dpg.add_text("Select a theme color (coming soon)")
        dpg.add_color_picker("Color Picker", width=200, display_hex=True, no_alpha=True, no_side_preview=True, callback=colorpicker)
        dpg.add_text(" ")
        dpg.add_button(label="Check Update", callback=check_update, width=150, height=35)
        dpg.add_text("Status: idle", tag="updatetxt")


imguiW = 800
imguiH = 500
async def MAIN():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    dpg.set_viewport_width(imguiW + 16)
    dpg.set_viewport_height(imguiH + 38)
    dpg.set_viewport_title("Pixel Gun 3D Tools")
    dpg.set_viewport_large_icon("Assets/Icon.ico")
    dpg.set_viewport_small_icon("Assets/Icon/ico")
    dpg.set_viewport_resizable(False)
    

    with dpg.window(width=imguiW, height=imguiH, label=f"Pixel Gun 3D Tools | version {VERSION}", no_close=True, no_move=True, no_collapse=True, no_resize=True) as window:
        with dpg.tab_bar():
            with dpg.tab(label="Tools"):
                tab1()
            with dpg.tab(label="API"):
                tab2()
            with dpg.tab(label="WebSocket"):
                tab3()
            with dpg.tab(label="Search"):
                tab4()
            with dpg.tab(label="Modding"):
                tab5()
            with dpg.tab(label="Credits"):
                tabcredits()
            with dpg.tab(label="Settings"):
                tabsettings()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

asyncio.run(MAIN())
