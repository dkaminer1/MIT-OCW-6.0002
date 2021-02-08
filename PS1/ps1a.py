###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
filename = 'ps1_cow_data_2.txt'
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

# Problem 2
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
                    del cows_names_left[cow_name]      
            cow_weights = cow_weights_copy

        trip_desc.append(cows_in_trip)
    
    return trip_desc


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    def Tripinlimit(partition,limit):
        for trip in partition :
            weight_trip = 0
            for cow in trip :
                weight_trip += cows_dict[cow]
                
            if weight_trip > limit:
                return False

    cows_dict = load_cows(filename)
    cows_names_left = (cows_dict.copy())
    cows_names_left = list(cows_names_left.keys())
    list_of_trips = []
    for partition in get_partitions(cows_names_left):
        if Tripinlimit(partition, limit) != False :
            list_of_trips.append(partition)
    min_cow_trips = min(len(trip) for trip in list_of_trips)
    copy_triplist = []
    for partition in list_of_trips :
        if len(partition) == min_cow_trips:
            copy_triplist.append(partition)
    return (list(copy_triplist)[0])
    
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    brute_force_cow_transport(cows,limit=10)
    end = time.time()
    print (end - start)
    start = time.time()
    greedy_cow_transport(cows,limit=10)
    end = time.time()
    print (end - start)

cows = load_cows(filename)    
compare_cow_transport_algorithms()
