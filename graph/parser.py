"""Python AST parsing and import extraction."""
import ast
from pathlib import Path


class ModuleNameConverter:
    """Converts file paths to module names."""
    
    def __init__(self, code_root_folder):
        self.code_root_folder = code_root_folder
    
    def file_path_to_module_name(self, full_path):
        """
        Convert file path to module name.
        e.g., content/api/zeeguu/core/model/user.py -> zeeguu.core.model.user
        """
        file_name = full_path[len(self.code_root_folder):]
        file_name = file_name.replace("/__init__.py", "")
        file_name = file_name.replace("/", ".")
        file_name = file_name.replace(".py", "")
        return file_name


class ImportExtractor:
    """Extracts imports from Python files using AST."""
    
    @staticmethod
    def extract_imports(file_path):
        """
        Extract all imported module names from a Python file using AST.
        
        Args:
            file_path: Path to a Python file
        
        Returns:
            List of imported module names
        """
        all_imports = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            # Walk the AST and find all import nodes
            for node in ast.walk(tree):
                # Handle 'from X import ...' statements
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        # Resolve relative import statements: 'from .X import ...'
                        if node.level > 0:
                            # level=1 is ".", level=2 is ".." etc.
                            parts = file_path.split(".")
                            base = ".".join(parts[:len(parts) - (node.level - 1)])
                            full_module = f"{base}.{node.module}"
                            continue
                        else:
                            full_module = node.module
                        all_imports.append(full_module)
                        
                        for alias in node.names:
                            if alias.name != "*":
                                all_imports.append(f"{node.module}.{alias.name}")
                
                # Handle 'import X' statements
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        all_imports.append(alias.name)
        
        except (SyntaxError, IOError, UnicodeDecodeError):
            # Return empty list if file can't be parsed
            pass
        
        return all_imports

    @staticmethod
    def get_n_level_module(module_name, n):
        """Extract top-level module from full module name eg.: n=2, zeeguu.core.model -> zeeguu.core"""
        return ".".join(module_name.split(".")[:n])