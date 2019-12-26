from selenium import webdriver
import requests

from spider.settings import Settings
from spider.exceptions import NoSuchPropertyException, InvalidTimetableException, NotLoggedInPortalException
from spider.functions import parse_class_text
from spider.tools import download_photo

class PortalDriver:
	"""A webdriver that is able to manipulate the Portal websites.
	
	Attributes:
		driver: A webdriver for Chrome controlling the browser.
	"""
	def __init__(self):
		self.driver = webdriver.Chrome()

	def isLoggedIn(self):
		"""Judge whether user has logged in Portal.

		Returns:
			a boolean incicating whether Portal is logged in.
		"""

		not_logged_sign = "Log in"
		logged_sign = self.driver.find_elements_by_class_name("loggedInAs")
		logged_sign = [item.text for item in logged_sign]

		if not_logged_sign in logged_sign or logged_sign == []:
			return False
		else:
			return True


	def logIn(self, account, passward):
		"""Log in Portal with an account and a passward
		   
		This method will open the index page of Portal first,
		and then input account and passward. At last, submit this
		information by clicking button.
		Note that this method does not make sure logging is successful,
		user should use isLoggedIn() method to check.

		Args:
			account: the account needed.
			passward: the passward needed.
		"""

		# open Portal index
		self.driver.get(Settings.portalIndexUrl)

		# log in
		login = self.driver.find_element_by_id("login")
		passwd = self.driver.find_element_by_id("passwd")
		submit_button = self.driver.find_element_by_name("sent")
		login.send_keys(account)
		passwd.send_keys(passward)
		submit_button.click()


	def getData(self, name, infoList=Settings.defaultStudentBasicInfoList):
		"""Get data including basic information, photo and timetable of a stuent from Portal.

		Exceptions will be raised if the name in infoList is not a property of basic information, 
		or timetable cannot be found, or Portal is not logged in.
		This method checks whether Portal is logged in first.

		Args:
			name: the name of the peroson whose data will be collected.
			infoList: the names of basic information thatwill be collected.
				e.g. ["firstName", "lastName", "intake"]

		Returns:
			the dict mapping names of each information to contents of it.
				e.g. {"firstName": "Alan", "lastName": "Smith", "timetable": ...}
			the content of a photo of this person.

	
		Raises:
			NoSuchPropertyException: A propery cannot be found.
			InvalidTimetableException: The timetable cannot be found.
			NotLoggedInPortalException: Portal is not logged in.
		"""
		photo = self.getPhoto(name)
		basic_info = self.getBasicInfo(name, infoList)
		timetable = {"timetable": self.getTimetable(name)}
		data = dict(list(basic_info.items()) + list(timetable.items()))

		return (data, photo)

	def getPhoto(self, name):
		"""Get the photo of a person

		Args:
			name: the name of the person

		Returns:
			if getting the photo, return the content of the photo,
			otherwise, return None
		"""

		photo = download_photo(Settings.photoSuffixUrl + name)
		return photo

	def getBasicInfo(self, name, infoList=Settings.defaultStudentBasicInfoList):
		"""Get basic information except timetable of a peroson from Portal.

		This method will jump to the basic information page of a peroson, and collect data from it.
		Exception will be raise if the name in infoList is not a property, or Portal is not logged in.
		This method checks whether Portal is logged in first.

		Args:
			name: the name of the peroson whose basic information will be collected.
			infoList: the names of basic information thatwill be collected.
				e.g. ["firstName", "lastName", "intake"]

		Returns:
			the dict mapping names of each property except timetable to contents of them.
				e.g. {"firstName": "Alan", "lastName": "Smith", "PreferredName": "Alan"}

		Raises:
			NoSuchPropertyException: A propery cannot be found.
			NotLoggedInPortalException: Portal is not logged in.

		"""

		self.toBasicInfoPage(name)  # jump to the basic information page

		keys = list()
		values = list()

		rows_head = self.driver.find_elements_by_class_name("rowhead")
		rows_content = self.driver.find_elements_by_xpath("//td[@class='rowhead']/following-sibling::td[1]")

		for item in rows_head:
			keys.append(item.text[:-1])  # to leave out :
		for item in rows_content:
			values.append(item.text)
		rows = dict(zip(keys, values))

		items = dict()
		for info_name in infoList:
			info_name_text = Settings.infoMap[info_name]
			# if no such a property, then raise an exception
			if info_name_text not in rows:
				raise NoSuchPropertyException(info_name)

			items[info_name] = rows[info_name_text]

		return items


	def getTimetable(self, name):
		"""Get the timetable of a peroson from Portal.

		This method will jump to the timetable page of a peroson, and collect data from it.
		Exception will be raise if timetable cannot be found, or Portal is not logged in.
		This method checks whether Portal is logged in first.

		Args:
			name: the name of the peroson whose timetable will be collected.

		Returns:
			the dict mapping each weekday to another dict mapping each period to contents of each class
				e.g. {"mon": {"p1": {"teacher": "...", ...}, ...}, ...}

		Raises:
			InvalidTimetableException: The timetable cannot be found.
			NotLoggedInPortalException: Portal is not logged in.

		"""

		self.toTimetablePage(name) # jump to the timetable page

		classes_map = dict() # initalize the dict mapping each time to the content of each classes
		for weekday in Settings.weekdays:
			classes_map[weekday] = dict()
			for period in Settings.periods:
				classes_map[weekday][period] = None

		raw_classes = self.driver.find_elements_by_xpath("//table[@summary='SAT timetable']/tbody/tr/td")  # get raw text of all classes  
		raw_classes = [item.text.strip() for item in raw_classes]  # simplify the raw text
		raw_classes = raw_classes[int(len(raw_classes)/2):]  # to leave out classes in the former timetable that has no useful information
		classes_list = [parse_class_text(item) for item in raw_classes]  # parse raw text to get information of all classes

		# if the number of classes is not equal to that it should have,
		# then this timetable is invalid
		if len(classes_list) != len(Settings.weekdays) * len(Settings.periods):
			raise InvalidTimetableException(name)

		# put the list information of each classes into a dictionary
		count = 0
		for period in Settings.periods:
			for weekday in Settings.weekdays:
				classes_map[weekday][period] = classes_list[count]
				count += 1

		return classes_map

	def toBasicInfoPage(self, name):
		"""Jump to the basic information page of a peroson.

		Make sure that Portal is logged in, otherwise an exception will be raised.

		Raises:
			NotLoggedInPortalException: Portal is not logged in.
		"""

		if not self.isLoggedIn():
			raise NotLoggedInPortalException

		self.driver.get(Settings.basicInfoSuffixUrl + name)

	def toTimetablePage(self, name):
		"""Jump to the timetable page of a peroson.

		Make sure that Portal is logged in, otherwise an exception will be raised.

		Raises:
			NotLoggedInPortalException: Portal is not logged in.
		"""

		if not self.isLoggedIn():
			raise NotLoggedInPortalException

		self.driver.get(Settings.timetableSuffixUrl + name)

	def end(self):
		"""Close the Portal driver.

			Please do not use Portal driver after calling this method.
		"""
		self.driver.quit()