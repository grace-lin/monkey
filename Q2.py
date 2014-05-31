import sys
import math
    

### === READ INPUT  === ###
# first 4 readline instances are for l, h, s, n
#
# info: list of tuples (x_i, t_i)
### only want attached nodes in neighbours, so don't populate while read
# neighbours: dictionary, where
#     value: int, x_i,
#     key  : list, first index is t_i
#                  remaining indeces are neighbours (x_j) of this node
### =================== ###

# TODO: monkey can drop >1 thing at same time, same place
count = 0
info = [(0, 0)]
neighbours = {}
neighbours[(0, 0)] = [0]

fname = sys.argv[1]
with open(fname) as f:
    for line in f:
        if line[0] != "#":
            if count == 0:
                l = int(line.strip())

            elif count == 1:
                h = int(line.strip())

            elif count == 2:
                s = int(line.strip())

            elif count == 3:
                n = int(line.strip())

            else: # info
                nums = line.strip().split() # list of strings
                x = int(nums[0])
                t = int(nums[1])
                
                # if more than one item is dropped at the same time and place
                if (x, t) in info:
                    neighbours[(x, t)][0] -= 1
                    
                else:
                    info.append((x, t))
                    neighbours[(x, t)] = [0]

            count += 1

info.sort()

if n > 99:
    sys.setrecursionlimit(n*n)
    

### build graph ver. 2 ###
# keep track of which nodes we've visited ==> delete from info
# 
# start at (0, 0), and check all of the remaining nodes in info;
# insert into its neighbours only if reachable
# remove (0, 0) from info
# 
# repeat above each neighbour:
# check remaining nodes in info;
# insert into its neighbours only if reachable
# remove node from info

### === populate ver. 2 === ###
### global info2 is for nodes to not recurse into.
### You can still check them for neighbours!
#
# if at the end of a path (no more neighbours!),
#     return itself? or append itself to the global info2
# else, grab first thing in info that's not in info2 and call populate
### ======================= ###

def get_next(info):
    """
    Given the list of (position, time) tuples,
    returns the tuple of the smallest time.
    """
    p = -1
    t = float('inf')
    for i in range(len(info)):
        if info[i][1] < t:
            t = info[i][1]
            p = i
    return p

no_rec = []

# valid = valid nodes to search through
# no_inv = don't investigate these
def populate2(valid, neighbours, node, no_inv):
    global no_rec
    #global valid
    
    while valid != []:
        i = get_next(valid)
    #for i in range(len(valid)):
        # in valid and not in no_investigate
        if (node not in no_inv):
            tot_time = valid[i][1] - node[1]
            x_diff   = (float(valid[i][0] - node[0])) / float(s)

            # from source
            if (node == (0, 0)):
                tot_time += h
                
            check = valid[i]
            del valid[i]
            
            # if we can reach the neighbour node in time
            if tot_time >= x_diff:
                neighbours[node].append(check)

                # if valid[i] is not in don't recurse,
                if check not in no_rec:
                    no_rec.append(check)
                    
                    # ancestors.append(valid[i])
                    #print ("pop2 again with %s\n" % (check,))
                    no_inv = populate2(valid, neighbours, check, no_inv)

    # investigated all possible neighbours, so add self to no_inv
    no_inv.append(node)
    return no_inv
del info[0]
#print("starting populate2 now\n")
populate2(info, neighbours, (0,0), [])
#print("done populating\n")

### ======================== ###

### === BELLMAN-FORD === ###
### ==================== ###

def bellman_ford():
    items = neighbours[(0, 0)][0]
    
    for i in range(1, n):
        # for each reachable key in neighbours, check each of its neighs
        for key in neighbours:
            for neigh in neighbours[key][1:]:
                old = neighbours[neigh][0]
                new = neighbours[key][0] - 1
    
                if new < old: 
                    neighbours[neigh][0] = new
    
                    # keep track of how many items caught so far
                    if new < items:
                        items = new
                        if items == -n:
                            #print ("done!")
                            return items
    return items

items = bellman_ford()
print (-items)
