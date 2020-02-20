import os
import json

def getPathPl():
	return "iosPhotoLab/Localization free/"

def getPathVs():
	return "iosPhotoLab/Resources-visagepro/Localization/"


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
			
def parseLine(line):
	if "=" not in line:
		return None
	parts = line.split('=')
	key = parts[0]
	if "//" in key:
		return None
	val = parts[-1]
	return [key, val]

def parse(link):
	items = {}
	path = link + "/Localizable.strings"
	with open(path, 'r') as fl:
		str = fl.read()
		lines = str.split('\n')
		for i in lines:
			tup = parseLine(i)
			if tup == None:
				continue
			items[tup[0]] = tup[1]
	return items

def getDiff(items1, items2):
	diffs = {}
	for k in items1.keys(): 
		if k not in items2:
			if "Photo Lab" in items1[k] and "//" not in k:
				print(k)
			else:
				diffs[k] = items1[k]
	return diffs

def getLines(link):
	path = link + "/Localizable.strings"
	lines = []
	with open(path, 'r') as fl:
		str = fl.read()
		lines = str.split('\n')
	return lines

def saveLines(lines, link):
	str = ""
	for line in lines:
		str += line+"\n"
	path = link + "/Localizable.strings"
	with open(path,"w") as fl:
		fl.write(str)

def removeLineForKey(key, lines):
	for i in lines:
		tup = parseLine(i)
		if tup == None:
			continue
		if tup[0] == key:
			lines.remove(i)
			break

def updateLines(link1, link2):
	lines = getLines(link1)
	vsLines = getLines(link2)
	keys = parse(link2)
	out = []
	for line in lines:
		tup = parseLine(line)
		if tup == None:
			out.append(line)
			if line in vsLines:
				vsLines.remove(line)
			continue
		if tup[0] in keys.keys():
			str = tup[0]+"="+keys[tup[0]]
			removeLineForKey(tup[0], vsLines)
			out.append(str)
		else:
			out.append(line)
			if "Photo Lab" in line:
				print(line)
	out.extend(vsLines)
	saveLines(out, link2)

def serialize(diff):
	text = ""
	for k in diff.keys():
		line = k + "=" + diff[k]
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
		updateLines(link1, link2)
	else:
		print("No compare:" + link1.split('/')[-1])

