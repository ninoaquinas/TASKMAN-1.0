from Define import *
from Template import *

class Validator:
	__stategy = None

	def __init__(self,strategy):
		if (strategy == "simple"):
			self.__strategy = SimpleValidatorStrategy()
		elif (strategy == "moderate"):
			self.__strategy = ModerateValidatorStrategy()
		else: 
			self.__strategy = None

	def validateTask(self, data):
		self.__strategy.validateTask(data)	

class ValidatorStrategy:
	def validateTask(self,data):
		pass

class SimpleValidatorStrategy(ValidatorStrategy):
	def validateTask(self,data):
		data["message"] = ""
		if (data[TASK_NAME] == ""):
			data["message"] += "\n -You need to specify the task name"
		if (data[TASK_CATEGORY] == ""):
			data["message"] += "\n -You need to specify the task category"
		if (data[TASK_MILESTONE] == list()):
			data["message"] += "\n -You need to have at least 1 milestone"
		if (data["message"] == ""):
			data["status"] = True
		else:
			data["status"] = False

class ModerateValidatorStrategy(ValidatorStrategy):
	def validateTask(self,data):
		data["message"] = ""
		if (data[TASK_NAME] == "" or data[TASK_NAME] == "untitled"):
			data["message"] += "\n -You need to change the task name (cannot be blank or \" untitled \" "
		if (data[TASK_CATEGORY] == "" or data[TASK_CATEGORY] == None):
			data["message"] += "\n -You need to specify the task category"
		if (data[TASK_PROGRESS] == "100%"):
			data["message"] += "\n -You are not supposed to add completed taks"
		if (data[TASK_MILESTONE] == list()):
			data["message"] += "\n -You need to have at least 1 milestone"
		else:
			for i in range(len(data[TASK_MILESTONE])):
				weight = None
				try:
					weight = int(data[TASK_MILESTONE][i][MILESTONE_WEIGHT])
				except ValueError:
					pass
				if(weight == None):
					data["message"] += "\n -Your milestone weight need to be an integer between 0 and 100"
					break
				if(weight<0 or weight>=100):
					data["message"] += "\n -Your milestone weight must be between 0 and 100"
					break
		if (TemplateDate.compareDate(data[TASK_DUEDATE],data[TASK_POSTDATE],0) == False):
			data["message"] += "\n -You need to set the due date in the future"
		if (data["message"] == ""):
			data["status"] = True
		else:
			data["status"] = False

