"""Graph visualization utilities."""
import matplotlib.pyplot as plt
import networkx as nx


class GraphVisualizer:
    """Handles graph visualization with matplotlib and Pyvis."""
    
    @staticmethod
    def draw_static(G, size=(12, 8), node_size=10, **args):
        """
        Draw graph using matplotlib (static).
        
        Args:
            G: NetworkX graph
            size: Figure size tuple
            node_size: Base node size parameter
            **args: Additional arguments to nx.draw()
        """
        plt.figure(figsize=size)
        pos = nx.spring_layout(G, k=1.5, iterations=50)
        
        # Calculate node sizes based on degree
        node_degrees = dict(G.degree())
        max_degree = max(node_degrees.values()) if node_degrees else 1
        min_degree = min(node_degrees.values()) if node_degrees else 1
        
        min_size = 50
        max_size = 2000
        node_sizes = [min_size + (node_degrees[node] - min_degree) / (max_degree - min_degree) * (max_size - min_size) 
                      for node in G.nodes()]
        
        nx.draw(G, pos, node_size=node_sizes, arrows=True, arrowsize=10, alpha=0.8, **args)
        nx.draw_networkx_labels(G, pos, font_size=7)
        plt.margins(0.15)
        plt.show()
    
    @staticmethod
    def draw_interactive(G, output_file="dependency_graph.html"):
        """
        Draw graph using Pyvis (interactive).
        
        Args:
            G: NetworkX graph
            output_file: Output HTML file path
        """
        try:
            from pyvis.network import Network
            
            net = Network(directed=True, notebook=False, height="750px", width="100%")
            net.from_nx(G)
            net.force_atlas_2based()
            # Configure physics for better spacing
            net.toggle_physics(True)
            net.show_buttons(filter_=True)
            
            # Calculate node sizes based on degree
            node_degrees = dict(G.degree())
            node_out_degrees = dict(G.out_degree()) if G.is_directed() else node_degrees
            node_in_degrees = dict(G.in_degree()) if G.is_directed() else node_degrees
            max_degree = max(node_degrees.values()) if node_degrees else 1
            min_degree = min(node_degrees.values()) if node_degrees else 1
            
            for node in net.nodes:
                degree = node_degrees.get(node['id'], 0)
                out_degree = node_out_degrees.get(node['id'], 0)
                in_degree = node_in_degrees.get(node['id'], 0)
                size = 25 + (degree - min_degree) / (max_degree - min_degree) * 75 if max_degree > min_degree else 50
                node['size'] = size
                if out_degree == 0:
                    node['color'] = 'gray'
                node['title'] = f"{node['id']}\nIndegree: {in_degree}\nOutdegree: {out_degree}"
            
            print(f"Creating {output_file}...")
            net.write_html(output_file)
            print(f"Interactive graph saved to {output_file}")
            print("Open in browser to interact with the graph!")
        
        except ImportError:
            print("Error: Pyvis not installed. Install with: pip install pyvis")
            print("Falling back to static matplotlib visualization...")
        except Exception as e:
            print(f"Error creating interactive graph: {e}")
            print("Falling back to static matplotlib visualization...")
