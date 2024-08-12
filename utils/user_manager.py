
# Diccionario para almacenar el estado de cada usuario
user_states = {}

# Diccionario para almacenar otras informaciones, como el historial de conversación
user_chats = {}

def get_user_state(user_id):
    return user_states.get(user_id, None)

def set_user_state(user_id, state):
    user_states[user_id] = state

def clear_user_state(user_id):
    if user_id in user_states:
        del user_states[user_id]

def get_user_chat(user_id):
    return user_chats.get(user_id, [])

def add_user_chat(user_id, role, content):
    if user_id not in user_chats:
        user_chats[user_id] = []
    user_chats[user_id].append({"role": role, "content": content})

def clear_user_chat(user_id):
    if user_id in user_chats:
        del user_chats[user_id]
