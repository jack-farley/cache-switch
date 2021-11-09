from ipaddress import IPv4Network
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

    ipv4_src: IPv4Network

    def __init__(self, ipv4_src):
        self.ipv4_src = ipv4_src

    def matches(self, packet: Packet) -> bool:
        return packet.ipv4_src.subnet_of(self.ipv4_src)


class IPv4DstPattern (Pattern):

    ipv4_dst: IPv4Network

    def __init__(self, ipv4_dst):
        self.ipv4_dst = ipv4_dst

    def matches(self, packet: Packet) -> bool:
        return packet.ipv4_dst.subnet_of(self.ipv4_dst)


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
