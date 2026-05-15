from fnmatch import fnmatch
import networkx as nx
from pathlib import Path

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
        grouped_graph = ViewProjector._apply_groups(subgraph, view_config.groups)
        if view_config.depth_config:
            grouped_graph = ViewProjector._apply_depth(grouped_graph, view_config.depth_config)

        return grouped_graph

    @staticmethod
    def _matches_any(value, patterns):
        return any(
            fnmatch(value, pattern)
            for pattern in patterns
        )
    
    @staticmethod
    def _apply_depth(graph, depth_config):
        root = depth_config["root"]
        depth = depth_config["depth"]
        groups = {}

        for node in graph.nodes:
            if not node.startswith(root):
                continue

            parts = node.split(".")
            group = ".".join(parts[:depth])
            groups.setdefault(group, []).append(node)
        
        return ViewProjector._apply_groups(graph, groups)
    
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

            if grouped_graph.has_node(grouped_node):
                grouped_graph.nodes[grouped_node]["count"] += 1
            else:
                grouped_graph.add_node(grouped_node, count=1)

        # Reconnect edges
        for source, target in graph.edges:
            grouped_source = node_to_group.get(source,source)
            grouped_target = node_to_group.get(target,target)

            if grouped_source != grouped_target:
                if grouped_graph.has_edge(grouped_source, grouped_target):
                    grouped_graph[grouped_source][grouped_target]["count"] += 1
                    grouped_graph[grouped_source][grouped_target]["label"] = str(grouped_graph[grouped_source][grouped_target]["count"])
                else:
                    grouped_graph.add_edge(
                        grouped_source,
                        grouped_target,
                        count=1,
                        label="1"
                    )
        return grouped_graph