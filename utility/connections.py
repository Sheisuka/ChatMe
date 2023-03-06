import stun


def set_out_address():
    nat_type, out_host, out_port = stun.get_ip_info()
    return out_host, out_port
    