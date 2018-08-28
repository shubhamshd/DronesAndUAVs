from square import square
from board import board
import math
import sys

class search(object):

    closedset = set()
    openset = set()
    came_from = {} # the next step back up the path from [node]
    g_score = {} # current path cost from the start node to [node]
    f_score = {} # estimated path cost from [node] to the goal node
    theboard = ""

    def __init__(self,startx,starty,endx,endy):

        i = 0
        for sq in self.run(startx,starty,endx,endy):
            self.theboard.squares[sq.x][sq.y].state = '*'
            i = i + 1
        print self.theboard

    def __str__(self):
        return self.theboard        


    def run(self,startx,starty,endx,endy):
        """ Run the search """

        # setup board
        path = 'boards/board20obs.txt'
        length = 20
        height = 20
        self.theboard = board(path,length,height,startx,starty,endx,endy)
        print self.theboard
        start = self.theboard.start
        goal = self.theboard.goal

        # initialise start node
        self.g_score[start] = 0
        self.f_score[start] = self.g_score[start] + self.heuristic_cost_estimate(start,goal)
        self.openset.add(start)

        while self.count(self.openset) > 0:
            # while we still have nodes left to evaluate

            # pick the next node to evaluate as the one we estimate has the shortest path cost to reach the goal node
            # that hasn't already been evaluated
            f_score_sorted = sorted(self.f_score, key=lambda square: self.g_score[square] + self.heuristic_cost_estimate(square,goal))
            i = 0
            for i in range(len(f_score_sorted)-1):
                if(f_score_sorted[i] not in self.closedset):
                    break

            current = f_score_sorted[i]

            if current == goal:
                return self.reconstruct_path(goal)

            try:
                self.openset.remove(current)
            except KeyError,e:
                pass

            self.closedset.add(current)
            for neighbour in self.neighbour_nodes(current):
                if neighbour not in self.closedset:
          
                    temp_g_score = self.g_score[current] + 1
                    if (neighbour not in self.openset) or (temp_g_score < self.g_score[neighbour]): 
                        # if the neighbour node has not yet been evaluated yet, then we evaluate it
                        # or, if we have just found a shorter way to reach neighbour from the start node, 
                        # then we replace the previous route to get to neighbour, with this new quicker route
                        self.came_from[neighbour] = current
                        self.g_score[neighbour] = temp_g_score
                        self.f_score[neighbour] = self.g_score[neighbour] + self.heuristic_cost_estimate(neighbour,goal)
            
                        if neighbour not in self.openset:
                            self.openset.add(neighbour)
        
      
        print "Reached the end of nodes to expand, failure"       


    def neighbour_nodes(self,node):
        """ Generate a set of neighbouring nodes """
        neighbours = set()

        if node.north != 0:
            neighbours.add(node.north)
        if node.east != 0:
            neighbours.add(node.east)
        if node.west != 0:
            neighbours.add(node.west)
        if node.south != 0:
            neighbours.add(node.south)
        
        return neighbours


    def distance_to(self,start_node,end_node):
        """ The distance in a straight line between two points on the board """
        x = start_node.x - end_node.x
        y = start_node.y - end_node.y
        return 1 * max(abs(x),abs(y))

    def evaluation_function(self,node,goal):
        """ Our evaluation function is the distance_to function plus the cost of the path so far """
        return (node.self.distance_to(goal) + node.path_cost)

    def heuristic_cost_estimate(self,start_node,end_node):
        heuristic = self.distance_to(start_node,end_node)
        return heuristic 

    def reconstruct_path(self, current_node):
        """ Reconstruct the path recursively by traversing back through the came_from list """

        try: 
            self.came_from[current_node]
            p = self.reconstruct_path(self.came_from[current_node])
            return_path = []
            return_path.extend(p)
            return_path.append(current_node)
            return return_path
        except KeyError,e:
            # we have reached the start node
            return [current_node]

    def count(self,set_to_count):
        total_count = 0
        for i in set_to_count:
            total_count = total_count + 1
        return total_count
        

