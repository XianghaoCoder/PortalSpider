class Configures:
	"""Settings
	"""

	namesDirectories = {"teachers": "../info/teachers/",
				   "students": "../info/students/"} # the directories containing name list of teachers and students

	namesFile = "names.txt" # the name of the file containing a list of names of persons
	namesLeftFile = "names_left.txt" # the name of the file containing a names of persons not crawlled

	defaultStudentBasicInfoList = ["firstName", "lastName", 
							"preferredName"]  # default basic information of student that will be collected
	defaultTeacherBasicInfoList = ["firstName", "lastName", 
							"preferredName"]  # default basic information of teacher that will be collected