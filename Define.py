#collection of key string use throughout the project
TASK_DONE = "task_done"
TASK_USER_CATEGORY = "task_category_list"
USER_DATA = "user_data"
TASK_ID = "task_id"

TASK_NAME = "task_name"
TASK_POSTDATE = "task_postdate"
TASK_PRIORITY = "task_priority"
TASK_PROGRESS = "task_progress"
TASK_CATEGORY = "task_category"
TASK_DUEDATE = "task_duedate"
TASK_FINISHDATE = "task_finishdate"
TASK_MILESTONE = "task_milestone"
TASK_STATUS = "task_status"

TASK_STATUS_NORMAL = "normal"
TASK_STATUS_WEEK = "week"
TASK_STATUS_DAY = "day"
TASK_STATUS_HOUR = "hour"
TASK_STATUS_OVERDUE = "overdue"

TASK_NAME_INDEX = 0 
TASK_POSTDATE_INDEX = 1 
TASK_PRIORITY_INDEX = 2
TASK_PROGRESS_INDEX = 3
TASK_CATEGORY_INDEX = 4
TASK_DUEDATE_INDEX = 5
TASK_MILESTONE_INDEX = 6

MILESTONE_NAME = "milestone_name"
MILESTONE_WEIGHT = "milestone_weight"
MILESTONE_DETAILS = "milestone_details"
MILESTONE_CHECKED = "milestone_checked"
MILESTONE_FINISHDATE = "milestone_finish"

MILESTONE_NAME_INDEX = 0
MILESTONE_WEIGHT_INDEX = 1
MILESTONE_DETAILS_INDEX = 2


#configuration file
SAVE_STRATEGY = "pickle"
FILE_NAME = "taskman.dat"
FILE_PWD = "pwd.dat"
VALIDATION_LEVEL = "moderate"

MESSAGE_TASK_DONE = """Congratulations, you have completed the task!
The task you have completed will be remove from the list
Press yes to confirmed"""
MESSAGE_REMOVE_TASK = "Are you sure you want to remove the task?"
MESSAGE_LOGIN_WRONG_PASSWORD = "Sorry, the username is taken or \nyou had key in the wrong password"
MESSAGE_LOGIN_NO_USERNAME = "Are you a human? \n you must have a name, right?"
MESSAGE_LOGIN_NO_PASSWORD = "Sorry, you might want to secure \nyourself first with a password"
MESSAGE_LOGIN_ERROR_EQUAL = "Hey there, please be more creative.\n differs your username and password okay?"
MESSAGE_LOGIN_ERROR = "Sorry, we are not so sure what is happening now. \nPlease report this bug if you find it"
MESSAGE_LOGOUT = "Are you sure you want to logout?"
MESSAGE_NO_COMPLETE_TASK = "There is no completed task yet"

TASK_STATUS_WEEK_COLOR = "YELLOW"
TASK_STATUS_DAY_COLOR = "ORANGE"
TASK_STATUS_HOUR_COLOR = "ORANGE RED"
TASK_STATUS_OVERDUE_COLOR = "RED"

TASK_STATUS_WEEK_CRITERIA = 7*24*60
TASK_STATUS_DAY_CRITERIA = 24*60 
TASK_STATUS_HOUR_CRITERIA = 60

