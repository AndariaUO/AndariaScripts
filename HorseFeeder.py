from Assistant import Engine
from DorchLib import *

pause = 500

def Main():
	Init()
	while FindHorse():
		FeedHorse()
		Pause(pause)
		WaterHorse()
		Pause(pause)
	SysMessage("Hotovo")
	
def Init():
	Makelist("horses")
	Makelist("watersources")
	ClearIgnoreList()
	if FindType(VratTyp("pripousteci_hul"),-1,"self"):
		EquipType(VratTyp("pripousteci_hul"), "TwoHanded")
	else:
		if not ConfirmPrompt("Nemám připouštěcí hůl, chceš pokračovat?"):
			Stop()
	
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
		if not FindType(VratTyp("seno"), -1, "self"):
			if not FindType(VratTyp("seno"), 3):
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
		WaitForGump(0x0000042e, 1000)
		if GumpExists(0x0000042e):
			ReplyGump(0x0000042e, 1)
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