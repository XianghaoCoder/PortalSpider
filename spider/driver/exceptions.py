class NoSuchPropertyException(Exception):
	"""Cannot find a property in basic information of a person.

	Attributes:
		propertyName: the name of the property that cannot be found.
	"""

	def __init__(self, propertyName):
		self.propertyName = propertyName

	def __str__(self):
		return "Cannot find a property named: " + self.propertyName + "."

class InvalidTimetableException(Exception):
	"""Cannot find the timetable of a person.

	Attributes:
		name: the name of the person
	"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "Cannot read the timetable of: " + self.name + "."

class NotLoggedInPortalException(Exception):
	"""Portal is not logged in.
		
	"""

	def __str__(self):
		return "Not logged in Portal now."
