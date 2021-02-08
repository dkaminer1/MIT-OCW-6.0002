# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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

#cow_dict = load_cows(filename)
#print(cow_dict)
#print(sorted(cow_dict.values(), reverse = True))

def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    def getCow(i):
        for cow, weight in cows_names_left.items() :
            if i == weight :
                return cow
        
        
    cows_dict = cows
    cows_dict_man = {}
    for cow in cows_dict.keys() :
        if int(cows_dict[cow]) <= limit :
            print(cows_dict[cow])
            cows_dict_man[cow] = cows_dict[cow]
#    print(cows_dict_man)
    weight_of_trip = 0
    cows_in_trip = []
    trip_desc = []
    cows_names_left = cows_dict_man.copy()
    cow_weights = sorted(cows_dict_man.values(), reverse = True)
    while len((cows_names_left.keys())) != 0 :
          cows_in_trip = []
          weight_of_trip = int(cow_weights[0])
          cow_name = getCow(i = cow_weights[0])
          cows_in_trip.append(cow_name)
          del cows_names_left[cow_name]
          cow_weights = cow_weights[1:]
          if weight_of_trip  <= limit :
              cow_weights_copy = cow_weights.copy()
              for i in cow_weights_copy :
                  if weight_of_trip + int(i) <= limit:
                      cow_weights_copy.remove(i)
                      weight_of_trip += int(i)
                      cow_name = getCow(i)
                      cows_in_trip.append(cow_name)
                      print(cow_name)
                      del cows_names_left[cow_name]      
              cow_weights = cow_weights_copy

          trip_desc.append(cows_in_trip)
    
    return trip_desc

#trip_desc = []
#print(type(trip_desc))
cows = load_cows(filename)
print(greedy_cow_transport(cows,limit=10))