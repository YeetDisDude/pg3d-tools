from capstone import *
from keystone import *
import dearpygui.dearpygui as dpg
def armtohex64error(e):
        if e.errno == KS_ERR_ASM_MNEMONICFAIL:
            arm64hex = "Invalid Mnemonic"
            dpg.set_value("armtohexarm64", arm64hex)
        elif e.errno == KS_ERR_ASM_INVALIDOPERAND:
            arm64hex = "Invalid Operand"
            dpg.set_value("armtohexarm64", arm64hex)
        else:
            arm64hex = "Assembly Error"
            dpg.set_value("armtohexarm64", arm64hex)

def armtohex7error(e):
        if e.errno == KS_ERR_ASM_MNEMONICFAIL:
            armv7hex = "Invalid Mnemonic"
            dpg.set_value("armtohexarmv7", armv7hex)
        elif e.errno == KS_ERR_ASM_INVALIDOPERAND:
            armv7hex = "Invalid Operand"
            dpg.set_value("armtohexarmv7", armv7hex)
        else:
            armv7hex = "Assembly Error"
            dpg.set_value("armtohexarmv7", armv7hex)

def ArmToHex(sender, data):
    print(data)
    ksarm64 = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
    ksarmv7 = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    try:
        bytecode_arm64, _ = ksarm64.asm(data)
        arm64hex = ' '.join('{:02x}'.format(x) for x in bytecode_arm64)
        arm64hex = arm64hex.upper()
        dpg.set_value("armtohexarm64", arm64hex)
    except KsError as e:
        armtohex64error(e=e)

    try:
        bytecode_v7, _ = ksarmv7.asm(data)
        armv7hex = ' '.join('{:02x}'.format(x) for x in bytecode_v7)
        armv7hex = armv7hex.upper()
        dpg.set_value("armtohexarmv7", armv7hex)
    except KsError as e:
        armtohex7error(e=e)

def HexToArm(sender, data):
    data = data.upper()
    print(data)
    csarm64 = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    csarmv7 = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    try:
        for insn in csarm64.disasm(bytes.fromhex(data), 0):
            dpg.set_value("hextoarm64", f"{insn.mnemonic} {insn.op_str}")
        for insn in csarmv7.disasm(bytes.fromhex(data), 0):
            dpg.set_value("hextoarmv7", f"{insn.mnemonic} {insn.op_str}")
    except ValueError as e:
        dpg.set_value("hextoarmv7", "Invalid Hex")
        dpg.set_value("hextoarm64", "Invalid Hex")