from switches.switch import Switch
from packet import Packet
from rules.action import ActionType


class Network:

    # switches[i] = switch with name i
    switches: map

    # hosts[i] = switch_name, switch_port
    hosts: map

    # links[switch_name][switch_port] = dst_name, dst_port
    # if dst_port is None, then dst_name is a host
    links: map

    # packet_queue[0] = packet, switch_name, switch_port
    # packet is waiting to enter switch_name on switch_port
    packet_queue: list

    def __init__(self):
        """Create a new netowrk."""
        self.switches = map()
        self.hosts = map()
        self.links = map()
        self.packet_queue = []

    def add_switch(self, name: str, switch: Switch):
        """Add a switch to the network."""
        self.switches[name] = switch
        self.links[name] = map()

    def add_host(self, host_name: str, switch_name: str, switch_port):
        """Add a host to the network."""
        if switch_name in self.switches:
            self.hosts[host_name] = switch_name, switch_port
            self.links[switch_name][switch_port] = host_name, None

    def add_link(self, a: str, a_port: int, b: str, b_port: int):
        """Add a link to the network."""
        if a in self.switches and b in self.switches:
            self.links[a][a_port] = b, b_port
            self.links[b][b_port] = a, a_port

    def send_packet(self, packet: Packet, host_name: str):
        """Send a packet into the network."""
        if host_name in self.hosts:
            switch_name, switch_port = self.hosts[host_name]
            self.packet_queue.append(packet, switch_name, switch_port)

        while len(self.packet_queue) > 0:
            packet, switch_name, switch_port = self.packet_queue.popleft()

            action = self.switches[switch_name].packet_in(packet, switch_port)

            if action.type == ActionType.FORWARD:
                src_port = action.forward_port
                dst_switch, dst_port = self.links[switch_name, src_port]
                self.packet_queue.append(packet, dst_switch, dst_port)
