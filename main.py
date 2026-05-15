"""Main entry point for dependency graph analysis."""
from graph.repository import RepositoryManager
from graph.graph import DependencyGraphBuilder
from graph.visualization import GraphVisualizer


def main():
    """Main entry point."""
    
    # Configuration
    REPO_URL = "https://github.com/zeeguu/api.git"
    CODE_ROOT_FOLDER = "content/api/"
    
    # Clone repository if needed
    RepositoryManager.clone_if_needed(REPO_URL, CODE_ROOT_FOLDER)
    RepositoryManager.pull(CODE_ROOT_FOLDER)
    
    # Build dependency graph
    print("\nBuilding dependency graph...")
    builder = DependencyGraphBuilder(CODE_ROOT_FOLDER, only_internal=False)
    folder_depth_from_root = 1
    G = builder.build(folder_depth_from_root)
    
    DependencyGraphBuilder.print_graph_stats(G)
    
    # Visualize
    print("\nGenerating visualization...")
    GraphVisualizer.draw_interactive(G)
    # GraphVisualizer.draw_static(G, size=(12, 8), node_size=10)


if __name__ == "__main__":
    main()
