#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 23:50:08 2021

@author: dkaminer
"""

# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#

# Problem 2b: Implementing load_map
#def load_map(map_filename):
#    """
#    Parses the map file and constructs a directed graph
#
#    Parameters:
#        map_filename : name of the map file
#
#    Assumes:
#        Each entry in the map file consists of the following four positive
#        integers, separated by a blank space:
#            From To TotalDistance DistanceOutdoors
#        e.g.
#            32 76 54 23
#        This entry would become an edge from 32 to 76.
#
#    Returns:
#        a Digraph representing the map
#    """
#    map_file = open(filename, 'r')
##    Opens the file and creates a copy to be used in the code
#    MIT_digraph = Digraph()
##    The Dirgraph() function from graph.py is ran and assigned to MIT_digraph
#    for line in map_file :
#        if len(line) != 0 :
#            line = line.rstrip()
##            gets rid of the ending indent
#            map_line = line.split(' ')
##            splits line at each space
#            try:
#                MIT_digraph.add_node(Node(map_line[0]))
#            except ValueError:
#                pass
#            try:
#                MIT_digraph.add_node(Node(map_line[1]))
#            except ValueError:
#                pass
#            ''' Checks if the first and second position have been added and if 
#            they have been then that add is not added a second time
#            '''
#            '''First and Second position of the line are the nodes
#            and the third and fourth positions are total distance and outdoor
#            distance respecfully, so source, destination, tot distance, outdoor dist'''
#            
#            try:
#                MIT_digraph.add_edge(WeightedEdge(Node(map_line[0]),
#                      Node(map_line[1]),
#                      (map_line[2]),(map_line[3])))
#            except ValueError:
#                pass
#    
#    
#    print("Loading map from file...")
#    return MIT_digraph    
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph
    Parameters:
        map_filename : name of the map file
    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.
    Returns:
        a Digraph representing the map
    """

    data_file = open(map_filename, 'r')
    map_graph = Digraph()
    for line in data_file:
        source_node, dest_node, total_distance, outdoor_distance = line.split(' ')
        source = Node(source_node)
        dest = Node(dest_node)
        edge = WeightedEdge(source, dest, int(total_distance), int(outdoor_distance))
        if not map_graph.has_node(source):   # checking if the node is already added to graph.
            map_graph.add_node(source)
        if not map_graph.has_node(dest):   # checking if the node is already added to graph.
            map_graph.add_node(dest)
        map_graph.add_edge(edge)
    print("Loading map from file...")
    return map_graph
#geo = load_map(filename)
#print(geo)
#gtg = []
#for edge in (geo.get_edges_for_node(Node(2))) :
#    gtg.append(str(edge.get_destination()))
#    print(edge.get_source())
##    print(edge.get_destination())
#print(geo.get_edges_for_node(Node(1)))
#print(gtg)


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#filename = 'test_load_map.txt'
#
#print(load_map(filename))
#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#)
# Problem 3a: Objective function
# 
# What is the objective function for this problem? What are the constraints?
#
# Answer: The objective function for this problem is finding the shortest path from the
#    starting vertex to the ending vertex, while the constraints are an upper bound of the 
#    max distance outside.
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
      ] and (for  best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    path[0] = path[0] + [start]
   
    if digraph.has_node(Node(start)) == False or digraph.has_node(Node(end)) == False:
        raise ValueError('Start or end node are not valid')
    elif start == end :
        return path
    else:
        for edge in digraph.get_edges_for_node(Node(start)):
            
            node = str(edge.get_destination())
            tot_distance = edge.get_total_distance() + path[1]
            tot_outdoors = edge.get_outdoor_distance() + path[2]

            if node not in path[0] and tot_distance <= best_dist and tot_outdoors <= max_dist_outdoors :
                updated_path = [path[0], tot_distance, tot_outdoors]
                new_path = get_best_path(digraph, node, end, updated_path, max_dist_outdoors, best_dist, best_path)
                    
                if new_path:
                    if not best_dist or new_path[1] < best_dist:  
                        best_path = new_path[0]
                        best_dist = new_path[1]

    return best_path, best_dist                
#'''


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
    if (digraph.has_node(start) or digraph.has_node(end)) != True:
        raise ValueError('Start or end node are not valid')
    elif start == end :
        raise ValueError('Start and End node are the same')
    else :
        def traverse_path(start, end, nodes_been_to) :
            if 
    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """


    path = [[],0 , 0]
    best_path = get_best_path(digraph, start, end, path, max_dist_outdoors, max_total_dist, best_path = None)

    if best_path[0] is None:
        raise ValueError('No work')
    else :
        return best_path[0]


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56']) #here

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32']) #here

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
