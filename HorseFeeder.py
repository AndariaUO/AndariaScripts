from Assistant import Engine
from DorchLib import *

pause = 500
gumpID = 0x000003ff # Toto se občas mění z nějakého důvodu, je třeba potom otevřít gump připouštěcí hole, potom otevřít brouka vpravo nahoře v CA a z Gumpů zkopírovat Serial

def Main():
	Init()
	while FindHorse():
		FeedHorse()
		Pause(pause)
		WaterHorse()
		Pause(pause)
	SysMessage("Hotovo")
	
def Init():
	ClearIgnoreList()
	if FindTypeBy("pripousteci_hul", -1, "self"):
		EquipType(GetType("pripousteci_hul"), "TwoHanded")
	else:
		if not ConfirmPrompt("Nemám připouštěcí hůl, chceš pokračovat?"):
			Stop()
	UnsetAlias("found")
	
def FindHorse():
	if FindTypeList("horses", 3):
		SetAlias("horse", "found")
		IgnoreObject("horse")
		HeadMsg("Teď já!", "horse")
		return True
			
	return False
	
def FeedHorse():
	while True:
		ClearJournal()
		if not FindTypeBy("seno", -1, "self"):
			if not FindTypeBy("seno", 3):
				SysMessage("Nemám seno")
				return
		MoveItem("found", "horse", 1)
		WhisperMsg("all stop")
		Pause(pause)
		if InJournal("Asi se to tvému miláèkovi pøíli nelíbí...") or InJournal("To není tvé zvíøe!"):
			return


def WaterHorse():
	while True:
		ClearJournal()
		Msg(".usehand")
		WaitForTarget(1000)
		Target("horse")
		WaitForGump(gumpID, 3000)
		if GumpExists(gumpID):
			ReplyGump(gumpID, 1)
		if not FindTypeList("watersources", -1, "self"):
			if not FindTypeList("watersources", 2):
				SysMessage("Nemám žádný zdroj vody")
				break
		Target("found")
		Pause(pause)
		if InJournal("nenapije") or InJournal("daleko"):
			IgnoreObject("found")
			HeadMsg("Jsem prázdný nebo moc daleko", "found")
		else:
			break

Main()