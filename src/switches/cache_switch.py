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

    num_packets: int
    num_misses: int

    def __init__(self, hw_switch_size: int):
        """Create a new cache switch."""
        logging.info("[cache_switch] Creating a new cache switch.")

        self.hw_switch = BasicSwitch()
        self.hw_switch_size = hw_switch_size

        self.sw_switch = BasicSwitch()

        # ascending order of priority - iterate in reverse
        self.all_rules = SortedKeyList([], key=lambda r: r.priority)

        self.num_packets = 0
        self.num_misses = 0

    def _depends_on(self, a: int, b: int) -> bool:
        """
        Returns whether rule a depends on rule b. In other words, if a depends
        b, then if a is cached, b must also be cached.
        """
        # b must have a higher priority, thus must be greater
        if a >= b:
            return False

        return self.all_rules[a].intersects(self.all_rules[b])

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
                if self._depends_on(i, j):
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

    def _update_cache_dependent_set(self):
        """
        Updates the rules in the hardware switch cache using the dependent set
        algorithm as described in the paper. This update function uses a basic 
        algorithm that respects rule depencies but does not create new rules to 
        cover groups of rarely used ones. 
        """
        logging.info("[cache_switch] Updating cached rules - dependent set.")

        dependency_graph, all_dependencies = self._construct_dependency_graph()
        # cost(i) = len(all_dependencies[i])

        weights = self._get_weights()

        # Heuristic for Budgeted Maximum Coverage Problem

        # In each stage we will choose a rule to add the maximizes the total
        # weight of the set to the combined rule cost.
        cached_rules = set()
        weight = 0

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

    def _update_cache_cover_set(self):
        """
        This method updates the rules in the hardware switch cache using the 
        cover set algorithm as described in the paper. Unlike the dependent-set 
        algorithm, this algorithm does add new rules to the cache to cover 
        groups of rarely used rules. 
        """
        logging.info("[cache_switch] Updating cached rules, cover set.")

        dependency_graph, all_dependencies = self._construct_dependency_graph()
        # cost(i) = len(all_dependencies[i])

        weights = self._get_weights()

        # Cache rules using cover-set algorithm
        cached_rules = set()
        cover_rules = set()
        weight = 0

        while len(cached_rules) + len(cover_rules) < self.hw_switch_size:
            to_add_cached = set()
            to_remove_cover = set()
            to_add_cover = set()
            weight_to_add = 0

            for i in range(len(self.all_rules)):
                if i not in cached_rules and weights[i] > weight_to_add:
                    # create the cover set
                    possible_to_add_cached = set()
                    possible_to_remove_cover = set()
                    possible_to_add_cover = set()

                    possible_to_add_cached.add(i)
                    if i in cover_rules:
                        possible_to_remove_cover.add(i)
                    possible_to_add_cover.update(dependency_graph[i])

                    if len(cached_rules) + len(cover_rules) + len(possible_to_add_cached) \
                        - len(possible_to_remove_cover) + len(possible_to_add_cover) \
                            > self.hw_switch_size:
                        continue

                    to_add_cached = possible_to_add_cached
                    to_remove_cover = possible_to_remove_cover
                    to_add_cover = possible_to_add_cover
                    weight_to_add = weights[i]

            if weight_to_add == 0:
                break

            cached_rules.update(to_add_cached)
            cover_rules.difference_update(to_remove_cover)
            cover_rules.update(to_add_cover)
            weight += weight_to_add

        new_cache_rules = set()
        for ind in cached_rules:
            new_cache_rules.add(self.all_rules[ind])
        for ind in cover_rules:
            cover_rules.add(self.all_rules[ind].create_cover_rule())

        self.hw_switch.set_rules(new_cache_rules)

    def _update_cache_mixed_set(self):
        """
        This method updates the rules in the hardware switch cache using the 
        mixed set algorithm as described in the paper. This combines the use
        of cover rules from the cover-set algorithm with the greedy approach
        of the dependent-set algorithm to achieve an implementation that 
        attempts to capture the benefits of both algorithms. 
        """
        logging.info("[cache_switch] Updating cached rules, mixed set.")

        dependency_graph, all_dependencies = self._construct_dependency_graph()
        # cost(i) = len(all_dependencies[i])

        weights = self._get_weights()

        # Cache rules using mixed-set algorithm
        cached_rules = set()
        cover_rules = set()
        weight = 0

        while len(cached_rules) + len(cover_rules) < self.hw_switch_size:
            to_add_cached = set()
            to_remove_cover = set()
            to_add_cover = set()
            weight_to_add = 0
            ratio = 0

            for i in range(len(self.all_rules)):

                # dependent set part
                if i not in cached_rules:
                    # create dependent set
                    possible_to_add_cached = {i}
                    possible_to_remove_cover = set()
                    if i in cover_rules:
                        possible_to_remove_cover.add(i)
                    possible_to_add_cover = set()
                    possible_weight_to_add = weights[i]

                    for j in all_dependencies[i]:
                        if j not in cached_rules:
                            possible_to_add_cached.add(j)
                            if j in cover_rules:
                                possible_to_remove_cover.add(j)
                            possible_weight_to_add += weights[j]

                    # make sure we havent exceeded the cost
                    if len(cached_rules) + len(cover_rules) + len(possible_to_add_cached) - len(possible_to_remove_cover) + len(possible_to_add_cover) > self.hw_switch_size:
                        continue

                    new_ratio = (weight + possible_weight_to_add) / (len(cached_rules) + len(cover_rules) + len(
                        possible_to_add_cached) + len(possible_to_add_cover) - len(possible_to_remove_cover))

                    if new_ratio > ratio:
                        to_add_cached = possible_to_add_cached
                        to_remove_cover = possible_to_remove_cover
                        to_add_cover = possible_to_add_cover
                        weight_to_add = possible_weight_to_add
                        ratio = new_ratio

                # cover set part
                if i not in cached_rules:
                    # create the cover set
                    possible_to_add_cached = set()
                    possible_to_remove_cover = set()
                    possible_to_add_cover = set()
                    possible_weight_to_add = weights[i]

                    possible_to_add_cached.add(i)
                    if i in cover_rules:
                        possible_to_remove_cover.add(i)
                    possible_to_add_cover.update(dependency_graph[i])

                    # make sure we havent exceeded the cost
                    if len(cached_rules) + len(cover_rules) + len(possible_to_add_cached) - len(possible_to_remove_cover) + len(possible_to_add_cover) > self.hw_switch_size:
                        continue

                    new_ratio = (weight + possible_weight_to_add) / (len(cached_rules) + len(cover_rules) + len(
                        possible_to_add_cached) + len(possible_to_add_cover) - len(possible_to_remove_cover))

                    if new_ratio > ratio:
                        to_add_cached = possible_to_add_cached
                        to_remove_cover = possible_to_remove_cover
                        to_add_cover = possible_to_add_cover
                        weight_to_add = possible_weight_to_add
                        ratio = new_ratio

            if ratio == 0:
                break

            cached_rules.update(to_add_cached)
            cover_rules.difference_update(to_remove_cover)
            cover_rules.update(to_add_cover)
            weight += weight_to_add

        new_cache_rules = set()
        for ind in cached_rules:
            new_cache_rules.add(self.all_rules[ind])
        for ind in cover_rules:
            cover_rules.add(self.all_rules[ind].create_cover_rule())

        self.hw_switch.set_rules(new_cache_rules)

    def _update_cache(self):
        # [TODO] Add ability to use other cache algorithms.
        self._update_cache_dependent_set()

    def packet_in(self, packet: Packet, port: int) -> Action:
        logging.info("[cache_swtich] Cache switch received a packet.")

        packet.in_port = port

        # check if the packet matches in the hardware switch
        action = self.sw_switch.packet_in(packet)
        self.num_packets += 1

        # check if we need to go to a software switch
        if action == None or action.type == ActionType.SOFTWARE_SWITCH:
            action = self.sw_switch.packet_in(packet)
            self.num_misses += 1

        return action

    def add_rule(self, rule: Rule):
        logging.info("[cache_switch] Adding a rule to the cache_switch.")

        self.all_rules.add(rule)
        self.sw_switch.add_rule(rule)

        self._update_cache()

    def remove_rule(self, rule: Rule):
        logging.info("[cache_switch] Removing a rule from the cache_switch.")

        self.all_rules.add(rule)
        self.sw_switch.remove_rule(rule)

        self._update_cache()

    def set_rules(self, rules: set):
        logging.info("[cache_switch] Setting the rules for the cache switch.")

        # [TODO]
        pass
