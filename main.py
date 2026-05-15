"""Main entry point for dependency graph analysis."""
from graph.repository import RepositoryManager
from graph.graph import DependencyGraphBuilder
from graph.visualization import GraphVisualizer
from graph.config_loader import load_views_config
from graph.projector import ViewProjector

def main():
    """Main entry point."""
    # Load configuration
    config = load_views_config("architecture_views.yaml")
    
    # Clone repository if needed
    RepositoryManager.clone_if_needed(config.REPO_URL, config.CODE_ROOT_FOLDER)
    RepositoryManager.pull(config.CODE_ROOT_FOLDER)
    
    # Build dependency graph
    print("\nBuilding dependency graph...")
    builder = DependencyGraphBuilder(config.CODE_ROOT_FOLDER, only_internal=False)
    folder_depth_from_root = 1
    G = builder.build(folder_depth_from_root)
    
    # Visualize
    print("\nGenerating visualization...")
    for view in config.views:
        subgraph = ViewProjector.project(G,view)
        DependencyGraphBuilder.print_graph_stats(subgraph)
        GraphVisualizer.draw_interactive(subgraph)
    
    # GraphVisualizer.draw_static(G, size=(12, 8), node_size=10)


if __name__ == "__main__":
    main()
