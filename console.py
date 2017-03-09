#!/usr/bin/python2.7
#-*- coding: utf-8 

from classes import API
from classes import IP
from classes import Passwords
from utils import Utils
from ocr import OCR
from PIL import Image
from io import BytesIO
import base64
import time
import json
import subprocess
from PIL import Image
import base64
import cStringIO
import requests
import re
import concurrent.futures

class Console:
	def myinfo(self):
		ut = Utils()
		temp = ut.requestString("user::::pass::::gcm::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "eW7lxzLY9bE:APA91bEO2sZd6aibQerL3Uy-wSp3gM7zLs93Xwoj4zIhnyNO8FLyfcODkIRC1dc7kkDymiWxy_dTQ-bXxUUPIhN6jCUBVvGqoNXkeHhRvEtqAtFuYJbknovB_0gItoXiTev7Lc5LJgP2" + "::::" + "userHash_not_needed", "vh_update.php")
		return temp

	def requestPassword(self,ip):
		ut = Utils()
		arr = ut.requestArray("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_vulnScan.php")
		imgs = Passwords(arr)
		return imgs

	def enterPassword(self, passwd, target, uhash):
		passwd = passwd.split("p")
		ut = Utils()
		temp = ut.requestString("user::::pass::::port::::target::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(passwd[1].strip()) + "::::" +  str(target) + "::::" + str(uhash), "vh_trTransfer.php")
		if temp == "10":
			return False
		else:
			return temp

	def scanUser(self):
		ut = Utils()
		arr = ut.requestArray("user::::pass::::", self.api.getUsername() + "::::" + self.api.getPassword() + "::::", "vh_scanHost.php")
		return arr

	def transferMoney(self, ip):
		ut = Utils()
		arr = ut.requestArray("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_trTransfer.php")
		return arr

	def clearLog(self, ip):
		ut = Utils()
		s = ut.requestString("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_clearAccessLogs.php")
		if s == "0":
			return True
		else:
			return False

	def uploadSpyware(self, ip):
		ut = Utils()
		s = ut.requestString("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_spywareUpload.php")
		if s == "0":
			return True
		else:
			return False 

	def getTournament(self):
		ut = Utils()
		temp = ut.requestString("user::::pass::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "UserHash_not_needed", "vh_update.php")
		if "tournamentActive" in temp:
			if not "2" in temp.split('tournamentActive":"')[1].split('"')[0]:
				return True
			else:
				return False

	def read(self, imgdata):
		if len(imgdata) > 10:
			im = Image.open(BytesIO(base64.b64decode(imgdata)))	
		else: 
			return ""	
		pix = im.load()
		width = im.size[0]
		height = im.size[1]
		record = False
		end = False
		words = []
		word = ""
		ut = Utils()
		passwd = ""
		count = 0
		for i1 in range(0,width):
			s = ""
			for i2 in range(0,height):
				if pix[i1,i2][3] == 255:
					s += "1"
				else:
					s += "0"
			if "1" in s and not record:
				record = True
			if not "1" in s and record:
				record = False
				end = True
			if record:
				word += s
			elif end:
				hash = ut.md5hash(word)
				count += 1
				letter = self.check(hash);
				if "null" in letter:
					words.append('		hashes.append(":' + hash + '") #' + str(count))
					self.hashes.append(" :" + hash)
					passwd += " "
					#print imgdata
				else:
					passwd += letter
				word = ""
				end = False
		for i1 in words:
			pass
			#print i1
		return passwd

	def check(self,hash):
		for i1 in self.hashes:
			if hash == i1[2:]:
				return i1[0]
		return "null"


	def getIP(self, blank):
		ut = Utils()
		info = self.myinfo()
		info = json.loads(info)
		uhash = info['uhash']
		temp = ut.requestString("user::::pass::::uhash::::global", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + "0", "vh_getImg.php")
		jsons = json.loads(temp)
		for i in range(0, len(jsons["data"])):
			hostname = str(jsons["data"][i]["hostname"])

			# Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
			#bg = Image.new("RGB", image.size, (255,255,255))
			#bg.paste(image,image)
			print self.read(jsons["data"][i]['img'])
			if "Hatched by the FBI" in self.read(jsons["data"][i]['img']):
				return 1, hostname
			else:
				temp = ut.requestString("user::::pass::::uhash::::hostname", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + hostname, "vh_scanHost.php")
				try:
					jsons = json.loads(temp)
					return 0, str(jsons['ipaddress'])
				except TypeError:
					return 0, 0
				#print str(jsons['ipaddress'])
		

	def attackIP(self, ip, max):
		ut = Utils()
		info = self.myinfo()
		info = json.loads(info)
		uhash = info['uhash']
		temp = ut.requestString("user::::pass::::uhash::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + uhash + "::::" + ip, "vh_loadRemoteData.php")

		jsons = json.loads(temp)
		
		o = OCR() 
		imgs = o.getSolution(str(temp))
		if imgs != None:
			try:
				user = jsons['username']
				winchance = jsons['winchance']
			except TypeError:
				return False
			try:
				if not "?" in str(winchance):
					fwlevel = jsons['fw']
					avlevel = jsons['av']
					spamlevel = jsons['spam']
					sdklevel = jsons['sdk']
					ipsplevel = jsons['sdk']
					money = jsons['money']
					saving = jsons['savings']
					anonymous = jsons['anonymous']
					username = jsons['username']
					winlo = jsons['winelo']
					winchance = jsons['winchance']
					spywarelevel = jsons['spyware']
				else:
					avlevel = "????"
					winchance = 0
					print "no scan username"
					return False

			except TypeError:
				fwlevel = jsons['fw']
				avlevel = jsons['av']
				spamlevel = jsons['spam']
				sdklevel = jsons['sdk']
				ipsplevel = jsons['sdk']
				money = jsons['money']
				saving = jsons['savings']
				anonymous = jsons['anonymous']
				username = jsons['username']
				winlo = jsons['winelo']
				winchance = jsons['winchance']
				spywarelevel = jsons['spyware']

			if type(winchance) == "int":
				if "?" in winchance:
					winchance = 0
					print "no chance"
					return False

			if not "?" in str(avlevel):
				if int(avlevel) < max and int(winchance) > 75 and str(anonymous) == "YES":
					password = self.enterPassword(imgs, ip, uhash)
					jsons = json.loads(password)
					if password:
						try:
							if not "?" in str(money) and str(jsons['result']) == 0:
								print "\n[TargetIP: " + str(ip) +"]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: "+ str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
								return True
							else:
								print "\n[TargetIP: " + str(ip) + "]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: " + str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
						except KeyError:
							print "Bad attack"
							return False
					else:
						print "Password Wrong"
						return False
				else:
					#print "\n"
					if int(avlevel) > max:
						print "Antivir to high " + str(avlevel)
						#print "passed"
						return False
					if int(winchance) < 75:
						print "winchance is poor: " + str(winchance)
						#print "passed"
						return False
					if str(anonymous) == "NO":
						print "No Anonymous need"
						#print "passed"
						return False
			else:
				print avlevel
				if len(avlevel) == 4:
					print avlevel
					print "Cant load User"
					return False
				else:
					print "Scan to low"
					return False
		else:
			print "Password Error"
			return False

	def attackIP2(self,ip,max):	
		ut = Utils()
		o = OCR(False)
		imgs = self.requestPassword(ip)
		selection = o.getPassword(imgs)
		print selection

	def attack(self, amount, max, wait):
		with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
			for i in range(1,amount):
				FBI, ips = self.getIP(True)
				if FBI == 0:
					lineexec = executor.submit(self.attackIP, ips, max)
					print "Waiting..."
					time.sleep(wait)
				else:
					print "Warning FBI Blocking account in " + str(ips) + " I'm not attack"

	def __init__(self, api):
		self.api = api

		hashes = []
		hashes.append("-:9d38e2356e3ef0c497aa594f1553232a")
		hashes.append("0:de388a423f28040cea9eb83196bd3fc2")
		hashes.append("1:a4bd8b698572e4deb66dca2a1a82ce80")
		hashes.append("2:2e649a81af630788522f7590be243818")
		hashes.append("3:35d2d07aa1017dc2280878e9728acd8f")
		hashes.append("4:4779d033d7ef5f1761e2bf5c2d8f3f93")
		hashes.append("5:47c07b0a04e161e8e879803449d4649d")
		hashes.append("6:9cd13d56408465e8dc39e2433cad513c")
		hashes.append("7:13a4ec1d6204a60723983ce0c667662f")
		hashes.append("8:d96f2958c199bde40350c1584412d532")
		hashes.append("9:6b8d59204cdff06a9daccf7c88805c3e")

		hashes.append("A:ffb2d85490c0460bb6fcdcc100f91a13")
		hashes.append("B:eb319e01cd62f01196a663f73286078b")
		hashes.append("C:b1eb521ab6b766176c546414fc90af04")
		hashes.append("D:ef08990c2bb2b140412391757eded4f5")
		hashes.append("E:2fa219869ce38138ba79c1f05657b112")
		hashes.append("F:7d8856b8f9872283aacf66c51b38c53a")
		hashes.append("G:6e888615c7fde253336bee31ad05b28e")
		hashes.append("H:26209353e4090fe7df6c7b72611e32ce")
		hashes.append("I:883f6bb17fd1de3b1fffacc753cff737")
		hashes.append("J:598dc845e042c740b4a914ca14ad9070")
		hashes.append("K:2d2e5e2080aec9f32d3e7cc511dac0f1")
		hashes.append("L:1c4214a3eb969f426f71ad9a89889721")
		hashes.append("M:6d4b9753afb275ab5ab9e4f92883f6ac")
		hashes.append("N:a93b9e9fb115207007f90f60c7b2894b")
		hashes.append("O:630720e00b3b44e8ed67e15af71e8df1")
		hashes.append("P:0ccd5a2b971fcce6fb6abe365ff1c311")
		hashes.append("Q:af95e91a486f9bc725176751c6194385")
		hashes.append("R:4ac2ad62b3b9ec873096c7b90a341b2d")
		hashes.append("S:18bea5850e25d7b6229fcac6e0fbd118")
		hashes.append("T:3d58b3adb23a56cc26eb8f2ee8afab08")
		hashes.append("U:c9019f81a82c42ef0dfb24930efec0c8")
		hashes.append("V:5f0d89b696adf57a2e279d812fe27fd7")
		hashes.append("W:5dfbc0cb803fb648cf2047983fa66074")
		hashes.append("X:eb0a95c0c70715e327cfc9399ede8849")
		hashes.append("Y:81858a0d10ae0dddce4a108b6098830d")
		hashes.append("Z:ed70c8c68f40f39fee952ad98dbf681d")

		hashes.append("[:a68c07c90910f7e296d90338b907ee3d")
		hashes.append("]:842af13feb5bcb70120032a59631c46d")
		hashes.append("_:4b6573a852d0f6e3b707736060b620a9")

		hashes.append("b:7e58388568826ea1b36d541f160d9554")
		hashes.append("c:91d1d3ecf67e766c67d83fa8e926a686")
		hashes.append("d:f4fe98c8df9033bfb66d23bfc7777197")
		hashes.append("e:d4bf766ba2638b1565f564e67f108d4f")
		hashes.append("f:af9c32c34ccd5c5524779e7f9524eed4")
		hashes.append("g:b55bf1a14f080cf100eef7b41f467e39")
		hashes.append("h:36c87bd7f5a3b165747d175f5d0d5138")
		hashes.append("i:aba1053a0d1d0f27d0f861fd6de09cfa")
		hashes.append("j:e52eb4b518ebf76d7253596828fb264e")
		hashes.append("k:ecd3850e69b886de3d9addf46ac9d04c")
		hashes.append("l:918743f6f233d2761ce32ce778d120c3")
		hashes.append("m:8adc1bb85417cf1e990f2fbab913b758")
		hashes.append("n:93197f7d2c15b1414b1c3147606d3249")
		hashes.append("o:b21a47fee49bcde77f8f48371423f7fc")
		hashes.append("p:9d1dec9af4ce0e7e7f817cdf5b40d86c")
		hashes.append("q:c6db96eba8580b4fb93314b0e9e4d6ee")
		hashes.append("r:aa2263dc4b1a50451cbe4261e19da856")
		hashes.append("s:2f5762adfc31944c05b53dd1f71cbbd4")
		hashes.append("t:6188e543842321b6f520b1302be5bb27")
		hashes.append("u:cf3372f39d14f657e0170d28c2629e6a")
		hashes.append("v:30a319a29c606f164f8ca34a4ab01401")
		hashes.append("w:c1a02ecd4d0bb01079043f5a7cfd326d")
		hashes.append("x:6bab42f5c0b26608091581a4dda7c50b")
		hashes.append("y:6484dbde0869f416eebf0c1e51c9b493")
		hashes.append("z:bfe55d70c55c1251b4d10877e7df67da")
		hashes.append("{:5de49094f406aacea4e23d201d71edfc")
		hashes.append("}:77dbf4bf90663fcde8398f6b367631fb")

		hashes.sort()

		self.hashes = hashes
