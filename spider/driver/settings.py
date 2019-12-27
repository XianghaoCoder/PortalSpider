class Settings:
	"""Some settings for Portal driver
	"""

	"""
		URLs
	"""
	portalIndexUrl = "https://portal.trinity.edu.au/portal/today/today.php"  # the url of Portal index page
	basicInfoSuffixUrl = "https://portal.trinity.edu.au/portal/directory/directory.php?uid="  # suffix of the url of student's basic information page
	timetableSuffixUrl = "https://portal.trinity.edu.au/portal/sat/view_timetable.php?uid="  # suffix of the url of students's timetable page
	photoSuffixUrl = "https://portal.trinity.edu.au/portal/get_ldap_photo.php?" # suffix of the url of photos

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


	weekdays = ["mon", "tue", "wed", "thu", "fri"]
	periods = ["p1", "p2", "p3", "p4", "p5"]


