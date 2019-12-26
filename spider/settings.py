class Settings:
	"""This class stores basic settings.

	Codes in portal/spider or portal/asker may need them.
	"""

	classInfo = {"class": "Class",
				 "room": "Room",
				 "time": "Time", 
				 "teacher": "Teacher"}  # dict mapping name of each property of a class to its name in raw text
	infoMap = {"firstName": "Given Names",
			   "lastName": "Family Name",
			   "preferredName": "Preferred Name",
			   "email": "Email",
			   "intake": "Intake"
			   }  # dict mapping names of each property of basic information to raw text in Portal page
	defaultStudentBasicInfoList = ["firstName", "lastName", 
							"preferredName"]  # default basic information of student that will be collected
	defaultTeacherBasicInfoList = ["firstName", "lastName", 
							"preferredName"]  # default basic information of teacher that will be collected

	weekdays = ["mon", "tue", "wed", "thu", "fri"]
	periods = ["p1", "p2", "p3", "p4", "p5"]

	studentsDirectory = "../info/students/" # the path of the directory containing students' information (data and photos)
	teachersDirectory = "../info/teachers/" # the path of the directory containing teachers' information (data and photos)
	dataDirectory = "data/" # part of the path of the directory containing data
	photosDirectory = "photos/" # part of the path of the directory containing photots
	namesFile = "names.txt" # the name of the file containing a list of names of persons
	namesLeftFile = "names_left.txt" # the name of the file containing a names of persons not crawlled
	studentsNamePath = studentsDirectory + namesFile  # the path of a list of names of all students
	teachersNamePath = teachersDirectory + namesFile  # the path of a list of names of all teachers
	studentsNameLeftPath = studentsDirectory + namesLeftFile # the path of a list of names of students not crawlled
	teachersNameLeftPath = teachersDirectory + namesLeftFile # the path of a list of names of teachers not crawlled
	studentDataPath = studentsDirectory + dataDirectory  # the path of information of students (json files)
	teacherDataPath = teachersDirectory + dataDirectory  # the path of information of teachers (json files)
	studentPhotosPath = studentsDirectory + photosDirectory  # the path of photos of students (jpeg files)
	teacherPhotosPath = teachersDirectory + photosDirectory  # the path of photos of teachers (jpeg files)

	portalIndexUrl = "https://portal.trinity.edu.au/portal/today/today.php"  # the url of Portal index page
	basicInfoSuffixUrl = "https://portal.trinity.edu.au/portal/directory/directory.php?uid="  # suffix of the url of student's basic information page
	timetableSuffixUrl = "https://portal.trinity.edu.au/portal/sat/view_timetable.php?uid="  # suffix of the url of students's timetable page
	photoSuffixUrl = "https://portal.trinity.edu.au/portal/get_ldap_photo.php?" # suffix of the url of photos

