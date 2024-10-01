# Midterm Project.py
from actor_search import actor_search
from graph_midterm import build_graph_and_search_recursive, visualize_graph
from api_code import get_actor_name

if __name__ == "__main__":
    try:
        # Keep prompting the user until a valid search method is provided
        while True:
            search_method = input("Do you want to search for actors by 'name' or 'id'? ").strip().lower()

            if search_method in ['name', 'id']:
                break
            else:
                print("Invalid input! Please enter 'name' or 'id'.")

        # Search for actor 1 and actor 2
        actor1_id = actor_search(search_method)
        actor2_id = actor_search(search_method)

        # User-specified depth for co-star retrieval
        depth = int(input("Enter the depth of co-star retrieval (1 for direct co-stars, 2 for co-stars of co-stars, etc.): "))

        # Build the graph and search for the connection
        actor_graph, actor_names, path, found = build_graph_and_search_recursive(actor1_id, actor2_id, depth)

        if found:
            print(f"Shortest path between actors: {[actor_names[actor] for actor in path]}")
        else:
            print(f"No connection found between the two actors within depth {depth}.")
            exit()

        # Visualize the graph using cached actor names
        #visualize_graph(actor_graph, actor_names)

    except Exception as e:
        print(f"An error occurred: {e}")
        exit()
