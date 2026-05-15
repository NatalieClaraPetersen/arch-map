from fnmatch import fnmatch
import networkx as nx


class ViewProjector:

    @staticmethod
    def project(graph, view_config):
        included_nodes = set()

        # Filter nodes
        for node in graph.nodes:
            if ViewProjector._matches_any(node, view_config.include):
                if not ViewProjector._matches_any(node, view_config.exclude):
                    included_nodes.add(node)

        subgraph = graph.subgraph(included_nodes).copy()

        # Apply grouping
        grouped_graph = ViewProjector._apply_groups(
            subgraph,
            view_config.groups,
        )
        
        return grouped_graph

    @staticmethod
    def _matches_any(value, patterns):
        return any(
            fnmatch(value, pattern)
            for pattern in patterns
        )
    
    @staticmethod
    def _apply_groups(graph, groups):
        grouped_graph = nx.DiGraph()
        node_to_group = {}

        # Map nodes to groups
        for group_name, patterns in groups.items():
            for node in graph.nodes:
                if ViewProjector._matches_any(node,patterns):
                    node_to_group[node] = group_name

        # Create nodes
        for node in graph.nodes:
            grouped_node = node_to_group.get(node,node)
            grouped_graph.add_node(grouped_node)

        # Reconnect edges
        for source, target in graph.edges:
            grouped_source = node_to_group.get(source,source)

            grouped_target = node_to_group.get(target,target)

            # avoid self-loop after collapsing
            if grouped_source != grouped_target:
                grouped_graph.add_edge(grouped_source,grouped_target)

        return grouped_graph