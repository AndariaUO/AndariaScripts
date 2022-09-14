from Assistant import Engine
from ClassicAssist.UO.Objects.Gumps import *
from AndariaLib import *
from collections import OrderedDict
import operator

cds = {}

def Main():
    LoadCooldowns()
    while cds:
        gump = AFKGump()
        gump.SendGump()
        Pause(1000)
    if gump is not None:
        gump.CloseGump()

class AFKGump(Gump):            
    def __new__(self):            
        gump = Gump.__new__(self, 250, 250, 800190019)
        gump.Closable = True
        gump.Movable = True
        
        gump.AddPage(0)
        gump.AddImage(0, 0, 1416)
        gump.AddLabel(35, 5, 333, "Cooldowns")
        
        LoadCooldowns()
        i = 1
        zeros = []
        for cd in cds:
            time = cds[cd]
            gump.AddLabel(5, 5 + (i * 20), 150, "{0} - {1}s".format(cd,time))
            cds[cd] -= 1
            i += 1
            if cds[cd] < 0:
                zeros.append(cd)
        for cd in zeros:
            SysMessageBlue("Cooldown {0} vypršel!".format(cd))
            del cds[cd]

        return gump
        
def LoadCooldowns():
    global cds
    cooldowns = LoadMacroVariables("Cooldown", {}).copy()
    if cooldowns:
        cooldowns.update(cds)
        cds = OrderedDict(sorted(cooldowns.items(), key=operator.itemgetter(1)))
        DeleteMacroVariables("Cooldown")

Main()