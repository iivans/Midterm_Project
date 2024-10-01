# actor_search.py
from api_code import search_actor_by_name

def actor_search(flag):
    if flag == 'name':
        actor_name = input("Enter the actor's name: ")
        actor_id = search_actor_by_name(actor_name)
        if actor_id is None:
            raise ValueError(f"Actor '{actor_name}' not found.")
    elif flag == 'id':
        actor_id = int(input("Enter the actor's ID: "))
    else:
        raise ValueError("Invalid! Please choose either 'name' or 'id'.")
    return actor_id
