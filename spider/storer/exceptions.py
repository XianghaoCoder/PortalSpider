class ReadOnlyException(Exception):
	"""The file is read-only
	
	It will be raised when user try to alter a read pattern controller.	

	Attributes:
		path: the path of the read-only file.
	"""

	def __init__(self, path):
		self.path = path

	def __str__(self):
		return "It is read-only of: " + path + "."
