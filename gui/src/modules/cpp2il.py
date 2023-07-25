import dearpygui.dearpygui as dpg
from tkinter import Tk
from tkinter.filedialog import askopenfile, askdirectory
import os

commands = []
apkname = ""
def modify_commands(cmdtype: bool, command: str):
    command = command.strip()
    if cmdtype:
        commands.append(command); print(commands)
        dpg.set_value("cmdslist", commands)
    else:
        commands.remove(command); print(commands)
        dpg.set_value("cmdslist", commands)

def addanalysislevel(level):
    for i, command in enumerate(commands):
        if command.startswith('--analysis-level='):
            commands[i] = f'--analysis-level="{level}"'; print(commands)
            dpg.set_value("cmdslist", commands)
            return
    commands.append(f'--analysis-level="{level}"'); print(commands)
    dpg.set_value("cmdslist", commands)

def list_to_args(lst: list):
    return " ".join(lst)

def addgamepath(path: str):
    apkpath = path.strip()
    dpg.set_value("cmdslist", commands)
    for i, command in enumerate(commands):
        if command.startswith('--game-path='):
            commands[i] = f'--game-path="{apkpath}"'; print(commands)
            dpg.set_value("cmdslist", commands)
            return
    commands.append(f'--game-path="{apkpath}"'); print(commands)
    dpg.set_value("cmdslist", commands)

def addoutputpath(path: str): # not used rn
    outputpath = path.strip()
    dpg.set_value("cmdslist", commands)
    for i, command in enumerate(commands):
        if command.startswith('--output-root='):
            commands[i] = f'--output-root="{outputpath}"'; print(commands)
            dpg.set_value("cmdslist", commands)
            return
    commands.append(f'--output-root="{outputpath}"'); print(commands)
    dpg.set_value("cmdslist", commands)


def selectapk():
    Tk().withdraw()
    try:
        file_path = askopenfile(filetypes=[("APK Files", "*.apk")])
        if file_path:
            apk_name = file_path.name.split("/")[-1] # get the name of the file
            global apkname
            apkname = apk_name
            print(f"Selected APK: {apk_name}")
            dpg.set_value("selectedapk", f"Selected APK: {apk_name}")
            addgamepath(file_path.name)
        print(f"File path: {file_path.name}")
    except AttributeError:
        print("[ERROR] No file selected")

def outputto():
    Tk().withdraw()
    folder_path = askdirectory()
    print(f"Selected Output Directory: {folder_path}")
    dpg.set_value("selectedoutput", f"Selected Output: {folder_path}")
    addoutputpath(folder_path)

def analysislevel():
    analysislevel = dpg.get_value("analysisleveltag")
    if analysislevel <= 0:
        analysislevel = 0
        dpg.set_value("analysisleveltag", analysislevel)
    elif analysislevel >= 4:
        analysislevel = 4
        dpg.set_value("analysisleveltag", analysislevel)
    print(f"Analysis Level: {analysislevel}")
    addanalysislevel(str(analysislevel))

def skipanalysis():
    isskipanalysis = dpg.get_value("skipanalysistag")
    print(f"Skip analysis: {isskipanalysis}")
    modify_commands(isskipanalysis, "--skip-analysis")

def skipmetadatatxts():
    isskipmetadatatxts = dpg.get_value("skipmetadatatxtstag")
    print(f"Skip Metadata txts: {isskipmetadatatxts}")
    modify_commands(isskipmetadatatxts, "--skip-metadata-txts")

def disableregprompts():
    isdisableregprompts = dpg.get_value("disableregpromptstag")
    print(f"Disable reg Prompts: {isdisableregprompts}")
    modify_commands(isdisableregprompts, "--disable-registration-prompts")

def verbose():
    isverbose = dpg.get_value("verbosetag")
    print(f"Verbose: {isverbose}")
    modify_commands(isverbose, "--verbose")

def iltoasm():
    isiltoasm = dpg.get_value("iltoasmtag")
    print(f"IL to Asm: {isiltoasm}")
    modify_commands(isiltoasm, "--experimental-enable-il-to-assembly-please")

def suppressattributes():
    issuppressattributestag = dpg.get_value("suppressattributestag")
    print(f"Suppress Attributes: {issuppressattributestag}")
    modify_commands(issuppressattributestag, "--suppress-attributes")

def runanalysisforasm():
    isrunanalysisforasmtag = dpg.get_value("runanalysisforasmtag")
    print(f"Run analysis for Assembly: {isrunanalysisforasmtag}")
    modify_commands(isrunanalysisforasmtag, "--run-analysis-for-assembly")

def throwsafetyoutofwindow():
    isthrowsafetyoutofwindow = dpg.get_value("throwsafetyoutofwindowtag")
    print(f"Throw Safety Out of Window: {isthrowsafetyoutofwindow}")
    modify_commands(isthrowsafetyoutofwindow, "--throw-safety-out-the-window")

def analyzeall():
    isanalyzeall = dpg.get_value("analyzealltag")
    print(f"Analyze All: {isanalyzeall}")
    modify_commands(isanalyzeall, "--analyze-all")

def skipmethoddumps():
    isskipmethoddumps = dpg.get_value("skipmethoddumpstag")
    print(f"Skip Method Dumps: {isskipmethoddumps}")
    modify_commands(isskipmethoddumps, "--skip-method-dumps")

def parallel():
    isparallel = dpg.get_value("paralleltag")
    print(f"Parallel: {isparallel}")
    modify_commands(isparallel, "--parallel")

def givemealldlls():
    isgivemealldlls = dpg.get_value("givemealldllstag")
    print(f"Just Give me All DLLs: {isgivemealldlls}")
    modify_commands(isgivemealldlls, "--just-give-me-dlls-asap-dammit")

def simpleattributeres():
    issimpleattributeres = dpg.get_value("simpleattributerestag")
    print(f"Simple Attribute Restoration: {issimpleattributeres}")
    modify_commands(issimpleattributeres, "--simple-attribute-restoration")



def startcpp2il():
    addoutputpath(f"cpp2il_out\{apkname}")
    arguments = list_to_args(commands)
    dpg.set_value("cpp2ilstatustxt", "Running Cpp2IL... See the console for what's happening")
    print(f"Expected Cpp2IL Path: Cpp2IL")
    print(F"Cpp2IL arguments: {arguments}\n\n")

    exitcode = os.system(f'modules\Cpp2IL\Cpp2IL.exe {arguments}')

    print(f"Finished running Cpp2IL... Exit Code: {exitcode}")
    if exitcode == -1: # cpp2il invalid arguments exit code
        dpg.set_value("cpp2ilstatustxt", "Error:   Invalid arguments given to Cpp2IL")
    elif exitcode == 1: # could not find file exit code
        dpg.set_value("cpp2ilstatustxt", "Error: System.IO.DirectoryNotFoundException: Could not find a part of a path")
    elif exitcode == -532462766:
        dpg.set_value("cpp2ilstatustxt", "Error:   Could not find Cpp2IL.exe!")
    else:
        dpg.set_value("cpp2ilstatustxt", "An unknown error occured.")

def cpp2ilgui():
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
        dpg.add_text("Status: idle", tag="statustxt")