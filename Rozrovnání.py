from Assistant import Engine
from AndariaLib import *

### Nastav True pokud chceš znovu dotázat ignorované předměty
promptIgnored = False
### Prefix používaný skriptem, defaultně je Name("self") = jméno postavy
###   U postav s diakritikou doporučuji používat prefix ručně bez diakritiky, bohužel CA občas nechápe co to je.:
prefix = Name("self")  # Např místo "Štěpán" dát natvrdo string "Stepan"


macroName = "Rozrovnání"
prompt = "kontejner"

def Main():
    CheckVersion()
    Init()

def Init():
    global memory
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
        
    ProcessBag()
    
    SaveMacroVariable(macroName, memName, memory)
    SysMessageGreen("Hotovo")

def ProcessBag():
    global memory
    cont = Engine.Items.GetItem(GetAlias("kontejner"))
    counts = {}
    if cont.Container == None:
        WaitForContents(GetAlias("kontejner"), 5000)

    for item in cont.Container.GetItems():
        itemkey = GetTypeName(item)
        if itemkey is None:
            itemkey = Deaccent(Name(item))
        if itemkey not in memory.keys() or (promptIgnored and memory[itemkey] == 0):
            ConfirmPrompt("Předmět '" + Name(item) + "' zatím nemám v paměti. Připrav kontejner do kterého ho chceš ukládat a klikni OK, pak ho vyber.")
            value = PromptAlias(prompt)
            memory[itemkey] = value
            UnsetAlias(prompt)
        
        Move(item, itemkey, memory[itemkey])

def Move(item, itemkey, tarCont):
    if tarCont != 0:
        MoveItem(item, tarCont)
        Pause(500)
        if InJournal("Je to moc tìké, ani s tím nehne."):
            graphic = Graphic(item)
            hue = Hue(item)
            while PresunItem(graphic, GetAlias("kontejner"), tarCont, 100, hue):
                Pause(500)

Main()