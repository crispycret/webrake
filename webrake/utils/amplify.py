
from .thirdparty import slugify


def validate_attribute_name(name):
	""" Modify a string to become a valid/legal lower case attribute """
	name = slugify(name).replace('-', '_')
	return name


def add_attribute(cls, attr_name, attr_value):
	""" Add a valid attribute name to a class and set the attribute value """
	attr_name = validate_attribute_name(attr_name)
	setattr(cls, attr_name, attr_value)



