"""Dependency graph building."""
import networkx as nx
from pathlib import Path
from graph.parser import ModuleNameConverter, ImportExtractor


class DependencyGraphBuilder:
    """Builds a dependency graph from Python source code."""
    
    def __init__(self, code_root_folder, only_internal=False):
        self.only_internal = only_internal
        self.converter = ModuleNameConverter(code_root_folder)
        self.extractor = ImportExtractor(self.converter)
        self.internal_modules = set()
    
    def build(self):
        """Build the dependency graph."""
        python_files = self.extractor.get_python_files()
        G = nx.DiGraph()
        
        # First pass: add all nodes and collect internal modules
        for file in python_files:
            file_path = str(file)
            module_name = self.converter.file_path_to_module_name(file_path)
            self.internal_modules.add(module_name)
            G.add_node(module_name)
        
        # Second pass: add edges
        for file in python_files:
            file_path = str(file)
            module_name = self.converter.file_path_to_module_name(file_path)
            
            for imported_module in self.extractor.extract_imports(file_path):
                if (not self.only_internal) or (imported_module in self.internal_modules):
                    if module_name != imported_module:
                        G.add_edge(module_name, imported_module)
        
        return G
    
    def print_graph_stats(G):
        cycles = list(nx.simple_cycles(G))
        nodes_no_in = [n for n in G.nodes if G.in_degree(n) == 0]
        nodes_no_in_or_out = [n for n in G.nodes if G.in_degree(n) == 0 and G.out_degree(n) == 0]
        
        print(f"\nGraph Statistics:")
        print(f"  #Nodes: {G.number_of_nodes()}")
        print(f"  #Edges: {G.number_of_edges()}")
        print(f"  #Cycles: {len(cycles)}")
        print(f"  #Nodes never referenced: {len(nodes_no_in)}")
        print(f"  #Nodes no in and no out: {len(nodes_no_in_or_out)}")
