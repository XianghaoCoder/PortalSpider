import sys
from selenium.common.exceptions import NoSuchWindowException

from configs import Configures
from spider.storer.portalStorer import PortalStorer
from spider.driver.exceptions import NoSuchPropertyException, InvalidTimetableException

def welcome():
	print("==========================================================================")
	print("=   This is a spider that can collect information from Trinity Portal.   =")
	print("=   This program is for study and reference.                             =")
	print("=   Author: Xianghao Wang                                                =")
	print("==========================================================================")	

def get_account_passward():
	print("Please input your information.")
	account = input("Account: ")
	passward = input("Passward: ")

	return (account, passward)

def log_in(portal_driver):
	while True:
		(account, passward) = get_account_passward()
		print("Logging in Portal.....")
		portal_driver.logIn(account, passward)

		if portal_driver.isLoggedIn():
			print("Log in Portal successfully.")
			return

		print("Wrong acoount or passward, please try again.")

def is_file_available(path):
	try:
		with open(path, "r") as f:
			return True
	except FileNotFoundError:
		return False

def choose_name_list_path(portal_driver):
	# choose a group
	print("Please choose a group whose inforation you want to collect.")
	print("===================================================================")
	print("=====          (1) Student    (2 or else) Teacher             =====")
	print("===================================================================")
	group_choice = input("Your selection: ")

	# choose a file
	print("Please choose which file you would like to use.")
	print("===================================================================")
	print("=====        (1) names.txt    (2 or else) names_left.txt      =====")
	print("===================================================================")
	file_choice = input("Your selection: ")

	if group_choice == "1":
		paths = [Configures.namesDirectories["students"], None]
	else:
		paths = [Configures.namesDirectories["teachers"], None]

	if file_choice != "1":
		paths[1] = Configures.namesLeftFile
		if is_file_available(paths[0] + paths[1]):
			return paths[0] + paths[1]
		else:
			print("Canont find 'names_left.txt', automatically choose 'names.txt' for you.")

	paths[1] = Configures.namesFile
	if is_file_available(paths[0] + paths[1]):
		return paths[0] + paths[1]
	else:
		print("Cannot find 'names.txt', please put it under '" + paths[0] + "' and restart this program.")
		endProgram(portal_driver)

def collect_data(name_list_path, portal_driver):
	if Configures.namesDirectories["students"] in name_list_path:
		isStudent = True
		info_list = Configures.defaultStudentBasicInfoList
	else:
		isStudent = False
		info_list = Configures.defaultTeacherBasicInfoList

	portal_storer = PortalStorer(isStudent)

	names_left_path = name_list_path.replace(Configures.namesFile, Configures.namesLeftFile)
	names = get_name_list_from_file(name_list_path)
	names_left = names.copy()  # contain names of persons not crawlled

	count = 1
	print("Start collecting information from Portal.")
	for name in names:
		print("Collecting information from " + name + "..... " + "(" + str(count) + "/" + str(len(names)) + ")")

		try:
			(data, photo) = portal_driver.getData(name, info_list)
		except (NoSuchPropertyException, InvalidTimetableException):
			print("There is some prolem when collecting information from " + name + ", ")
			print("This person's information may be not available, ")
			print("would you like to delete this name from name list file?")
			print("===================================================================")
			print("=====           (1) Yes             (2 or else) No            =====")
			print("===================================================================")

			choice = input("Your selection: ")

			if choice == "1":
				delete_name_from_file(name, names_left_path.replace(Configures.namesLeftFile, Configures.namesFile))
		except NoSuchWindowException:
			print("The Portal driver was closed accidently, the names of people not crawlled are in '" + names_left_path + "'.")
			write_name_list_to_file(names_left, names_left_path)
			endProgram(portal_driver)
		else:
			print("Finishing getting information from " + name + ".")
			portal_storer.storeData(data, name)
			portal_storer.storePhoto(photo, name)

		names_left.remove(name)
		count += 1

	write_name_list_to_file(names_left, names_left_path)
	print("Finished.")


def endProgram(portal_driver):
	portal_driver.end()
	print("Portal driver is closed.")
	sys.exit(0)

def get_name_list_from_file(path):
	"""Get a list of names from a file.

	If cannot find the file, return None.

	Args:
		path: the path of the file.

	Returns:
		a list of names
	"""
	name_list = []
	try:
		with open(path, "r") as f:
			for line in f:
				name = line.strip()
				name_list.append(name)
	except FileNotFoundError as e:
		return None

	return name_list

def write_name_list_to_file(name_list, path):
	"""Write name list to a file
	
	Args:
		path: the path of the file.
		name_list: the name list that will be stored to the file.
	"""

	with open(path, "w") as f:
		for name in name_list:
			f.write(name + "\n")

def delete_name_from_file(name, path):
	"""Delete a name from the file storing name list.
	
	Args:
		name: the name that will be deleted.
		path: the path of the file
	"""

	name_list = get_name_list_from_file(path)
	name_list.remove(name)
	write_name_list_to_file(name_list, path)