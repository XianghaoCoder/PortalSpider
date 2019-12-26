from spider.settings import Settings
from spider.exceptions import InvalidTimetableException


def parse_class_text(class_text):
	"""Get all properties of a class by parsing its raw text.

	If there is no class information in raw text, then return None.
	
	Args:
		class_text: the raw text will be parsed.

	Returns:
		a dict mapping names of properties of a class to contents of each property.
		e.g. {"class": "EAP 2G", "room": "VIC510", "teacher": "ABC", "time": "9:00am-10:00am"} 
	"""
	
	if class_text == "":  # if no any information, then return None means that there is no class
		return None

	data = dict()
	for key, value in Settings.classInfo.items():
		data[key] = find_prop(class_text, value)

	return data


def find_prop(class_text, prop_name):
	"""get a property from the raw text
		
	Args:
		class_text: the raw text
		prop_name: the name of the property

	Returns:
		string containing the content of the property
	"""

	begin = class_text.find(prop_name) + len(prop_name) + 2
	end = class_text.find("\n", begin)
	if end == -1:  # if the last line does not include \n, then the end should be the end of the whole text
		end = len(class_text)

	return class_text[begin:end]