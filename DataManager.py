import time
import datetime
from DataFactory import *
from Define import *

class DataManager:
	__instance = None
	__holder = None
	__data = None
	__user = None
	__userdata = dict()

	def __init__(self,strategy,username):
		DataManager.__instance = self
		self.__holder = DataHolder.getInstance(strategy)
		self.__data = self.__holder.load()
		self.__user = username

		#check if save file exist or init the save file
		if(self.__data == None):
			self.__data = self.__holder.initData()

		#check if userdata exist
		if(self.__data.has_key(username)==False):
			self.__data = self.__holder.initUserData(self.__data,username)
		
		#create user data
		self.__userdata = self.__data[username]

	@staticmethod
	def getInstance():
		return DataManager.__instance

	def save(self, data):
		self.__data[self.__user] = data
		self.__holder.save(self.__data)
	
	def saveTask(self, data):
		self.__data[self.__user][USER_DATA].append(data)
		self.__holder.save(self.__data)

	def saveTaskDone(self, data):
		self.__data[self.__user][TASK_DONE] = data
		self.__holder.save(self.__data)
	
	def saveCategory(self, data):
		self.__data[self.__user][TASK_USER_CATEGORY] = data
		self.__holder.save(self.__data)

	def load(self):
		return self.__userdata

	def getData(self,command):
		return self.__data[command["type"]]

	def initTask(self):
		return self.__holder.initTaskData(self.__data,self.__user)
"""
if __name__ == '__main__':
	DataManager.getInstance("pickle").save({TASK_CATEGORY:["Work","School","Home"]})
	data = dict(DataManager.getInstance("pickle").load())
"""	
