"""
Application Controller - MVC Controller Layer
Coordinates between UI (View) and Business Logic (Model)
Entry point for the application
"""
import sys
from app.ui.main_window import MainWindow
from app.core.invoice import Invoice
from app.core.validator import Validator
from app.utils.config import config
from app.utils.log_manager import get_logger

logger = get_logger()

class InvoiceController:
    """
    Main application controller
    Implements MVC pattern - coordinates between View and Model
    """

    def __init__(self):
        # Model
        self.invoice = Invoice()

        # View
        self.window = MainWindow()

        # Connect UI callbacks to controller methods
        self._connect_callbacks()

        logger.info("Invoice Controller initialized")

    def _connect_callbacks(self):
        """Connect UI events to controller methods"""
        # Form callbacks
        self.window.invoice_form.on_add_item = self.handle_add_item

        # Button callbacks
        self.window.generate_btn.configure(command=self.handle_generate_invoice)
        self.window.new_invoice_btn.configure(command=self.handle_new_invoice)
        self.window.clear_items_btn.configure(command=self.handle_clear_items)

        logger.debug("UI callbacks connected")

    def handle_add_item(self):
        """Handle add item action"""
        try:
            # Get data from form
            item_data = self.window.invoice_form.get_item_data()

            # Validate item data
            is_valid, item_dict, error = Validator.validate_invoice_item(
                item_data['qty'],
                item_data['desc'],
                item_data['price']
            )

            if not is_valid:
                self.window.show_error("Validation Error", error)
                logger.warning(f"Item validation failed: {error}")
                return

            # Add item to invoice model
            self.invoice.add_item(
                item_dict['qty'],
                item_dict['desc'],
                item_dict['price']
            )

            # Update table view
            self._refresh_table()

            # Update summary
            self._refresh_summary()

            # Clear item fields
            self.window.invoice_form.clear_item_fields()

            # Show success message
            self.window.show_success("Success", "Item added successfully!")

            logger.info(f"Item added: {item_dict}")

        except Exception as e:
            error_msg = f"Failed to add item: {str(e)}"
            self.window.show_error("Error", error_msg)
            logger.error(error_msg, exc_info=True)

    def handle_generate_invoice(self):
        """Handle generate invoice action"""
        try:
            # Get customer data from form
            customer_data = self.window.invoice_form.get_customer_data()

            # Set customer info in invoice
            self.invoice.set_customer_info(
                customer_data['first_name'],
                customer_data['last_name'],
                customer_data['phone']
            )

            # Get and set tax rate
            tax_str = self.window.invoice_form.get_tax_rate()
            is_valid, tax_value, error = Validator.validate_tax_rate(tax_str)

            if not is_valid:
                self.window.show_error("Validation Error", error)
                return

            self.invoice.set_tax_rate(tax_value)

            # Generate invoice document
            success, filename, error = self.invoice.generate_document()

            if success:
                self.window.show_success(
                    "Success",
                    f"Invoice generated successfully!\n\nSaved as: {filename}"
                )
                logger.info(f"Invoice generated: {filename}")
            else:
                self.window.show_error("Error", f"Failed to generate invoice:\n{error}")
                logger.error(f"Invoice generation failed: {error}")

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.window.show_error("Error", error_msg)
            logger.error(error_msg, exc_info=True)

    def handle_new_invoice(self):
        """Handle new invoice action"""
        try:
            # Confirm if there are items
            if len(self.invoice.items) > 0:
                confirmed = self.window.confirm_action(
                    "New Invoice",
                    "Are you sure you want to create a new invoice?\n"
                    "All current data will be cleared."
                )

                if not confirmed:
                    return

            # Reset invoice model
            self.invoice.reset()

            # Clear all form fields
            self.window.invoice_form.clear_all_fields()

            # Clear table
            self.window.invoice_table.clear_rows()

            # Reset summary
            self._refresh_summary()

            self.window.show_info("New Invoice", "Ready for new invoice")
            logger.info("New invoice started")

        except Exception as e:
            error_msg = f"Failed to create new invoice: {str(e)}"
            self.window.show_error("Error", error_msg)
            logger.error(error_msg, exc_info=True)

    def handle_clear_items(self):
        """Handle clear all items action"""
        try:
            if len(self.invoice.items) == 0:
                self.window.show_info("Info", "No items to clear")
                return

            # Confirm action
            confirmed = self.window.confirm_action(
                "Clear Items",
                f"Are you sure you want to clear all {len(self.invoice.items)} items?"
            )

            if not confirmed:
                return

            # Clear items from model
            self.invoice.clear_items()

            # Clear table view
            self.window.invoice_table.clear_rows()

            # Update summary
            self._refresh_summary()

            self.window.show_success("Success", "All items cleared")
            logger.info("All items cleared")

        except Exception as e:
            error_msg = f"Failed to clear items: {str(e)}"
            self.window.show_error("Error", error_msg)
            logger.error(error_msg, exc_info=True)

    def _refresh_table(self):
        """Refresh table display with current invoice items"""
        items = self.invoice.get_items_as_lists()
        self.window.invoice_table.update_table(items)

    def _refresh_summary(self):
        """Refresh summary display with current totals"""
        # Get tax rate from form for calculation
        tax_str = self.window.invoice_form.get_tax_rate()
        is_valid, tax_value, _ = Validator.validate_tax_rate(tax_str)

        if is_valid:
            self.invoice.set_tax_rate(tax_value)

        self.window.update_summary(
            self.invoice.subtotal,
            self.invoice.tax_amount,
            self.invoice.total
        )

    def run(self):
        """Start the application"""
        logger.info("Application started")
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.critical(f"Application crashed: {str(e)}", exc_info=True)
            raise
        finally:
            logger.info("Application closed")


def main():
    """Main entry point"""
    try:
        # Create and run controller
        controller = InvoiceController()
        controller.run()
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()