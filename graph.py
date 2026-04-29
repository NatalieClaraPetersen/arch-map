"""Dependency graph building."""
import networkx as nx
from pathlib import Path
from parser import ModuleNameConverter, ImportExtractor


class DependencyGraphBuilder:
    """Builds a dependency graph from Python source code."""
    
    def __init__(self, code_root_folder, only_internal=False):
        self.code_root_folder = code_root_folder
        self.only_internal = only_internal
        self.converter = ModuleNameConverter(code_root_folder)
        self.extractor = ImportExtractor()
        self.internal_modules = set()
    
    def build(self):
        """Build the dependency graph."""
        files = list(Path(self.code_root_folder).rglob("*.py"))
        
        G = nx.DiGraph()
        
        # First pass: add all nodes and collect internal modules
        for file in files:
            file_path = str(file)
            module_name = self.converter.file_path_to_module_name(file_path)
            grouped_name = self._get_top_level_module(module_name)
            self.internal_modules.add(grouped_name)
            
            if grouped_name not in G.nodes:
                G.add_node(grouped_name)
        
        # Second pass: add edges
        for file in files:
            file_path = str(file)
            module_name = self.converter.file_path_to_module_name(file_path)
            grouped_name = self._get_top_level_module(module_name)
            
            for imported_module in self.extractor.extract_imports(file_path):
                grouped_import = self._get_top_level_module(imported_module)
                
                if grouped_import not in G.nodes:
                    G.add_node(grouped_import)
                
                # Only add edge if not filtering for internal, or if the import is internal
                if not self.only_internal or grouped_import in self.internal_modules:
                    if grouped_name != grouped_import:
                        G.add_edge(grouped_name, grouped_import)
        
        return G
    
    @staticmethod
    def _get_top_level_module(module_name):
        """Extract top-level module from full module name."""
        return ".".join(module_name.split(".")[:1])
