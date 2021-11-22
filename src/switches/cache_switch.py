import logging
from sortedcontainers import SortedKeyList
from switches.switch import Switch
from switches.basic_switch import BasicSwitch
from rules.rule import Rule
from rules.action import Action, ActionType
from packet import Packet


class CacheSwitch (Switch):

    hw_switch: BasicSwitch
    hw_switch_size: int

    sw_switch: BasicSwitch

    all_rules: SortedKeyList

    def __init__(self, hw_switch_size: int):
        """Create a new cache switch."""
        logging.info("[cache_switch] Creating a new cache switch.")

        self.hw_switch = BasicSwitch()
        self.hw_switch_size = hw_switch_size

        self.sw_switch = BasicSwitch()

        # ascending order of priority - iterate in reverse
        self.all_rules = SortedKeyList([], key=lambda r: r.priority)

    def _construct_dependency_graph(self):
        """Construct the dependency graph."""
        logging.info("[cache_switch] Constructing the dependency graph.")

        # get a list of dependencies
        # dependency_graph[i] is the set of rules that i directly depends on
        dependency_graph = {}
        # all_dependencies[i] is the set of all rules that i depends on - if i
        # is cached these rules must also be cached
        all_dependencies = {}
        for i in reversed(range(len(self.all_rules))):
            i_depends_on = set()
            all_i_depends_on = set()
            for j in reversed(range(i + 1, len(self.all_rules))):
                # check if i depends on j
                if (self.all_rules[j].intersects(self.all_rules[i])):
                    i_depends_on.add(j)
                    all_i_depends_on.add(j)
                    all_i_depends_on.update(all_dependencies[j])
            dependency_graph[i] = i_depends_on
            all_dependencies[i] = all_i_depends_on

        return dependency_graph, all_dependencies

    def _get_weights(self):
        """Get the weights."""
        logging.info("[cache_switch] Getting weights.")

        weights = []
        for rule in self.all_rules:
            weights.append(rule.counter)
        return weights

    def update(self):
        """Update the rules in the hardware and software switches."""
        logging.info("[cache_switch] Updating cached rules.")

        dependency_graph, all_dependencies = self._construct_dependency_graph()
        # cost(i) = len(all_dependencies[i])

        weights = self._get_weights()

        # Heuristic for Budgeted Maximum Coverage Problem

        # In each stage we will choose a rule to add the maximizes the total
        # weight of the set to the combined rule cost.
        cached_rules = set()
        weight = -1

        while len(cached_rules) < self.hw_switch_size:
            to_add = set()
            weight_to_add = 0
            ratio = 0

            for i in range(len(self.all_rules)):
                if i not in cached_rules:
                    possible_to_add = {i}
                    possible_weight_to_add = weights[i]
                    for j in all_dependencies[i]:
                        if j not in cached_rules:
                            possible_to_add.add(j)
                            possible_weight_to_add += weights[j]

                    # make sure we haven't exceeded the cost
                    if (len(cached_rules) + len(to_add) > self.hw_switch_size):
                        continue

                    # check if this produces the best ratio so far
                    new_ratio = (weight + possible_weight_to_add) / \
                        (len(cached_rules) + len(possible_to_add))

                    if new_ratio > ratio:
                        to_add = possible_to_add
                        weight_to_add = possible_weight_to_add
                        ratio = new_ratio

            if ratio == 0:
                break

            # add the rules
            cached_rules.update(to_add)
            weight += weight_to_add

        # update the caches
        new_cache_rules = set()
        for ind in cached_rules:
            new_cache_rules.add(self.all_rules[ind])

        self.hw_switch.set_rules(new_cache_rules)

    def packet_in(self, packet: Packet, port: int) -> Action:
        logging.info("[cache_swtich] Cache switch received a packet.")

        packet.in_port = port

        # check if the packet matches in the hardware switch
        action = self.sw_switch.packet_in(packet)

        # check if we need to go to a software switch
        if action == None or action.type == ActionType.SOFTWARE_SWITCH:
            action = self.sw_switch.packet_in(packet)

        return action

    def add_rule(self, rule: Rule):
        logging.info("[cache_switch] Adding a rule to the cache_switch.")

        self.all_rules.add(rule)
        self.sw_switch.add_rule(rule)

        self.update()

    def remove_rule(self, rule: Rule):
        logging.info("[cache_switch] Removing a rule from the cache_switch.")

        self.all_rules.add(rule)
        self.sw_switch.remove_rule(rule)

        self.update()

    def set_rules(self, rules: set):
        logging.info("[cache_switch] Setting the rules for the cache switch.")

        # [TODO]
        pass
