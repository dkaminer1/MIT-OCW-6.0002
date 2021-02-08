###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    egg_weights = sorted(egg_weights, reverse = True)
    weight_mut = int(target_weight)
    egg_dict = {}
    for weight in egg_weights :
        rem_weight = weight_mut % weight
        eggs_by_weight = int((weight_mut - rem_weight) / weight)
        weight_mut = rem_weight
        egg_dict[weight] = eggs_by_weight
    egg_dict_copy = egg_dict.copy()
    for weight in egg_dict_copy :
        if egg_dict_copy[weight] == 0 :
            del egg_dict[weight]
    tot_eggs = 0
    egg_string = ""
    for weight in egg_dict:
        tot_eggs += egg_dict[weight]
        egg_string = egg_string + str(egg_dict[weight]) + ' * ' + str(weight) + ' + '
    egg_string = egg_string[:-3]
    tot_weight = 0
    for weight in egg_dict:
        tot_weight += egg_dict[weight] * weight
    return  str(tot_eggs) + ' (' + egg_string + ') = ' + str(tot_weight)
        
        
        
        

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
