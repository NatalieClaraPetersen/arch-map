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
