import dearpygui.dearpygui as dpg
import os
import tkinter as tk
from tkinter import filedialog

commands = []

def list_to_args(lst: list):
    return " ".join(lst)

def selectexec(path: str):
    root = tk.Tk()
    root.withdraw()
    execpath = filedialog.askopenfilename(title="Select Executable")
    if not os.path.isfile(execpath):
        if os.path.isfile(execpath + ".so"):
            execpath += ".so"
        elif os.path.splitext(execpath)[1] == "":
            pass
        else:
            return
    dpg.set_value("cmdslist1", commands)
    commands.append(f'"{execpath}"'); print(commands)
    dpg.set_value("cmdslist1", commands)

def selectmetadata(path: str):
    metadatapath = path.strip()
    if not os.path.isfile(metadatapath):
        if os.path.splitext(metadatapath)[1] == ".dat":
            pass
        else:
            return
    dpg.set_value("cmdslist1", commands)
    commands.append(f'"{metadatapath}"'); print(commands)
    dpg.set_value("cmdslist1", commands)

def startil2cppdump():
    arguments = list_to_args(commands)
    dpg.set_value("il2cppstatustxt", "Running IL2Cpp Dumper... See the console for what's happening")
    print(f"Expected Cpp2IL Path: Cpp2IL")
    print(F"IL2Cpp Dumper arguments: {arguments}\n\n")

    exitcode = os.system(f'modules\Cpp2IL\Cpp2IL.exe {arguments}')

    print(f"Finished running IL2Cpp Dumper... Exit Code: {exitcode}")