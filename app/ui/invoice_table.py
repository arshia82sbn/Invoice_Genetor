import customtkinter as ctk
from typing import List
from app.utils.config import config
from app.utils.log_manager import get_logger

logger = get_logger()

class InvoiceTable(ctk.CTkFrame):
    """Custom scrollable table widget for invoice items"""

    def __init__(self, parent,**kwargs):
        super().__init__(parent, **kwargs)

        self.columns = ("Qty","Description","Price","Total")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the table UI components"""
        # Header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(pady=5,padx=5,fill="x")

        # Create header labels
        col_widths = config.get("ui.column_widths",{
            "qty" : 100,
            "description" : 300,
            "price" : 100,
            "total" : 100,
        })

        headers = [
            ("Qty",col_widths.get('qty',100)),
            ("Description",col_widths.get('description',300)),
            ("Price",col_widths.get('price',100)),
            ("Total",col_widths.get('total',100))
        ]
        for header_text , width in headers:
            label = ctk.CTkLabel(
                self.header_frame,
                text=header_text,
                width=width,
                anchor="center",
                font=("Arial", 14, "bold")
            )
            label.pack(padx=5,side="left")

        # Scrollable content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="left",fill="both",expand=True)

        # Canvas for scrolling
        self.canvas = ctk.CTkCanvas(
            self.content_frame,
                  bg="#2b2b2b",
                  highlightthickness=0
        )
        self.canvas.pack(side="left",fill="both",expand=True)

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.content_frame,
            orientation= "vertical",
            command=self.canvas.yview
        )
        self.scrollbar.pack(side="right",fill="y")

        # Scrollable frame inside canvas
        self.scrollable_frame = ctk.CTkFrame(self.canvas,fg_color="#2b2b2b")

        # Add scrollable frame to canvas
        self.canvas_window = self.canvas.create_window(
            (0,0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        # Configuration scrolling
        self.scrollable_frame.bind("<Configure>",self._on_frame_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind mousewheel for scrolling
        self.canvas.bind_all("<MouseWheel>",self._on_mousewheel)

    def _on_frame_configure(self,event=None):
        """Update scroll region when frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self,event):
        """Handle mouse wheel"""
        self.canvas.yview_scroll(-1 * (event.delta / 120), "units")

    def add_row(self,data: List):
        """
        Add a row of data to the table
        data: [qty, description, price, total]
        """
        row_frame = ctk.CTkFrame(self.scrollable_frame,fg_color="#333333")
        row_frame.pack(pady=2,padx=5,fill="x")

        col_widths = config.get("ui.column_widths",{
            "qty" : 100,
            "description" : 300,
            "price" : 100,
            "total" : 100
        })

        widths = [
            col_widths.get('qty',100),
            col_widths.get('description',300),
            col_widths.get('price',100),
            col_widths.get('total',100)
        ]

    def clear_rows(self):
        """Clear all rows from the table"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def update_table(self, items: List[List]):
        """
        Update the table with new data
        items: List of [qty, description, price, total]
        """
        self.clear_rows()
        for item in items:
            self.add_row(item)

    def get_row_count(self) -> int:
        """Get number of rows in the table"""
        return len(self.scrollable_frame.winfo_children())