import os
import json

def getPathPl():
	return "iosPhotoLab/Localization free/"

def getPathVs():
	return "iosPhotoLab/Resources-visagelab/Localization/"


def getContentForPath(path):
	link = os.getcwd() + "/" + path
	files = []

	with os.scandir(link) as list:
		for item in list:
			if item.path.split('.')[-1] == "lproj":
				files.append(item.path)
				
	return files

def verify(item, list):
	name = item.split('/')[-1]
	res = None

	for i in list:
		if name == i.split('/')[-1]:
			res = i
			break
	return res
			

def parse(link):
	items = {}
	path = link + "/Localizable.strings"
	with open(path, 'r') as fl:
		str = fl.read()
		lines = str.split('\n')
		for i in lines:
			if "=" not in i:
				continue
			parts = i.split('=')
			items[parts[0]] = parts[-1]
	return items

def getDiff(items1, items2):
	diffs = {}
	for k in items1.keys(): 
		if k not in items2:
			if "Photo Lab" in items1[k] and "//" not in k:
				print("Warning:"+k)
			else:
				diffs[k] = items1[k]
	return diffs

def serialize(diff):
	text = ""
	for k in diff.keys():
		line = k + " = " + diff[k]
		text += line
		text += '\n'
	return text

def processLinks(link1, link2):
	items1 = parse(link1)
	items2 = parse(link2)
	diffs  = getDiff(items1, items2)
	str = serialize(diffs)
	path = link2 + "/Localizable.strings"
	with open(path, 'a') as fw:
		fw.write(str)

plItems = getContentForPath(getPathPl())	
vsItems = getContentForPath(getPathVs())

for link1 in plItems:
	link2 = verify(link1, vsItems)
	if link2 != None:
		print("Verified:" + link1.split('/')[-1])
		processLinks(link1, link2)
	else:
		print("No compare:" + link1.split('/')[-1])

