from .agent import default_agent

def get_msoko_response(user_message):
    """
    Get AI response from the professional MsokoAgent.
    """
    return default_agent.get_response(user_message)
