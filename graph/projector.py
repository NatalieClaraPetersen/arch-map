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

        # Apply depth
        if view_config.depth_config:
            subgraph = ViewProjector._apply_depth(subgraph, view_config.depth_config)
        
        # Apply groups
        if view_config.groups:
            subgraph = ViewProjector._apply_groups(subgraph, view_config.groups)

        # MVP reflexion model
        if view_config.allowed_edges_to:
            subgraph = ViewProjector._detect_unallowed_edges(subgraph, view_config.allowed_edges_to)
        
        return subgraph

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
            if (not node.startswith(root)) and root != '*':
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
            existing_count = graph.nodes[node].get("count", 1) # if not previously grouped default to 1
            if grouped_graph.has_node(grouped_node):
                grouped_graph.nodes[grouped_node]["count"] += existing_count
            else:
                grouped_graph.add_node(grouped_node, count=existing_count)

        # Reconnect edges
        for source, target in graph.edges:
            grouped_source = node_to_group.get(source,source)
            grouped_target = node_to_group.get(target,target)

            if grouped_source != grouped_target:
                existing_edge_count = graph[source][target].get("count", 1) # if not previously grouped default to 1
                if grouped_graph.has_edge(grouped_source, grouped_target):
                    grouped_graph[grouped_source][grouped_target]["count"] += existing_edge_count
                else:
                    grouped_graph.add_edge(
                        grouped_source,
                        grouped_target,
                        count=existing_edge_count,
                    )
        return grouped_graph
    
    @staticmethod
    def _detect_unallowed_edges(graph, allowed_edges_to):
        for source, target in graph.edges:
            allowed_targets = None
            for pattern, targets in allowed_edges_to.items():
                if ViewProjector._matches_any(source, [pattern]):
                    allowed_targets = targets
                    break

            if allowed_targets is None:
                # no allowed_edges_to rule specified for this node
                continue

            is_allowed = ViewProjector._matches_any(target, allowed_targets)
            if not is_allowed:
                graph[source][target]["forbidden"] = True
            else:
                graph[source][target]["forbidden"] = False

        return graph