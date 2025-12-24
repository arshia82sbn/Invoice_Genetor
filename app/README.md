# Invoice Generator Pro 2.0

A professional invoice generation application built with Python, CustomTkinter, and following MVC design patterns.

## Features

- ✨ Modern, dark-themed UI with CustomTkinter
- 📝 Easy customer and item entry
- 🧮 Automatic calculations (subtotal, tax, total)
- 📄 Professional invoice document generation (DOCX)
- ✅ Comprehensive input validation
- 📊 Real-time invoice preview table
- 🔧 Configurable settings via JSON
- 📝 Detailed logging system
- 🏗️ Clean MVC architecture

## Project Structure

```
invoice_project/
├── assets/
│   └── templates/
│       └── invoice_template.docx    # Invoice template file
│
├── core/
│   ├── __init__.py
│   ├── invoice.py                   # Invoice business logic (Model)
│   └── validator.py                 # Input validation logic
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py               # Main application window
│   ├── invoice_form.py              # Form widgets
│   └── invoice_table.py             # Table display component
│
├── utils/
│   ├── __init__.py
│   ├── config.py                    # Configuration manager
│   └── log_manager.py               # Logging system
│
├── logs/                            # Generated log files
├── invoices/                        # Generated invoice files
├── old/                             # Original files (archived)
│
├── app.py                           # Application entry point (Controller)
├── config.json                      # Configuration settings
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Design Patterns Used

### 1. **MVC (Model-View-Controller)**
- **Model**: `core/invoice.py` - Business logic and data
- **View**: `ui/` folder - All UI components
- **Controller**: `app.py` - Coordinates Model and View

### 2. **Singleton Pattern**
- `ConfigManager` - Single configuration instance
- `LogManager` - Single logging instance

### 3. **Strategy Pattern**
- `Validator` - Multiple validation strategies

### 4. **Builder Pattern**
- `Invoice` class - Step-by-step invoice construction

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone or download the project**
```bash
cd invoice_project
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup template file**
- Place your `invoice_template.docx` in `assets/templates/`
- Or use the provided template

5. **Create required directories**
```bash
mkdir -p logs invoices
```

## Configuration

Edit `config.json` to customize:

- **Window settings**: Size, theme, title
- **Paths**: Template location, output directory
- **Validation rules**: Phone length, price limits
- **Invoice defaults**: Tax rate, currency, date format

## Usage

### Running the Application

```bash
python app.py
```

### Creating an Invoice

1. **Enter Customer Information**
   - First Name
   - Last Name
   - Phone (10 digits)

2. **Add Items**
   - Enter Quantity (use +/- buttons or type)
   - Enter Description
   - Enter Unit Price (use +/- buttons or type)
   - Click "Add Item"

3. **Set Tax Rate** (optional, defaults to 10%)

4. **Review Items** in the table

5. **Generate Invoice**
   - Click "Generate Invoice"
   - Invoice saved in `invoices/` folder

### Other Actions

- **New Invoice**: Clear all data and start fresh
- **Clear All Items**: Remove all items from current invoice

## Validation Rules

- **First/Last Name**: At least 2 characters, letters only
- **Phone**: Exactly 10 digits
- **Quantity**: Positive integer
- **Price**: Positive number, max $500
- **Description**: Not empty, max 200 characters
- **Tax Rate**: 0-100%

## Logging

Logs are saved in `logs/` folder with daily rotation:
- Format: `app_YYYYMMDD.log`
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Console output: INFO and above
- File output: DEBUG and above

## Troubleshooting

### Template Not Found
- Ensure `invoice_template.docx` is in `assets/templates/`
- Check path in `config.json`

### Permission Errors
- Ensure write permissions for `invoices/` and `logs/` directories

### Import Errors
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check virtual environment is activated

### UI Not Responding
- Check logs in `logs/` folder for errors
- Ensure all `__init__.py` files exist in module folders

## Extending the Application

### Adding New Validation Rules
Edit `core/validator.py` and add new validation methods.

### Customizing UI
Modify components in `ui/` folder:
- `invoice_form.py` - Form layout
- `invoice_table.py` - Table appearance
- `main_window.py` - Overall layout

### Changing Calculations
Edit `core/invoice.py` properties:
- `subtotal`
- `tax_amount`
- `total`

### Adding New Features
1. Add business logic to `core/`
2. Add UI components to `ui/`
3. Connect in `app.py` controller

## Code Quality

- **Type hints** throughout for better IDE support
- **Comprehensive docstrings** for all classes/methods
- **Error handling** with try-except blocks
- **Logging** for debugging and monitoring
- **Separation of concerns** - each module has single responsibility

## Version History

- **2.0.0** - Complete refactor with MVC pattern
  - Professional architecture
  - Comprehensive validation
  - Logging system
  - Configurable settings

- **1.0.0** - Original monolithic version

## License

This project is for educational/personal use.

## Support

For issues or questions:
1. Check logs in `logs/` folder
2. Review validation error messages
3. Ensure all dependencies are installed
4. Verify template file exists

## Future Enhancements

- [ ] Database integration for invoice history
- [ ] PDF export option
- [ ] Email invoice directly
- [ ] Multiple templates support
- [ ] Invoice editing/deletion
- [ ] Customer database
- [ ] Invoice search functionality
- [ ] Analytics dashboard

---

**Enjoy using Invoice Generator Pro!** 🎉