"""
Interface module for connecting with external applications.
"""

class AppInterface:
    """Interface for external application integration."""
    
    def __init__(self, command_template, param_mapping, result_parser):
        self.command_template = command_template
        self.param_mapping = param_mapping
        self.result_parser = result_parser
    
    def build_command(self, params):
        """Build command line from parameters."""
        pass
    
    def execute(self, params):
        """Execute external application with given parameters."""
        pass
    
    def parse_results(self, output):
        """Parse results from application output."""
        pass