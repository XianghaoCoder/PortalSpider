from spider.storer.settings import Settings
from spider.storer.functions import write_data_json

class PortalStorer:
	"""A storer that can write information to local files.
	
	Attributes:
		__currentDirectory(private): a list of path representing the current directory where the storer is in.
	"""

	def __init__(self, isStudent):
		"""
		Args:
			isStudent: whether the information belongs to a student(True) or a teacher(False).
		"""

		if isStudent:
			self.__currentDirectory = [Settings.studentsDirectory]
		else:
			self.__currentDirectory = [Settings.teachersDirectory]

	def storePhoto(self, photo, name):
		"""Store a photo of a person.
			
		Args:
			photo: the content of the photo.
			name: the name of the person.
		"""

		self.toPhotoDirectory()
		path = self.getCurrentPath(name + ".jpeg")
		with open(path, "wb") as f:
			f.write(photo)

	def storeData(self, data, name):
		"""Store the data of a person in JSON form.
			
		Args:
			data: the data in dict form.
			name: the name of the person.
		"""

		self.toDataDirectory()
		path = self.getCurrentPath(name + ".json")
		write_data_json(data, path)

	def toDataDirectory(self):
		"""Change the cuurent directory to data directory.
		"""

		if len(self.__currentDirectory) == 2:
			self.__currentDirectory.pop()

		self.__currentDirectory.append(Settings.dataDirectory)

	def toPhotoDirectory(self):
		"""Change the cuurent directory to photos directory.
		"""
		if len(self.__currentDirectory) == 2:
			self.__currentDirectory.pop()

		self.__currentDirectory.append(Settings.photosDirectory)

	def getCurrentPath(self, fileName):
		"""Get the current the path of the file that will be created.
		
		Args:
			name: the name of the file.

		Returns:
			The current path of the file that will be created.
		"""

		path = ""
		for item in self.__currentDirectory:
			path += item
		path += fileName

		return path