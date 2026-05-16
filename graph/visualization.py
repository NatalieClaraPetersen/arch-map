"""Graph visualization utilities."""
import matplotlib.pyplot as plt
import networkx as nx


class GraphVisualizer:
    """Handles graph visualization with matplotlib and Pyvis."""

    @staticmethod
    def draw_interactive(G, output_dir="diagrams", output_file="dependency_graph.html"):
        """
        Draw graph using Pyvis (interactive).
        
        Args:
            G: NetworkX graph
            output_file: Output HTML file path
        """
        try:
            from pyvis.network import Network
            output_file_path=f"{output_dir}/{output_file}"
            
            net = Network(directed=True, notebook=False, height="750px", width="100%")
            net.from_nx(G)
            net.force_atlas_2based(overlap=0.01)
            # Configure physics for better spacing
            net.toggle_physics(True)
            net.show_buttons(filter_=True)
            
            # Calculate node sizes based on degree
            node_degrees = dict(G.degree())
            node_out_degrees = dict(G.out_degree()) if G.is_directed() else node_degrees
            node_in_degrees = dict(G.in_degree()) if G.is_directed() else node_degrees

            counts = [d["count"] for _, d in G.nodes(data=True)]
            min_count = min(counts)
            max_count = max(counts)

            for node in net.nodes:
                out_degree = node_out_degrees.get(node['id'], 0)
                in_degree = node_in_degrees.get(node['id'], 0)
                if out_degree == 0:
                    node['color'] = "#b1b1b1"
                
                # Set node size based on how many modules are grouped together in the node
                count = node['count']
                size = (
                    25 + (count - min_count) / (max_count - min_count) * 75
                    if max_count > min_count else 50
                )
                node['size'] = size
                
                group_count_str=""
                if count > 1:
                  group_count_str=f"\nModules grouped together: {count}"

                node['title'] = f"{node['id']}\nIndegree: {in_degree}\nOutdegree: {out_degree}{group_count_str}"
            
            print(f"Creating {output_file_path}...")
            net.write_html(output_file_path)
            print(f"Interactive graph saved to {output_file}")
            print("Open in browser to interact with the graph!")
        
        except ImportError:
            print("Error: Pyvis not installed. Install with: pip install pyvis")
            print("Falling back to static matplotlib visualization...")
        except Exception as e:
            print(f"Error creating interactive graph: {e}")
            print("Falling back to static matplotlib visualization...")

from pathlib import Path

def inject_bold_outgoing_edges(output_file):
    html = Path(output_file).read_text()
    extra_js = """
      var network = drawGraph();

      function resetEdgeStyles() {
        edges.forEach(function(edge) {
          edges.update({id: edge.id, width: 1, color: '#97c2fc'});
        });
      }

      function highlightIngoing(nodeId) {
        resetEdgeStyles();
        var outgoing = edges.get({
          filter: function(edge) {
            return edge.to === nodeId;
          }
        });
        outgoing.forEach(function(edge) {
          edges.update({id: edge.id, width: 5, color: 'red'});
        });
      }

      network.on("blurNode", function() {
        resetEdgeStyles();
      });

      network.on("click", function(params) {
        if (params.nodes.length === 0) {
          resetEdgeStyles();
        } else {
          highlightIngoing(params.nodes[0]);
        }
      });
    """
    html = html.replace("drawGraph();", extra_js)
    Path(output_file).write_text(html)