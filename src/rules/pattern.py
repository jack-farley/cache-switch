from ipaddress import IPv4Address
from packet import Packet


class Pattern:

    def matches(packet: Packet) -> bool:
        """Returns whether or not the packet matches this rule."""
        pass


class InPortPattern (Pattern):

    in_port: int

    def __init__(self, port: int):
        self.in_port = port

    def matches(self, packet: Packet) -> bool:
        return self.in_port == packet.in_port


class IPv4SrcPattern (Pattern):

    ipv4_src: IPv4Address

    def __init__(self, ipv4_src):
        self.ipv4_src = ipv4_src

    def matches(self, packet: Packet) -> bool:
        return self.ipv4_src.network.overlaps(packet.ipv4_src.network)


class IPv4DstPattern (Pattern):

    ipv4_dst: IPv4Address

    def __init__(self, ipv4_dst):
        self.ipv4_dst = ipv4_dst

    def matches(self, packet: Packet) -> bool:
        return self.ipv4_dst.network.overlaps(packet.ipv4_dst.network)


class TCPSPortPattern (Pattern):

    tcp_sport: int

    def __init__(self, tcp_sport):
        self.tcp_sport = tcp_sport

    def matches(self, packet: Packet) -> bool:
        return self.tcp_sport == packet.tcp_sport


class TCPDPortPattern (Pattern):

    tcp_dport: int

    def __init__(self, tcp_dport):
        self.tcp_dport = tcp_dport

    def matches(self, packet: Packet) -> bool:
        return self.tcp_dport == packet.tcp_dport
