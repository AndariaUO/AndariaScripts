# -*- coding: utf-8 -*-

from Assistant import Engine
from DorchLib import *
import re
import os
from datetime import datetime
import codecs
from collections import namedtuple

MOVECOUNTFILES = "Data\Plugins\ClassicAssist\Modules\move-count.txt"


def __canTake(item, allowedItems):
	for allowedItem in allowedItems:
		if isinstance(allowedItem, ItemTypeClass):
			if allowedItem.match(item):
				return True, allowedItem
		else:
			if allowedItem == item.ID:
				return True, allowedItem
	return False, None


def Uklid(Config, move=True, log=True):
	PromptAlias("bagToUklid")
	UseObject("bagToUklid")

	transferedItems = []
	now = datetime.now()
	for pathConfig in Config:
		macro = pathConfig["path"]["macro"]
		rail = pathConfig["path"]["rail"]

		if move:
			PathfindToRail(macro, rail, None)

		canBags = {}
		for bagName, positionItems in pathConfig["bags"].items():
			canM = False
			for bagToOpen in positionItems["bagToOpen"]:
				foundItems = Engine.Items.SelectEntities(
					lambda i: i.Serial == bagToOpen and i.Distance <= 2)
				if foundItems is not None:
					canM = True

			canBags[str(positionItems["bagId"])] = canM

		cont = Engine.Items.GetItem(GetAlias("bagToUklid"))
		if cont.Container == None:
			WaitForContents(GetAlias("bagToUklid"), 5000)

		for item in cont.Container.GetItems():
			for bagName, positionItems in pathConfig["bags"].items():
				if canBags[str(positionItems["bagId"])]:
					can, type = __canTake(item, positionItems["items"])
					if can:
						MoveItem(item.Serial, positionItems["bagId"], item.Count)
						Pause(700)
						transferedItems.append(item)

	if log:
		namesChange = [
			{"from": "Lektvary", "to": "Lektvar"},
			{"from": "Protijedy", "to": "Protijed"},
			{"from": "Jedy", "to": "Jed"},
			{"from": "Silne", "to": "Silny"},
			{"from": "Silné", "to": "Silny"},
			{"from": "Silný", "to": "Silny"},
			{"from": "Výbušné", "to": "Výbušný"},
			{"from": "Vybušné", "to": "Vybušný"},
			{"from": "Kosti", "to": "Kost"},
			{"from": "Krvavé", "to": "Krvavá"},
		]

		mergedItems = {}

		for transferedItem in transferedItems:
			itemName = transferedItem.Name
			for nameChange in namesChange:
				itemName = re.sub(r'(' + nameChange["from"] + ')', nameChange["to"], itemName)

			if itemName in mergedItems:
				mergedItems[itemName]["count"] += transferedItem.Count
			else:
				mergedItems[itemName] = {
					"item": transferedItem,
					"count": transferedItem.Count,
				}

		with codecs.open(MOVECOUNTFILES, "a", encoding='utf-8') as f:
			f.write("-----------------------------\n")
			f.write(now.strftime("%d.%m.%Y, %H:%M:%S") + " Začátek vykládání\n")

			for itemName, data in mergedItems.items():
				f.write(NormalizeString(itemName.strip()) + ": " + str(data["count"]) + "\n")

			now = datetime.now()
			f.write(now.strftime("%d.%m.%Y, %H:%M:%S") + " Konec vykládání\n")
			f.write("-----------------------------\n")



from UklidExampleConfig import UKLIDCONFIG

Uklid(UKLIDCONFIG)