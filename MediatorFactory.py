from DataManager import *
from LoginManager import *
from Define import *
from Template import *
from Validator import *
import wx

class AbstractMediator:
	def __init__(self,parent): pass
	@staticmethod
	def getInstance(parent): pass
	def response(self,command): pass		

class FactoryMediator:
	@staticmethod
	def getMediator(parent,mediator):
		if mediator == "Main":
			return MainTaskMediator.getInstance(parent)
		elif mediator == "AddEdit":
			return AddTaskMediator.getInstance(parent)
		elif mediator == "Login":
			return LoginMediator.getInstance(parent)
		elif mediator == "Complete":
			return CompleteTaskMediator.getInstance(parent)
		elif mediator == "Global":
			return GlobalMediator.getInstance()
		else:
			return None

class LoginMediator(AbstractMediator):
	__instance = None
	__global = None

	def __init__(self,parent):
		LoginMediator.__instance = self
		self.parent = parent
		self.__global = FactoryMediator.getMediator(None,"Global")

	@staticmethod
	def getInstance(parent):
		LoginMediator(parent)
		return LoginMediator.__instance 	

	def response(self,command):
		parent = self.parent
		print "Login Mediator",command["type"]
		if command["type"] == "Login":
			res = LoginManager.getInstance().checkUser(command["user"],command["password"])
			if(res==""):
				self.__global.response(command)
			else:
				parent.init()
				dialog = wx.MessageDialog(None,res, 'Login failed', wx.ICON_EXCLAMATION|wx.CENTER)
				dialog.ShowModal()	
		else:
			pass

class GlobalMediator(AbstractMediator):
	__instance = None

	def __init__(self,parent):
		if GlobalMediator.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			GlobalMediator.__instance = self
			self.parent = parent

	def setTaskIndex(self, index):
		self.__index = index

	@staticmethod
	def getInstance():
		if GlobalMediator.__instance == None:
			raise Exception("Class need to be initialized first")
		return GlobalMediator.__instance 	

	def response(self,command):
		parent = self.parent
		print "Global Mediator",command["type"]
		if command["type"] == "Login":
			parent.login(command["user"])
		elif command["type"] == "AddTask":
			parent.addTask()
		elif command["type"] == "EditTask":
			parent.editTask(command["data"])
			parent.main.init()
		elif command["type"] == "PostTask":
			DataManager.getInstance().saveTask(command["data"])	
			parent.main.init()
		elif command["type"] == "ValidateTask":
			Validator(VALIDATION_LEVEL).validateTask(command["data"])	
		elif command["type"] == "SaveAll":
			DataManager.getInstance().save(command["data"])	
			parent.main.init()
		elif command["type"] == "SaveCategory":
			DataManager.getInstance().saveCategory(command["data"])	
		elif command["type"] == "SaveTaskDone":
			DataManager.getInstance().saveTaskDone(command["data"])	
		elif command["type"] == "ShowComplete":
			if(command["data"] == list()):
				dialog = wx.MessageDialog(None,MESSAGE_NO_COMPLETE_TASK, 'No completed task', wx.ICON_INFORMATION|wx.CENTER)
				dialog.ShowModal()	
			else:
				parent.showComplete(command["data"])
		elif command["type"] == "Logout":
			parent.logout()
		else:
			pass

class CompleteTaskMediator(AbstractMediator):
	__instance = None
	__global = None
	def __init__(self,parent):
		CompleteTaskMediator.__instance = self
		self.parent = parent
		self.__global = FactoryMediator.getMediator(None,"Global")

	@staticmethod
	def getInstance(parent):
		CompleteTaskMediator(parent)
		return CompleteTaskMediator.__instance 	

	def response(self,command):
		main = self.parent
		print "Complete mediator", command["type"]
		if command["type"] == "AddTask":
			self.__global.response(command)
		elif command["type"] == "Close":
			main.destroy()
		elif command["type"] == "TaskSelect":
			main.mileStoneBoxWidget.setValue(main.data[command["index"]][TASK_MILESTONE])		
		elif command["type"] == "TaskSort":
			print "field type", command["field"]
			main.mileStoneBoxWidget.setValue(list())
			main.data=Template.sort(main.data,command["field"])
			command["type"] = "SaveTaskDone"
			command["data"] = main.data
			self.__global.response(command)	
			main.taskListBoxWidget.setValue(main.data)
		else:
			pass


