import re
from typing import Tuple
from app.utils.log_manager import get_logger
from app.utils.config import config

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class validator:
    """Validator various types of input data"""

    @staticmethod
    def validate_name(name:str,field_name:str="Name")->Tuple[bool,str]:
        """
        Validate name fields (first name , last name)
        :return: (is_valid,error_message)
        """
        if not name or not name.strip():
            return False,"Name cannot be empty"

        if len(name.strip()) < 2:
            return False,"Name must have at least 2 characters"

        if not re.match(r"^[a-zA-Z\s-]+$",name):
            return False,"Name must contain only letters, numbers, hyphens and space "

        return True,""

    @staticmethod
    def validate_phone(phone:str)->Tuple[bool,str]:
        """
        Validate phone number
        :return: (is_valid,error_message)
        """
        if not phone or not phone.strip():
            return False,"Phone number cannot be empty"

        # Remove common separators
        cleaned_phone = re.sub(r"[\s\-\(\)]","",phone)

        if not cleaned_phone.isdigit():
             return False,"Phone number must be digit"

        max_length = config.get('validation.phone_max_length',10)
        if len(cleaned_phone) != max_length:
            return False,"Phone number must be of length {}".format(max_length)

        return True,""

    @staticmethod
    def validate_tax_rate(tax_str:str)->Tuple[bool,str]:
        pass