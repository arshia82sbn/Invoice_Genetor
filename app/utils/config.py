import json
import os
from app.utils.log_manager import get_logger

logger = get_logger()

class ConfigManager:
    """Class to manage application configuration settings."""
    _instance = None
    _config = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self.load_config()

    def load_config(self,config_path="config.json"):
        """Load application configuration settings from json file."""
        try:
            with open(config_path, encoding="utf-8") as f:
                logger.debug("Loading application configuration settings from {}".format(config_path))
                self._config = json.load(f)
        except FileNotFoundError:
            # Default configuration if file not loaded
            logger.error("Configuration file not found.")
            self._config = {
                "app": {
                    "title": "Invoice Generator Pro",
                    "window_size": "1000x800",
                    "theme": "dark"
                },
                "paths": {
                    "template_dir": "assets/templates",
                    "output_dir": "invoice",
                },
                "invoice": {
                    "default_tax-rate":10.0
                }
            }
    def get(self,key_path,default=None):
        """
        Get configuration value using not notation
        """
        keys = key_path.split(".")
        value = self._config

        for key in keys:
            if isinstance(value,dict) and key in value:
                value = value[key]
            else:
                default

        return value

    def get_template_path(self,template_name="invoice_template.docx"):
        """Get full path template file"""
        template_dir = self.get("paths.template_dir","assets/templates")
        return os.path.join(template_dir,template_name)

    def get_output_dir(self):
        """Get full path output directory"""
        output_dir = self.get("paths.output_dir")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    @property
    def app_title(self):
        return self.get("app.title","Invoice Generator Pro")

    @property
    def window_size(self):
        return self.get("app.window_size","1000x800")

    @property
    def theme(self):
        return self.get("app.theme","dark")

    @property
    def default_tax_rate(self):
        return self.get("invoice.default_tax-rate",10.0)

config = ConfigManager()