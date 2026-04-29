from git import Repo
import os
import ast

CODE_ROOT_FOLDER="content/api/"

if not os.path.exists(CODE_ROOT_FOLDER):
    print("Started cloning into "+os.getcwd()+"/content/api ...")
    Repo.clone_from("https://github.com/zeeguu/api.git", CODE_ROOT_FOLDER)
    print("Finished cloning")
    
def file_path(file_name):
    return CODE_ROOT_FOLDER+file_name
assert (file_path("zeeguu/core/model/user.py") == "content/api/zeeguu/core/model/user.py")

def module_name_from_file_path(full_path):
    # e.g. ../core/model/user.py -> zeeguu.core.model.user
    file_name = full_path[len(CODE_ROOT_FOLDER):]
    file_name1 = file_name.replace("/__init__.py","")
    file_name2 = file_name1.replace("/",".")
    file_name3 = file_name2.replace(".py","")
    if file_name3 == "eguu":
        print(file_name,file_name1,file_name2,file_name3,"Full: ",full_path)
    return file_name3
assert 'zeeguu.core.model.user' == module_name_from_file_path(file_path('zeeguu/core/model/user.py'))
assert 'content.api.zeeguu' == module_name_from_file_path(file_path('content/api/zeeguu/__init__.py'))
print(module_name_from_file_path(file_path('content/api/zeeguu/__init__.py')))
# extracts all the imported modules from a file using AST
# returns a list of module names, e.g. ['zeeguu.core.model', 'flask', ...]
def imports_from_file(file):
    """
    Extract all imported modules from a Python file using AST.
    More efficient than line-by-line parsing since it parses the file once.
    
    Args:
        file: Path to a Python file
    
    Returns:
        List of imported module names
    """
    all_imports = []
    
    try:
        with open(file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        tree = ast.parse(source_code)
        
        # Walk the AST and find all import nodes
        for node in ast.walk(tree):
            # Handle 'from X import ...' statements
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    all_imports.append(node.module)
            
            # Handle 'import X' statements
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    all_imports.append(alias.name)
    
    except (SyntaxError, IOError, UnicodeDecodeError):
        # Return empty list if file can't be parsed
        pass
    
    return all_imports

# test
bookmark_imports = imports_from_file(file_path('zeeguu/core/model/bookmark.py'))
unique_code_imports =  imports_from_file(file_path('zeeguu/core/model/unique_code.py'))
print(bookmark_imports)
print(unique_code_imports)
assert(unique_code_imports != bookmark_imports)

import pathlib
from pathlib import Path
import networkx as nx

def dependencies_graph(code_root_folder, only_internal=False):
    files = Path(code_root_folder).rglob("*.py")

    G = nx.DiGraph()

    for file in files:
        file_path = str(file)
        module_name = module_name_from_file_path(file_path)
        
        # Group by first two parts (zeeguu.x)
        grouped_name = ".".join(module_name.split(".")[:1])

        if grouped_name not in G.nodes:
            G.add_node(grouped_name)

        for each in imports_from_file(file_path):
            # Only add if internal
            if only_internal:
                pass
            
            # Group imported module by first two parts (zeeguu.x)
            grouped_import = ".".join(each.split(".")[:1])

            if grouped_import not in G.nodes:
                G.add_node(grouped_import)
            
            if (grouped_name != grouped_import and module_name != grouped_name):
                G.add_edge(grouped_name, grouped_import)

    return G

import matplotlib.pyplot as plt

# a function to draw a graph
def draw_graph(G, size, node_size=300, **args):
    plt.figure(figsize=size)
    pos = nx.spring_layout(G, k=1.5, iterations=50)
    
    # Calculate node sizes based on degree (nodes used more are larger)
    node_degrees = dict(G.degree())
    max_degree = max(node_degrees.values()) if node_degrees else 1
    min_degree = min(node_degrees.values()) if node_degrees else 1
    
    # Scale node sizes between min_size and max_size
    min_size = 50
    max_size = 2000
    node_sizes = [min_size + (node_degrees[node] - min_degree) / (max_degree - min_degree) * (max_size - min_size) 
                  for node in G.nodes()]
    
    nx.draw(G, pos, node_size=node_sizes, arrows=True, arrowsize=10, alpha=0.8, **args)
    nx.draw_networkx_labels(G, pos, font_size=7)
    plt.margins(0.15)
    plt.show()
    
G = dependencies_graph(CODE_ROOT_FOLDER)
# print(G)
# print(G.nodes)
draw_graph(G, (12, 8), node_size=10)   # even smaller