import math 

def find_distance(rock1, rock2):
    return math.sqrt((rock1[0] - rock2[0])**2 + 
                        (rock1[1] - rock2[1])**2)

def find_min_distance(rocks_in, rocks, distance_in):
    p = 0
    q = 0
    min_distance = 0
    if len(rocks_in) == 0:
        for i in range(len(rocks)):
            for j in range(i+1,len(rocks)):
                distance = find_distance(rocks[i], rocks[j])
                if i == 0 and j == 1:
                    min_distance = distance
                    p = i
                    q = j
                else:
                    if distance < min_distance:
                        min_distance = distance
                        p = i
                        q = j
        rocks_in.append(rocks.pop(p))
        rocks_in.append(rocks.pop(q-1))
        distance_in.append(min_distance)
        return rocks_in, rocks, distance_in
    else:
        for i in range(len(rocks)):
            for j in range(len(rocks_in)):
                distance = find_distance(rocks[i], rocks_in[j])
                if i==0 and j==0:
                    min_distance = distance
                    p = i
                    q = j
                else:
                    if distance < min_distance:
                        min_distance = distance
                        p = i
                        q = j
        rocks_in.append(rocks.pop(p))
        distance_in.append(min_distance)
        return rocks_in, rocks, distance_in

def count_rocks(ribbon_length, rocks):
    i = 0
    rocks_in = []
    distance_in = []
    while(len(rocks)>0):
        if i == 0:
            rocks_in, rocks, distance_in = find_min_distance(rocks_in, rocks, distance_in)
            if distance_in[i]*2 > ribbon_length:
                return 1
        else:
            rocks_in, rocks, distance_in = find_min_distance(rocks_in, rocks, distance_in)
            if (sum(distance_in) + find_distance(rocks_in[0], rocks_in[-1])) > ribbon_length:
                return len(rocks_in)-1 
        i=i+1
    if len(rocks) == 0:
        return len(rocks_in)

rocks = [(0,0),(3,0),(3,3),(3,5),(7,9)]
ribbon_length = 15
print(count_rocks(ribbon_length,rocks))
