from Assistant import Engine
from AndariaLib import *

### Nastav True pokud chceš znovu dotázat ignorované předměty
promptIgnored = False
### Prefix používaný skriptem, defaultně je Name("self") = jméno postavy
###   U postav s diakritikou doporučuji používat prefix bez, bohužel CA občas nechápe co to je.:
prefix = Name("self")


macroName = "Rozrovnání"
prompt = "kontejner"

def Main():
    CheckVersion()
    Init()

def Init():
    global memory
    global prefix
    ClearIgnoreList()
    
    LoadAlias("kontejner")
    contName = Name("kontejner")
    
    if contName in ["pytel", "batoh", "mesec", "drevena truhlicka"]:
        SysMessageYellow("")
        res, name = MessagePrompt("Název kontejneru je příliš obecný.\nSkript ukládá nastavení podle názvu kontejneru a pokud chceš mít uloženo více nastavení, zadej unikátní klíčové slovo nebo rovnou kontejner přejmenuj.", contName)
        if res:
            contName = name
        else:
            return
    # Odstranění názvu cechu, pokud je obsažen v názvu
    if '[' in prefix:
        prefix = prefix.split('[')[0].strip()
    memNameAcc = prefix + "_" + contName
    memName = Deaccent(memNameAcc)
    memory = LoadMacroVariable(macroName, memName, {})
    if memory == {}:
        SysMessageYellow("Kontejner '" + memName + "' ještě neznám. Zakládám novou paměť.")
        
    ProcessBag(GetAlias("kontejner"))
    
    SaveMacroVariable(macroName, memName, memory)
    SysMessageGreen("Hotovo")

def ProcessBag(cont):
    global memory
    cont = Engine.Items.GetItem(cont)
    counts = {}
    if cont.Container == None:
        WaitForContents(cont, 2000)
        
    if cont.Container == None:
        return

    for item in cont.Container.GetItems():
        if Graphic(item.Serial) in [0x9b0, 0xe76, 0xe75, 0x9aa]:
            ProcessBag(item.Serial)
            continue
        
        WaitForProperties(item.Serial, 5000)
        itemkey = GetTypeName(item)
        if itemkey is None:
            itemkey = Deaccent(Name(item))
        if itemkey not in memory.keys() or (promptIgnored and memory[itemkey] == 0):
            if ConfirmPrompt("Patří předmět '" + Name(item) + "' do kontejneru " + Name(cont) + " ?"):
                memory[itemkey] = cont.Serial

Main()