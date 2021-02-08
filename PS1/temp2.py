#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:52:00 2021

@author: dkaminer
"""
#from ps1_partition import partitions
#from ps1_partition import get_partitions

def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b

def get_partitions(set_):
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_file = open(filename, 'r')
    cow_dict = {}
    for line in cow_file:
        if not len(line) == 0:
            line = line.rstrip()
            line = line.split(',')
            cow_dict[line[0]] = int(line[1])
    return cow_dict




filename = 'ps1_cow_data_2.txt'
cows_dict = load_cows(filename)
cows_names_left = (cows_dict.copy())
cows_names_left = list(cows_names_left.keys())
#print(cows_names_left)
def Tripinlimit(partition,limit):
    for trip in partition :
        weight_trip = 0
        for cow in trip :
            weight_trip += cows_dict[cow]
            
        if weight_trip > limit:
            return False
list_of_trips = []
i=0
limit = 10
for partition in get_partitions(cows_names_left):
    weight_trip = 0
    if Tripinlimit(partition, limit) != False :
        list_of_trips.append(partition)
min_cow_trips = min(len(trip) for trip in list_of_trips)
def getmintrips(list_of_trips, min_cow_trips) :
    copy_triplist = []
    for partition in list_of_trips :
        if len(partition) == min_cow_trips:
            copy_triplist.append(partition)
    return copy_triplist[0]
print(getmintrips(list_of_trips, min_cow_trips)[0])

