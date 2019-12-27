import sys

from spider.driver.portalDriver import PortalDriver
from functions import welcome, get_account_passward, log_in, choose_name_list_path, collect_data, endProgram

def main():
	# log in
	welcome()
	print("Loading Portal driver.....")
	portal_driver = PortalDriver()
	log_in(portal_driver)

	# choose name list
	name_list_path = choose_name_list_path(portal_driver)
	collect_data(name_list_path, portal_driver)

	# close Portal driver
	endProgram(portal_driver)

main()