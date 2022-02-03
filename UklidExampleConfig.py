# -*- coding: utf-8 -*-

from DorchLib import *

closetScrollsSecond = 0x40006cae
bagWands = 0x40040c85
wands = {"bagId": bagWands, "bagToOpen": [closetScrollsSecond, 0x400ef751],
		 "items": MultiTypes["hulky"]}

closetPotionSecond = 0x40006cfd
bagPotion = 0x40040c85
lektvary = {"bagId": bagPotion, "bagToOpen": [closetPotionSecond, 0x400ef144],
		 "items": MultiTypes["lektvary"]}

UKLIDCONFIG = [
	{
		"path": {
            "macro": "Uklid Postava",
            "rail": "DoHulekBedny",
        },
		"bags": {
			"wands": wands,
		}
	},
	{
		"path": {
            "macro": "Uklid",
            "rail": "DoAlchymisticke",
        },
		"bags": {
			"lektvary": lektvary,
		}
	}
]
