import logging
from ipaddress import IPv4Network
from network.switches.switch import Switch
from network.packet import Packet
from network.rules.action import ActionType


class Network:
    """
    Represents a network of hosts, switches, and links.
    This class also acts as the controller in the SDN model.
    """

    # switches[i] = switch with name i
    switches: dict

    # hosts[i] = ip_address
    hosts: dict

    # links[switch_name][switch_port] = dst_name, dst_port
    # if dst_port is None, then dst_name is a host
    links: dict

    # packet_queue[0] = packet, switch_name, switch_port
    # packet is waiting to enter switch_name on switch_port
    packet_queue: list

    packets_in: int
    packets_arrived: int
    packets_dropped: int

    def __init__(self):
        """Create a new netowrk."""
        self.switches = dict()
        self.hosts = dict()
        self.links = dict()
        self.packet_queue = []

        self.packets_in = 0
        self.packets_arrived = 0
        self.packets_dropped = 0

    def add_switch(self, switch_name: str, switch: Switch):
        """Add a switch to the network."""
        self.switches[switch_name] = switch
        self.links[switch_name] = dict()

    def add_host(self, host_name: str, ip_address: IPv4Network):
        """Add a host to the network."""
        self.hosts[host_name] = ip_address

    def connect_host(self, host_name: str, switch_name: str, switch_port: int):
        if host_name in self.hosts and switch_name in self.switches:
            self.links[host_name] = switch_name, switch_port
            self.links[switch_name][switch_port] = host_name, None

    def add_link(self, a: str, a_port: int, b: str, b_port: int):
        """Add a link to the network."""
        if a in self.switches and b in self.switches:
            self.links[a][a_port] = b, b_port
            self.links[b][b_port] = a, a_port

    def drop_packet(self, packet: Packet):
        """Drop a packet."""
        self.packets_dropped += 1

    def send_packet(self, host_name: str, tcp_sport: int, ipv4_dst: IPv4Network, tcp_dport: int):
        """Send a packet into the network."""

        self.packets_in += 1

        if host_name in self.hosts:
            packet = Packet(None, self.hosts[host_name],
                            ipv4_dst, tcp_sport, tcp_dport)
            switch_name, switch_port = self.links[host_name]
            self.packet_queue.append((packet, switch_name, switch_port))
        else:
            self.drop_packet

        while len(self.packet_queue) > 0:
            packet, switch_name, switch_port = self.packet_queue.pop()

            # packet has arrived at a switch
            if switch_port != None:
                packet.in_port = switch_port

                action = self.switches[switch_name].packet_in(
                    packet, switch_port)

                if action.type == ActionType.FORWARD:
                    src_port = action.forward_port
                    dst_switch, dst_port = self.links[switch_name][src_port]
                    self.packet_queue.append((packet, dst_switch, dst_port))

                elif action.type == ActionType.CONTROLLER:
                    self.packet_in(packet, switch_name)

                else:
                    self.drop_packet(packet)

            # packet has arrived at a host
            else:
                packet.in_port = None
                if switch_name in self.hosts and packet.ipv4_dst.subnet_of(self.hosts[switch_name]):
                    self.packets_arrived += 1
                else:
                    self.drop_packet(packet)

    def packet_in(self, packet: Packet, switch_name: str):
        """Handle a packet that has been sent to the controller."""
        self.drop_packet(packet)

    def get_stats(self):
        return self.packets_in, self.packets_arrived, self.packets_dropped