class MainTaskMediator(AbstractMediator):
	__instance = None
	__global = None
	def __init__(self,parent):
		MainTaskMediator.__instance = self
		self.parent = parent
		self.__global = FactoryMediator.getMediator(None,"Global")

	@staticmethod
	def getInstance(parent):
		MainTaskMediator(parent)
		return MainTaskMediator.__instance 	

	def response(self,command):
		main = self.parent
		print "Main mediator", command["type"]
		if command["type"] == "AddTask":
			self.__global.response(command)
		elif command["type"] == "RemoveTask":
			main.taskListBoxWidget.onRemoveTask()
		elif command["type"] == "RemoveTask2":
			dialog = wx.MessageDialog(None,MESSAGE_REMOVE_TASK, 'Question',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			decision = dialog.ShowModal()
			if(decision == wx.ID_NO): return
			del(main.data[USER_DATA][command["index"]])
			main.init()
			command["type"] = "SaveAll"
			command["data"] = main.data
			self.__global.response(command)
		elif command["type"] == "EditTask":
			main.taskListBoxWidget.onEditTask()
		elif command["type"] == "EditTask2":
			command["type"] = "EditTask"
			data = dict(main.data[USER_DATA][command["index"]])
			del(main.data[USER_DATA][command["index"]])
			data[TASK_USER_CATEGORY] = main.data[TASK_USER_CATEGORY]		
			command["data"] = data
			self.__global.response(command)
		elif command["type"] == "CopyTask":
			main.taskListBoxWidget.onCopyTask()
		elif command["type"] == "CopyTask2":
			data = dict(main.data[USER_DATA][command["index"]])
			main.data[USER_DATA].append(data)
			main.init()
			command["type"] = "SaveAll"
			command["data"] = main.data
			self.__global.response(command)
		elif command["type"] == "UpdateTask":
			command = main.mileStoneBoxWidget.getValue()
			command["type"] = "UpdateTask2"
			self.response(command)
		elif command["type"] == "UpdateTask2":
			main.taskListBoxWidget.onUpdateTask(command)
		elif command["type"] == "UpdateTask3":
			main.data[USER_DATA][command["index"]][TASK_PROGRESS] = str(command["progress"]) + "%"
			main.data[USER_DATA][command["index"]][TASK_MILESTONE] = command["data"]
			if(main.data[USER_DATA][command["index"]][TASK_PROGRESS]=="100%"):
				if(main.data.has_key(TASK_DONE)==False):
					main.data[TASK_DONE] = list()
				dialog = wx.MessageDialog(None,MESSAGE_TASK_DONE, 'Task done',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
				decision = dialog.ShowModal()
				if(decision == wx.ID_YES):
					main.data[USER_DATA][command["index"]][TASK_FINISHDATE] = TemplateDate.now()
					main.data[TASK_DONE].append(main.data[USER_DATA][command["index"]])
					del(main.data[USER_DATA][command["index"]])
			command["type"] = "SaveAll"
			command["data"] = main.data
			self.__global.response(command)	
			main.taskListBoxWidget.setSelect(command["index"])
			command["type"] = "TaskSelect"
			self.response(command)
		elif command["type"] == "TaskSelect":
			if(len(main.data[USER_DATA]) <= command["index"]):
				return
			main.mileStoneBoxWidget.setValue(main.data[USER_DATA][command["index"]][TASK_MILESTONE])		
		elif command["type"] == "TaskSort":
			print "field type", command["field"]
			main.mileStoneBoxWidget.setValue(list())
			main.data[USER_DATA]=Template.sort(main.data[USER_DATA],command["field"])
			command["type"] = "SaveAll"
			command["data"] = main.data
			self.__global.response(command)	
		elif command["type"] == "ShowComplete":
			if( main.data.has_key(TASK_DONE) == False):
				main.data[TASK_DONE] = list()
			command["data"] = main.data[TASK_DONE]
			self.__global.response(command)
		elif command["type"] == "Logout":
			dialog = wx.MessageDialog(None,MESSAGE_LOGOUT, 'Logout',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			decision = dialog.ShowModal()
			if(decision == wx.ID_NO): return
			self.__global.response(command)
		else:
			pass


class AddTaskMediator(AbstractMediator):
	__global = None
	__instance = None
	def __init__(self,parent):
		AddTaskMediator.__instance = self
		self.parent = parent
		self.__global = FactoryMediator.getMediator(None,"Global")

	def setTaskIndex(self, index):
		self.__index = index

	@staticmethod
	def getInstance(parent):
		AddTaskMediator(parent)
		return AddTaskMediator.__instance 	

	def response(self,command):
		main = self.parent
		print "Task mediator",command["type"]
		if command["type"] == "AddMilestone":
			main.milestoneBoxWidget.addMilestone()
		elif command["type"] == "RemoveMilestone":
			main.milestoneBoxWidget.removeMilestone(main.data[TASK_MILESTONE])
		elif command["type"] == "CopyMilestone":
			main.milestoneBoxWidget.copyMilestone()
		elif command["type"] == "LoadCategory":
			return main.data[TASK_USER_CATEGORY]
		elif command["type"] == "SaveCategory":
			main.data[TASK_USER_CATEGORY] = command["data"]
			self.__global.response(command)	
		elif command["type"] == "SaveTask":
			main.data[TASK_USER_CATEGORY] = command["data"]
		elif command["type"] == "DeleteTask":
			dialog = wx.MessageDialog(None,MESSAGE_REMOVE_TASK, 'Question',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			decision = dialog.ShowModal()
			if(decision == wx.ID_NO): return
			main.destroy()
		elif command["type"] == "PostTask":
			data = dict()
			data[TASK_NAME] = main.nameWidget.getValue()
			data[TASK_PRIORITY] = main.priorityWidget.getValue()
			data[TASK_DUEDATE] = TemplateDate.formatDate(main.duedateWidget.getValue())
			data[TASK_POSTDATE] = TemplateDate.now()
			data[TASK_CATEGORY] = main.categoryWidget.getValue()
			data[TASK_MILESTONE] = main.milestoneBoxWidget.getValue()
			data[TASK_PROGRESS] = Template.getProgress(data[TASK_MILESTONE])
			command["data"] = data
			command["type"] = "ValidateTask"
			self.__global.response(command)
			valid = command["data"]
			if (valid["status"]):
				command["type"] = "PostTask"
				self.__global.response(command)
				main.destroy()
			else:
				dialog = wx.MessageDialog(None,valid["message"], 'Add task failed', wx.ICON_EXCLAMATION|wx.CENTER)
				dialog.ShowModal()	
		else:
			pass
