def generate_get_request(name):
    """Generates request in json format to get address by client name"""
    request = {
        "command": "get",
        "name": name
    }

