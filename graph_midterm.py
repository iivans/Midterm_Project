# graph_midterm.py
from collections import deque
from api_code import get_movie_actors, get_actor_movies, get_actor_name

def build_graph_and_search_recursive(actor_id, target_actor_id, depth):

    print(f"Building co-star graph up to depth {depth} for actor ID {actor_id}.")
    
    # Graph to store actor connections
    graph = {}
    
    # Dictionary to store actor names
    actor_names = {}
    
    # Track visited actors to avoid reprocessing the same actors
    visited_actors = set()
    
    # Initialize the found flag
    found = False

    def recursive_build(current_actor_id, current_depth):
        nonlocal graph, found
        
        # Stop recursion if depth limit is exceeded or if the actor is already visited
        if current_depth > depth or current_actor_id in visited_actors:
            return None

        # Mark the actor as visited
        visited_actors.add(current_actor_id)

        # Store the actor name in the cache
        actor_names[current_actor_id] = get_actor_name(current_actor_id)

        # If the target actor is found, stop the search
        if current_actor_id == target_actor_id:
            print(f"Immediate connection found between {actor_names[actor_id]} and {actor_names[target_actor_id]}!")
            found = True
            return [current_actor_id]  # Return a direct path

        print(f"\nDepth {current_depth}: Getting co-stars for actor ID {current_actor_id}.")
        
        # Get movies for the current actor
        movies = get_actor_movies(current_actor_id)
        
        for movie in movies:
            #movie_title = movie.get('title', 'Unknown title')
            #print(f"\nProcessing movie: {movie_title} (Movie ID: {movie['id']})")

            # Get the list of actors in this movie
            actors = get_movie_actors(movie['id'])
            
            for actor in actors:
                # Cache actor name
                if actor['id'] not in actor_names:
                    actor_names[actor['id']] = actor['name']

                # Add this actor to the graph if not already present
                if actor['id'] not in graph:
                    graph[actor['id']] = set()

                # Link current actor with all co-stars
                for co_star in actors:
                    if co_star['id'] != actor['id']:
                        graph[actor['id']].add(co_star['id'])

                # Immediately check if the current co-star is the target
                if actor['id'] == target_actor_id:
                    print(f"Immediate connection found between {actor_names[actor_id]} and {actor_names[target_actor_id]}!")
                    found = True
                    return [current_actor_id, actor['id']]  # Return the co-star path immediately
                
                # Continue building the graph recursively for co-stars
                if current_depth < depth:
                    path = recursive_build(actor['id'], current_depth + 1)
                    
                    # If BFS found the target actor, return the path immediately
                    if path:
                        return [current_actor_id] + path

        return None

    # Start building the graph from the initial actor and search for the connection simultaneously
    path = recursive_build(actor_id, 1)

    return graph, actor_names, path, found



def visualize_graph(graph, actor_names):
    """Visualizes the co-star graph using NetworkX."""
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()

    for actor, co_stars in graph.items():
        G.add_node(actor)
        for co_star in co_stars:
            G.add_edge(actor, co_star)

    print("Running visual graph done")

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=False, node_size=50, node_color="lightblue", edge_color="gray", font_weight='bold')

    # Use the cached actor names
    nx.draw_networkx_labels(G, pos, labels=actor_names, font_size=10, font_color="black")

    plt.show()


