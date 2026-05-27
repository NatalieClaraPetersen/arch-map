"""Python AST parsing and import extraction."""
import ast
import os
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

    def module_name_to_file_path(self, module_name):
        """
        Convert module name to file path.
        e.g., zeeguu.core.model.user -> content/api/zeeguu/core/model/user.py
        """
        relative_path = module_name.replace(".", "/")

        # Check if it's a package (directory with __init__.py)
        package_path = os.path.join(self.code_root_folder, relative_path, "__init__.py")
        if os.path.exists(package_path):
            return package_path

        # Otherwise it's a regular module file
        return os.path.join(self.code_root_folder, relative_path + ".py")


class ImportExtractor:
    """Extracts imports from Python files using AST."""

    def __init__(self, converter: ModuleNameConverter):
        self.converter = converter
        
    def get_python_files(self):
        """Find all Python files in the repository."""
        path = Path(self.converter.code_root_folder)
        return sorted(path.rglob("*.py"))

    def extract_imports(self, file_path):
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
                            parts = file_path.split("/")
                            base = ".".join(parts[:len(parts) - node.level])
                            full_module = f"{base}.{node.module}"
                        else:
                            full_module = node.module
                        
                        module_path = self.converter.module_name_to_file_path(full_module)
                        if os.path.exists(module_path):
                            all_imports.append(full_module)
                        else:
                            continue
                        
                        for alias in node.names:
                            if alias.name != "*":
                                candidate = f"{full_module}.{alias.name}"
                                candidate_path = self.converter.module_name_to_file_path(candidate)
                                if os.path.exists(candidate_path):
                                    all_imports.append(candidate)

                # Handle 'import X' statements
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        module_path = self.converter.module_name_to_file_path(alias.name)
                        if os.path.exists(module_path):
                            all_imports.append(alias.name)
                
        except (SyntaxError, IOError, UnicodeDecodeError):
            # Return empty list if file can't be parsed
            pass
        
        return all_imports

    @staticmethod
    def get_n_level_module(module_name, n):
        """Extract top-level module from full module name e.g.: n=2, zeeguu.core.model -> zeeguu.core"""
        return ".".join(module_name.split(".")[:n])