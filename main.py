import sys
from selenium.common.exceptions import NoSuchWindowException

from spider.settings import Settings
from spider.exceptions import NoSuchPropertyException, InvalidTimetableException
from spider.portalDriver import PortalDriver
from spider.tools import get_name_list_from_file, delete_name_from_file, write_name_list_to_file, write_data_json, write_photo

names_left = None

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

def choose_name_list(portal_driver):
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
	isStudent = None

	paths = None
	directory = None
	if group_choice == "1":
		directory = Settings.studentsDirectory
		isStudent = True
		if file_choice == "1":
			path = Settings.studentsNamePath 
		else:
			path = Settings.studentsNameLeftPath
	else:
		directory = Settings.teachersDirectory
		isStudent = False
		if file_choice == "1":
			path = Settings.teachersNamePath
		else:
			path = Settings.teachersNameLeftPath

	name_list = get_name_list_from_file(path)
	if name_list == None:
		if group_choice == "1":
			path = Settings.studentsNamePath
		else:
			path = Settings.studentsNameLeftPath

		name_list = get_name_list_from_file(path) # choose another name list

		if file_choice != "1":
			print("Canont find 'names_left.txt', automatically choose 'names.txt' for you.")
		if file_choice == "1" or name_list == None:
			print("Cannot find 'names.txt', please put it under '" + directory + "' and restart this program.")
			endProgram(portal_driver)

	return (name_list, path, isStudent)

def collect_data(name_list, name_list_path, isStudent, portal_driver):
	if isStudent:
		directory_path = Settings.studentsDirectory
		info_list = Settings.defaultStudentBasicInfoList
	else:
		directory_path = Settings.teachersDirectory
		info_list = Settings.defaultTeacherBasicInfoList

	data_path = directory_path + Settings.dataDirectory
	photos_path = directory_path + Settings.photosDirectory
	names_left_path = directory_path + Settings.namesLeftFile

	count = 1
	names_left = name_list.copy()
	print("Start collecting information from Portal.")
	for name in name_list:
		print("Collecting information from " + name + "..... " + "(" + str(count) + "/" + str(len(name_list)) + ")")

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
				delete_name_from_file(name, directory_path + Settings.namesFile)
		except NoSuchWindowException:
			print("The Portal driver was closed accidently, the names of people not crawlled are in '" + names_left_path + "'.")
			write_name_list_to_file(names_left, names_left_path)
			endProgram(portal_driver)
		else:
			print("Finishing getting information from " + name + ".")
			write_data_json(data, data_path + name + ".json")
			write_photo(photo, photos_path + name + ".jpeg")

		names_left.remove(name)
		
		count += 1
	write_name_list_to_file(names_left, names_left_path)
	print("Finished.")

def endProgram(portal_driver):
	portal_driver.end()
	print("Portal driver is closed.")
	sys.exit(0)

def main():
	# log in
	welcome()
	print("Loading Portal driver.....")
	portal_driver = PortalDriver()
	log_in(portal_driver)

	# choose name list
	(name_list, name_list_path, isStudent) = choose_name_list(portal_driver)
	collect_data(name_list, name_list_path, isStudent, portal_driver)

	# close Portal driver
	endProgram(portal_driver)

main()