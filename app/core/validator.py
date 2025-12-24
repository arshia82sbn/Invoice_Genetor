import re
from typing import Tuple
from app.utils.log_manager import get_logger
from app.utils.config import config

logger = get_logger()

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class Validator:
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
        logger.info(f"Phone number: {phone}")

        # Remove common separators
        cleaned_phone = re.sub(r"[\s\-\(\)]","",phone)

        if not cleaned_phone.isdigit():
             return False,"Phone number must be digit"

        max_length = config.get('validation.phone_max_length',10)
        if len(cleaned_phone) != max_length:
            return False,"Phone number must be of length {}".format(max_length)
        logger.info(f"Phone number: {cleaned_phone}")
        return True,""

    @staticmethod
    def validate_tax_rate(tax_str:str)->Tuple[bool,float,str]:
        """
        Validate tax rate
        :return: (is_valid,tax_valid,error_message)
        """
        if not tax_str or not tax_str.strip():
            default_tax = config.default_tax_rate
            logger.info(f"Using tax rate is {default_tax}")

            return True,default_tax,""

        try:
            tax_value = float(tax_str)

            if tax_value < 0:
                return False,0,"Tax rate cannot be negative"

            if tax_value > 100:
                return False,0,"Tax rate cannot be greater than 100"

            return True,tax_value,""

        except ValueError:
            return False,0,"Tax rate must be valid number"

    @staticmethod
    def validate_quantity(qty_str:str)->Tuple[bool,int,str]:
        """
        Validate quantity
        :return: (is_valid,quantity_value,error_message)
        """
        try:
            qty = int(qty_str)

            qty_min = config.get('validation.qty_min',0)
            if qty <= qty_min:
                return False , 0,f"Quantity must  be greater than {qty_min}"

            return True,qty,""

        except ValueError:
            return False, 0,"Quantity must be valid integer"

    @staticmethod
    def validate_price(price_str:str)->Tuple[bool,float,str]:
        """
        Validate price
        :return: (is_valid,price_value,error_message)
        """
        try:
            price = float(price_str)
            if price <= 0:
                return False,0.0,"Price must be positive number"

            price_max = config.get('validation.price_max',10000.0)
            if price > price_max:
                return False,0.0,"Price must be less than {}".format(price_max)

            return True,round(price,2),""

        except ValueError:
            return False, 0.0,"Price must be valid number"

    @staticmethod
    def validate_description(desc:str)->Tuple[bool,str] :
        """
        Validate description
        :return: (is_valid,error_message)
        """
        if not desc or not desc.strip():
            return False,"Description cannot be empty"

        max_length = config.get('validation.description_max_length',200)
        if len(desc.strip()) > max_length:
                return False,"Description must be longer than {}".format(max_length)
        return True,""

    @staticmethod
    def validate_invoice_item(qty_str:str,desc:str,price_str:str)->Tuple[bool,dict,str]:
        """
        Validate complete invoice item
        :return: (is_valid,item_dict,error_message)
        """
        # Validate quantity
        is_valid,qty,error = Validator.validate_quantity(qty_str)
        if not is_valid:
            return False,{},error

        # Validate price
        is_valid ,price ,error = Validator.validate_price(price_str)
        if not is_valid:
            return False,{},error

        # Validate description
        is_valid ,error = Validator.validate_description(desc)
        if not is_valid:
            return False,{},error

        # Calculate line total
        line_total = round(qty*price,2)

        item = {
            "quantity" : qty,
            "price" : price,
            "description" : desc,
            "total" : line_total,
        }

        return True, item, ""

    @staticmethod
    def validate_invoice_data(
            first_name:str,
            last_name:str,
            phone:str,
            invoice_items:list)->Tuple[bool,str]:
        """
        Validate complete invoice data before generation
        :return: (is_valid,error_message)
        """

        # Validate first name
        is_valid,error_message = Validator.validate_name(first_name,"First name")
        if not is_valid:
            return False,error_message

        # Validate last name
        is_valid,error_message = Validator.validate_name(last_name,"Last name")
        if not is_valid:
            return False,error_message

        # Validate phone number
        is_valid, error_message = Validator.validate_phone(phone)
        if not is_valid:
            return False,error_message

        # Validate invoice items
        if not invoice_items or len(invoice_items)==0:
            return False,"Invoice items cannot be empty"

        return True, ""
