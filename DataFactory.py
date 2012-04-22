import cPickle
import os
from Define import *
from Template import *

class DataHolder:
	__instance = None
	__stategy = None

	def __init__(self,strategy):
		if DataHolder.__instance != None:
			raise Exception("This is singleton class!")
		DataHolder.__instance = self
		if (strategy == "pickle"):
			self.__strategy = PickleDataStrategy()
		else: 
			self.__strategy = None
	
	def initData(self): 
		data = dict()
		self.save(data)
		return data

	def initPwdData(self): 
		data = dict()
		self.saveUser(data)
		return data
	
	def initTaskData(self,data,username):
		taskData = dict()
		taskData[TASK_NAME] = "untitled"
		taskData[TASK_POSTDATE] = TemplateDate.now() 
		taskData[TASK_PRIORITY] = ("Fixed")
		taskData[TASK_PROGRESS] = ("0%")
		taskData[TASK_CATEGORY] = ("Work")
		taskData[TASK_DUEDATE] = TemplateDate.initDueDate()
		taskData[TASK_MILESTONE] = list()
		taskData[TASK_USER_CATEGORY] = data[username][TASK_USER_CATEGORY]
		return taskData

	def initUserData(self,data,username):
		data[username] = dict()
		data[username][TASK_USER_CATEGORY] = list()
		data[username][USER_DATA] = list()
		data[username][TASK_USER_CATEGORY].append("Home")
		data[username][TASK_USER_CATEGORY].append("Work")
		data[username][TASK_USER_CATEGORY].append("Extra")
		self.save(data)
		return data

	@staticmethod
	def getInstance(strategy):
		if DataHolder.__instance == None:
			DataHolder(strategy)
		return DataHolder.__instance

	def save(self, data):
		self.__strategy.save(data)

	def load(self):
		return self.__strategy.load()

	def loadUser(self):
		return self.__strategy.loadUser()

	def saveUser(self, data):
		return self.__strategy.saveUser(data)

class DataStrategy:
	def save(self,data):
		pass
	def load(self):
		return None
	def saveUser(self,data):
		pass
	def loadUser(self):
		return None

class PickleDataStrategy(DataStrategy):
	def save(self,data):
		fname = open(FILE_NAME, 'w')
		object = cPickle.Pickler(fname)
		object.dump(data)
		fname.close()

	def load(self):
		if os.path.exists(FILE_NAME):
			try:
				fname = open(FILE_NAME, 'rb')
				rawdata = cPickle.Unpickler(fname)
				data = rawdata.load()
			finally:
				fname.close()
		else:
			data = {}
	
		return data

	def saveUser(self,data):
		fname = open(FILE_PWD, 'w')
		object = cPickle.Pickler(fname)
		object.dump(data)
		fname.close()

	def loadUser(self):
		if os.path.exists(FILE_PWD):
			try:
				fname = open(FILE_PWD, 'rb')
				rawdata = cPickle.Unpickler(fname)
				data = rawdata.load()
			finally:
				fname.close()
		else:
			data = {}
	
		return data

