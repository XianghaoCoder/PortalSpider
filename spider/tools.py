import requests
import json

def download_photo(url):
	"""Download a photo from the url, then store it in a variable and return this variable.

	Args:
		url: the url of this photo

	Returns:
		the content of the photo,
		if cannot find this url, then return None
	"""

	image = requests.get(url)
	if image.status_code == 200:
		return image.content
	else:
		return None

def write_photo(photo, path):
	"""Write the content of a photo to a specified path.
		
	Args:
		photo: the content of the photo will be written.
		path: the path that will store this photo.
	"""

	with open(path, "wb") as f:
		f.write(photo)

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

def write_data_json(data, path):
	"""Write the data to a json file.

	Args:
		data: the data that will be written.
		path: the path of the file.
	"""

	with open(path, "w") as f:
		contents = json.dumps(data)
		f.write(contents)
