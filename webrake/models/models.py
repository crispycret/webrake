import csv


def excel_to_csv(excel_model):
	tmp_dict = excel_model.excel_to_dict()
	csv_model = CSVModel()
	csv_model.dict_to_csv(tmp_dict)
	return csv_model

def csv_to_excel(csv_model):
	tmp_dict = csv_model.csv_to_dict()
	excel_model = ExcelModel()
	excel_model.dict_to_excel(tmp_dict)
	return excel_model

class ExcelModel(object):
	def load_excel(self):pass
	def save_excel(self):pass
	def dict_to_excel(self):pass
	def excel_to_dict(self):pass

class CSVModel(object):
	def load_csv(self):pass
	def save_csv(self):pass
	def dict_to_csv(self):
		""" 
		the the dictionary keys will be the 
		The key of the dictionary will be the first column in
		the csv file 
		"""
		
	def csv_to_dict(self):
		""" 
		The first column in the csv is the key, the following 
		columns are the values that are to be placed in a list.
		If the csv file has a header column then instead of using
		a list, use a dictionary with the header names as keys.
		"""
		pass

def format_data(data_obj, sep='::'):
	""" 
	format the data_obj into with the given delimter.
	HELP: https://en.wikipedia.org/wiki/Delimiter-separated_values
	"""
	VALID_SEPERATORS = ('::', ',', ':')




class BaseData(object):

	field_names = []
	format_order = []


