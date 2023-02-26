def generate_get_request(name):
    """Generates request in json format to get address by client name"""
    request = {
        "command": "get",
        "name": name
    }
    return request

def generate_put_request(in_host, in_port, out_host, out_port, name):
    """Generates request in json format to put data to signal server"""
    request = {
        "command": "put",
        "addresses": {
            "in": {
                "host": in_host,
                "port": in_port
            },
            "out": {
                "host": out_host,
                "port": out_port
            }
        },
        "name": name
    }
    return request