import json

def write_data_json(data, path):
	"""Write the data to a json file.

	Args:
		data: the data that will be written.
		path: the path of the file.
	"""

	with open(path, "w") as f:
		contents = json.dumps(data)
		f.write(contents)