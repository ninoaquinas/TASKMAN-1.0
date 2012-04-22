import time
import datetime
from DataFactory import *
from Define import *

class LoginManager:
	__instance = None
	__holder = None
	__data = None

	def __init__(self,strategy):
		if LoginManager.__instance != None:
			raise Exception("This is singleton class!")
		LoginManager.__instance = self
		self.__holder = DataHolder.getInstance(strategy)
		self.__data = self.__holder.loadUser()

		#check if save file exist or init the save file
		if(self.__data == None):
			self.__data = self.__holder.initPwdData()

		self.__data = self.__holder.loadUser()
	
	@staticmethod
	def getInstance():
		return LoginManager.__instance

	def save(self, data):
		self.__holder.saveUser(self.__data)

	def checkUser(self, user, password):
		if(self.__data.has_key(user)==False):
			self.__data[user] = password
			self.save(self.__data)
			return True	
		elif(self.__data[user] == password):
			return True
		else:
			return False
