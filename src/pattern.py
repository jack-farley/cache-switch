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
