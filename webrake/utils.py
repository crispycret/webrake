from crispys_webkit.urls import LazyUrl

from crispys_webkit.objverify import is_type_of, is_int, is_str, is_list, is_dict 
from crispys_webkit.objverify import is_lazy_url, is_soup, is_response
from crispys_webkit.objverify import has_attr_of_type, has_soup, has_response, has_headers

from crispys_webkit.objextend import remove_non_ascii
from crispys_webkit.objextend import validate_attribute_name, add_attribute
from crispys_webkit.objextend import make_get_has_header_methods_for_obj_with_response


from crispys_webkit.objprope import get_methods_on_class
from crispys_webkit.objprope import get_class, get_class_name

