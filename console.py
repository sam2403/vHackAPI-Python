#!/usr/bin/python2.7
#-*- coding: utf-8 

from classes import API
from classes import IP
from classes import Passwords
from utils import Utils
import time
import json
import subprocess
from PIL import Image
import base64
import pytesseract
import cStringIO


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
		time.sleep(2)
		temp = ut.requestString("user::::pass::::port::::target::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(passwd[1].strip()) + "::::" +  str(target) + "::::" + str(uhash), "vh_trTransfer.php")
		if temp == "10":
			return False
		else:
			return True

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

	def getIP(self, blank):
		ut = Utils()
		info = self.myinfo()
		info = json.loads(info)
		uhash = info['uhash']
		temp = ut.requestString("user::::pass::::uhash::::global", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + "0", "vh_getImg.php")
		jsons = json.loads(temp)
		for i in range(0, len(jsons["data"])):
			hostname = jsons["data"][i]["hostname"]
			imgstring = 'data: image/png;base64,'+jsons["data"][i]['img']
			imgstring = imgstring.split('base64,')[-1].strip()
			pic = cStringIO.StringIO()
			image_string = cStringIO.StringIO(base64.b64decode(imgstring))
			image = Image.open(image_string)

			# Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
			#bg = Image.new("RGB", image.size, (255,255,255))
			#bg.paste(image,image)
			if "Hatched by the FBI" in pytesseract.image_to_string(image) or "Watched by the FBI" in pytesseract.image_to_string(image):
				return 0, hostname
			else:
				temp = ut.requestString("user::::pass::::uhash::::hostname", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + hostname, "vh_scanHost.php")
				try:
					jsons = json.loads(temp)
					return 0, jsons['ipaddress']
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
		if temp == "null":
			return False
		cmd = "python ocr.py '"+ str(temp) + "'"
		imgs = subprocess.check_output(cmd, shell=True)
		print temp
		if imgs != "0":
			password = self.enterPassword(imgs, ip, uhash)
			if password:
				print password
				return True
				user = self.scanUser()
				if len(user) > 2:
					fwlevel = user[0].split(":")[1]
					avlevel = user[1].split(":")[1]
					spamlevel = user[2].split(":")[1]
					sdklevel = user[3].split(":")[1]
					ipsplevel = user[4].split(":")[1]
					money = user[5].split(":")[1]
					saving = user[6].split(":")[1]
					anonymous = user[7].split(":")[1]
					username = user[8].split(":")[1]
					winlo = user[9].split(":")[1]
					winchance = user[10].split(":")[1]
					spywarelevel = user[11].split(":")[1]
				else:
					avlevel = "????"
					winchance = 0

				if type(winchance) == "int":
					if "?" in winchance:
						winchance = 0

				if not "?" in avlevel:
					if int(avlevel) < max and int(winchance) > 75 and anonymous == "YES":
						out = self.transferMoney(ip)
						if len(out) == 5:
							if not "?" in money:
								print "\n[TargetIP: " + ip +"]\n\nMade " + "{:11,}".format(int(out[1].split(":")[1])) + " and " + "{:2d}".format(int(out[3].split(":")[1])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + winchance + " Anonymous: "+ anonymous +" username: "+ username + " saving: " + saving
							else:
								print "\n[TargetIP: " + ip + "]\n\nMade " + "{:11,}".format(int(out[1].split(":")[1])) + " and " + "{:2d}".format(int(out[3].split(":")[1])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + money + "\n YourWinChance: " + winchance + " Anonymous: " + anonymous +" username: "+ username + " saving: " + saving
							log = self.clearLog(ip)
							if log == True:
								print "clearing log"
							else:
								print "no clear log upgrade your SDK"
							return True
					else:
						#print "\n"
						if int(avlevel) < max:
							#print "Antivir to high " + str(avlevel)
							#print "passed"
							pass
						if int(winchance) < 75:
							#print "winchance is poor: " + str(winchance)
							#print "passed"
							pass
						if anonymous == "NO":
							#print "No Anonymous need"
							#print "passed"
							pass
				else:
					if len(avlevel) == 4:
						print avlevel
						print "Cant load User"
					else:
						print "Scan to low"
			else:
				print "Password Wrong"
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
		i1 = 0
		while i1 < amount:
			host, ips = self.getIP(True)
			if ips != 0:
				if self.attackIP(ips,max):
					i1 += 1
					print "Waiting..."
					time.sleep(wait)
			else:
				print "Warning FBI Blocking account in " + str(host)

	def __init__(self,api):
		self.api = api
