import math
import numpy as np

from Graph import *
from node import *

class dStarLite:
    def __init__(self, graph, start, goal) -> None:
        """D* Lite algorithm initializer

        Args:
            graph (Graph): graph object
            start (string): staert node name
            goal (string): goal node name
        """
        self.graph = graph
        self.CLOSED = []
        self.OPEN = []
        self.start = start
        self.goal = goal
        self.OPEN.append(self.goal)

    def fill_min_action(self, _node):
        """find the minimum action from a given node

        Args:
            _node (node): node
        """
        _node.state_action.clear()

        min_action_cost = math.inf
        for s_name in self.graph.nodes:
            s = self.graph.nodes[s_name]

            if _node.name in s.parent:
                _node.state_action[s.name] = (s.parent[_node.name] + s.G)
                if min_action_cost > _node.state_action[s.name]:
                    min_action_cost = _node.state_action[s.name]
                    _node.min_action = s.name

    def fill_state_action(self, _node):
        """Fills action costs for all child nodes of a given node

        Args:
            _node (node): node
        """
        _node.state_action.clear()

        min_action_cost = math.inf
        for s_name in self.graph.nodes:
            s = self.graph.nodes[s_name]

            if _node.name in s.parent:
                _node.state_action[s.name] = (s.parent[_node.name] + s.G)
                if min_action_cost > _node.state_action[s.name]:
                    min_action_cost = _node.state_action[s.name]
                    _node.min_action = s.name


    def get_keys(self, _node):
        """Computes Key1 and Key2 for popping from open list

        Args:
            _node (node): node

        Returns:
            tuple: (key1, key2)
        """
        min_cost = min(_node.G, _node.rhs)
        return (min_cost+_node.C, min_cost)
    

    def check_open_list_min_key(self):
        """Returns the node with minimum key values in the open lsit

        Returns:
            string: node name
        """
        min_node  = self.start
        min_k1, min_k2 = self.get_keys(self.graph.nodes[self.start])

        lstK1 = []
        lstK2 = []
        for s in self.OPEN:
           K1, K2 =  self.get_keys(self.graph.nodes[s])
           lstK1.append(K1)
           lstK2.append(K2)

        if len(self.OPEN) > 0:
            open_min_k1 = min(lstK1)

            if lstK1.count(open_min_k1) > 1:
                open_min_k2 = min(lstK2)
                if lstK2.count(open_min_k2) == 1  and min_k2 > open_min_k2:
                    index = lstK2.index(open_min_k2)
                    min_node =  self.OPEN[index]
            else:
                if min_k1 > open_min_k1:
                    index = lstK1.index(open_min_k1)
                    min_node =  self.OPEN[index]
                elif min_k1 == open_min_k1:
                    open_min_k2 = min(lstK2)
                    if lstK2.count(open_min_k2) == 1  and min_k2 > open_min_k2:
                        index = lstK2.index(open_min_k2)
                        min_node =  self.OPEN[index]

        return min_node
            
        


    def updateState(self, _node):
        """Updates state of the given node

        Args:
            _node (node): node
        """
        # if _node.G == math.inf:
        #     _node.G = math.inf
        
        if _node.name != self.goal:
            self.fill_state_action(_node)
            _node.rhs = min(list(_node.state_action.values()))
        
        if _node.name in self.OPEN:
            self.OPEN.remove(_node.name)
        
        if _node.G != _node.rhs:
            if _node.name in self.CLOSED:
                self.CLOSED.remove(_node.name)
            self.OPEN.append(_node.name)

    def print_open_list(self):
        """Prints open list in a formated string
        """
        strOPEN = "[ "
        for s in self.OPEN:
            strOPEN += s
            strOPEN += ":"
            strOPEN += str(self.get_keys(self.graph.nodes[s]))
            strOPEN += ", "
        strOPEN += " ]"
        print(f"OPEN LIST : {strOPEN}")
    
    def compute_shortest_path(self):
        """Computes shotest path for D* lite
        """
        min_state = self.check_open_list_min_key()
        count = 0
        print(f"\n\nAlgorith started---------------------\n\n\n")
        while  min_state!= self.start or \
            self.graph.nodes[self.start].rhs != self.graph.nodes[self.start].G:
            count += 1

            self.print_open_list()
            self.OPEN.remove(min_state)
            if min_state not in self.CLOSED:
                self.CLOSED.append(min_state)
            print(f"ITERATION {count}")
            print(f"POP STATE : {min_state}")

            if self.graph.nodes[min_state].G > self.graph.nodes[min_state].rhs:
                self.graph.nodes[min_state].G = self.graph.nodes[min_state].rhs

                for s in self.graph.nodes[min_state].parent:
                    self.updateState(self.graph.nodes[s])

            else:
                self.graph.nodes[min_state].G = math.inf

                for s in self.graph.nodes[min_state].parent:
                    self.updateState(self.graph.nodes[s])

                self.updateState(self.graph.nodes[min_state])
            
            for s in self.graph.nodes:
                pretext = ""
                if s == min_state:
                    pretext = "->"
                if s in self.graph.nodes[min_state].parent:
                    pretext = "->"

                self.graph.nodes[s].print(pretext)
            self.print_open_list()
            print(f"CLOSED LIST : {self.CLOSED}")
            
            print("\n\n\n")



            min_state = self.check_open_list_min_key()


        print(f"Algorith completed---------------------")


    def back_track(self, start, goal):
        print(f"\n\nDiscovered Path---------------------\n")
        # for s in self.graph.nodes:
        #     self.fill_min_action(self.graph.nodes[s])

        s = start
        path = ""
        while s != goal:
            path += f"{s} -> "
            s = self.graph.nodes[s].min_action
        path+= goal
        print(path)
        print(f"\n\n------------------------------------")

    def run_dstar(self):
        """Continuously runs D* algorithm
        """
        while True:
            self.compute_shortest_path()
            self.back_track(self.start , self.goal)
            
            cost_updates = input("\n\nPlease enter edge updates (ex-format : x1,100,x2;x2,100,x3 ): ")

            for cost_update in cost_updates.split(";"):
                parent = cost_update.split(",")[0]
                cost = int(cost_update.split(",")[1])
                child = cost_update.split(",")[2]
                self.graph.nodes[child].parent[parent] = cost
                self.updateState(self.graph.nodes[parent])


if __name__ == "__main__":
    _graph = Graph()
    _dStarLite = dStarLite(_graph, _graph.start_node_name, _graph.goal_node_name)
    _dStarLite.run_dstar()

