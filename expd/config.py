"""
Configuration management for EXPD.
"""

import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path


class Config:
    """Configuration management for experiments."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.data = {}
        if config_path:
            self.load(config_path)
    
    def load(self, config_path: str) -> None:
        """Load configuration from YAML file."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key."""
        keys = key.split('.')
        data = self.data
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
    
    @property
    def experiment_name(self) -> str:
        """Get experiment name."""
        return self.get('experiment_name', 'default_experiment')
    
    @property
    def target_script(self) -> str:
        """Get target script path."""
        return self.get('target_script', 'target_script.py')
    
    @property
    def fixed_params(self) -> Dict[str, Any]:
        """Get fixed parameters."""
        return self.get('parameters.fixed_params', {})
    
    @property
    def grid_params(self) -> Dict[str, List[Any]]:
        """Get grid search parameters."""
        return self.get('parameters.grid_params', {})
    
    def save(self, config_path: Optional[str] = None) -> None:
        """Save configuration to YAML file."""
        path = config_path or self.config_path
        if not path:
            raise ValueError("No configuration path specified")
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, default_flow_style=False, allow_unicode=True)