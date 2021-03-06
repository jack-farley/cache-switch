from ipaddress import IPv4Network


class Packet:

    in_port: int

    ipv4_src: IPv4Network
    ipv4_dst: IPv4Network

    tcp_sport: int
    tcp_dport: int

    def __init__(
        self,
        in_port: int,
        ipv4_src: IPv4Network,
        ipv4_dst: IPv4Network,
        tcp_sport: int,
        tcp_dport: int
    ):
        self.in_port = in_port
        self.ipv4_src = ipv4_src
        self.ipv4_dst = ipv4_dst
        self.tcp_sport = tcp_sport
        self.tcp_dport = tcp_dport

    def __str__(self):
        return f'[in_port: {self.in_port}, ipv4_src: {str(self.ipv4_src)}, ipv4_dst: {str(self.ipv4_dst)}, tcp_sport: {self.tcp_sport}, tcp_dport: {self.tcp_dport}]'
