# -*- coding: utf-8 -*-

# Name: SpojLektvary
# Description: Spoj všechny lektvary pomocí nádoby do největšího počtu. Například lektvary z dungu když je chceš spojit. Uprav si proměnnou tempBag (dočasný pytlíček potřebný pro odkládání)
# Author: Draff
# Era: Any

from DorchLib import *

tempBag = 0x4000712f

UseObject(tempBag)
fr = PromptAlias("from")
what = PromptAlias("what")
whatItem = Engine.Items.GetItem(what)
fromItem = Engine.Items.GetItem(fr)
potionVesel = FindTypeBy("nadobaLektvar", "backpack")

whatType = None
for name, item in Types.items():
	if item.match(whatItem):
		whatType = item
		break

if whatType is not None and potionVesel is not None:
	while True:
		MoveItemCount(whatType, fromItem, "backpack", 100)

		Pause(500)
		itemsToUse = FindTypeBy(whatType, container="backpack")
		if itemsToUse is not None:
			PotionVesselJoinTheMost(potionVesel.Serial, itemsToUse)
			Pause(500)
			PotionVesselJoinTheMost(potionVesel.Serial, FindTypeBy("lahvicky", "backpack"))

			MoveItemCount(whatType, "backpack", tempBag, 100)
		else:
			break

		Pause(1000)

	items = FindTypeBy(whatType, container=tempBag, returnAllItems=True)
	if items is not None:
		for item in items:
			MoveItem(item.Serial, fromItem.Serial)
			Pause(500)

	print("Všechno přerovnáno")