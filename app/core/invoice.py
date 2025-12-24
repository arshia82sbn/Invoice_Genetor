import os
import datetime as dt
from typing import List, Dict, Optional
from docxtpl import DocxTemplate

from app.utils.config import config
from app.utils.log_manager import get_logger
from app.core.validator import Validator

logger = get_logger()

class InvoiceItem:
    "Represents an invoice item in an invoice document"

    def __init__(self,qty:int,decs:str,price:float):
        self.qty = qty
        self.decs = decs
        self.price = price
        self.total = round (qty * price,2)

    def to_dict(self) -> Dict:
        """Convert item to dictionary for template"""
        return {
            'qty': self.qty,
            'decs': self.decs,
            'price': self.price,
            'total': self.total,
        }

    def to_list(self) -> List[Dict]:
        """Convert item to list for template"""
        return [self.qty,self.decs,self.price,self.total]

    def __repr__(self):
        return f"InvoiceItem(qty={self.qty}, desc={self.decs}, price={self.price}, total={self.total})"

class Invoice:
    """
    Main Invoice class - handles all invoice operations
    Uses builder pattern for construction
    """
    def __init__(self):
        self.first_name: str = " "
        self.last_name: str = " "
        self.phone: str = " "
        self.tax_rate: float = config.default_tax_rate
        self.items: List[InvoiceItem] = []

        logger.info("New invoice created")

    @property
    def customer_name(self) -> str:
        """Get full customer name"""
        return self.first_name.strip() + " " + self.last_name.strip()

    @property
    def subtotal(self) -> float:
        """Calculate subtotal of all items"""
        return round(sum(item.total for item in self.items),2)

    @property
    def tax_amount(self) -> float:
        """Calculate tax amount"""
        return round(self.subtotal * self.tax_amount,2)

    def set_customer_info(self, first_name: str, last_name: str, phone: str):
        """Set customer information"""
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.phone = phone.strip()
        logger.debug(f"Customer info set: {first_name}-{last_name}-{phone}")

    def set_tax_rate(self,tax_rate: float):
        """Set tax rate"""
        self.tax_rate = tax_rate
        logger.debug(f"Tax rate set: {tax_rate}%")

    def add_item(self,qty:int,desc:str,price:float)->InvoiceItem:
        """Add an item to the invoice"""
        item = InvoiceItem(qty,desc,price)
        self.items.append(item)
        logger.info(f"Invoice item added: {item}")
        return item

    def remove_item(self,index:int)->bool:
        """Remove an item by index"""
        try:
            removed_item = self.items.pop(index)
            logger.info(f"Invoice item removed: {removed_item}")
            return True
        except IndexError:
            logger.error(f"Failed to remove item at indexs: {index}")
            return False

    def clear_items(self):
        """Clear all items"""
        count = len(self.items)
        self.items.clear()
        logger.info(f"Cleared {count} items")

    def reset(self):
        """Reset invoice to initial state"""
        self.first_name = " "
        self.last_name = " "
        self.phone = " "
        self.tax_rate = config.default_tax_rate
        self.items.clear()
        logger.info(f"Reset invoice to initial state")

    def validate(self) -> tuple[bool,str]:
        """Validate invoice date"""
        return Validator.validate_invoice_data(
            self.first_name,
            self.last_name,
            self.phone,
            self.items
        )

    def get_items_as_dict(self) -> List[dict]:
        """Get all items as dictionary for template"""
        return [items.to_dict() for items in self.items]

    def get_items_as_lists(self) -> List[list]:
        """Get all items as list for template"""
        return [item.to_list() for item in self.items]

    def generate_document(
            self,template_name:str = "invoice_template.docx")->tuple[bool,str,str]:
        """
        Generate invoice document
        :return: (success,file_name,error_message)
        """
        try:
            # Validate invoice data
            is_valid ,error = self.validate()
            if not is_valid:
                logger.error(f"Failed to validate invoice document: {error}")
                return False,"", error

            # Get template path
            template_path = config.get_template_path(template_name)

            if not os.path.exsits(template_path):
                error_msg = f"template {template_name} does not exist"
                logger.error(f"Failed to generate invoice document: {template_path}")
                logger.error(error_msg)
                return False,"",error_msg

            # Load template
            doc = DocxTemplate(template_path)

            # Prepare data for template
            context = {
                "name" : self.customer_name,
                "phone" : self.phone,
                "invoice_list": self.get_items_as_dict(),
                "subtotal" : self.subtotal,
                "salestax" : f"{self.tax_amount}%",
                "tax_amount" : self.tax_amount,
                "total" : self.subtotal,
                "date": dt.datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
            }

            # Render document
            doc.render(context)

            # Generate filename
            timestamp = dt.datetime.strftime(config.get("invoice.date_format","%Y-%m-%d:%H:%M:%S"))
            filename = f"Invoice_{self.customer_name.replace(' ','_')}_{timestamp}.docx"

            # Get output directory
            output_dir = config.get_output_dir()
            filepath = os.path.join(output_dir,filename)

            # Save document
            doc.save(filepath)

            logger.info(f"Invoice document saved successfully: {filepath}")
            return True,filename,""

        except Exception as e:
            error_msg = f"Failed to generate invoice document: {e}"
            logger.error(f"Failed to generate invoice document: {str(e)}")
            return False,"",error_msg

    def __repr__(self):
        return (f"Invoice(customer='{self.customer_name}', "
                f"items={len(self.items)}, total={self.subtotal})")