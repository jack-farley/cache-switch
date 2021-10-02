from ipaddress import ip_interface, IPv4Address


class Packet:

    in_port: int

    ipv4_src: IPv4Address
    ipv4_dst: IPv4Address

    tcp_sport: int
    tcp_dport: int

    def __init__(
        self,
        in_port: int,
        ipv4_src: IPv4Address,
        ipv4_dst: IPv4Address,
        tcp_sport: int,
        tcp_dport: int
    ):
        self.in_port = in_port
        self.ipv4_src = ipv4_src
        self.ipv4_dst = ipv4_dst
        self.tcp_sport = tcp_sport
        self.tcp_dport = tcp_dport
