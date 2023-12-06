import numpy as np
import logging


logger = logging.getLogger('MariooCarteLogger')

###Defining usefull fonctions :
def fenetre(position,track):
    x = position[0]
    y = position[1]
    fenetre = np.zeros([3,3])
    fenetre = track[x:x+3, y:y+3]

    # for i in range(3):
    #     for j in range(3):
    #         fenetre[i][j]=int(track[x+i][y+j])
    return fenetre


def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def get_neighbors(array, node):
    neighbors = []
    for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbor = (node[0] + i, node[1] + j)
        if 0 <= neighbor[0] < array.shape[0] and 0 <= neighbor[1] < array.shape[1]:
            if array[neighbor[0]][neighbor[1]] != 0:
                neighbors.append(neighbor)
    return neighbors

def astar(array, start, goal, block_costs):
    open_set = set([start])
    closed_set = set()
    came_from = {}

    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda x: fscore[x])

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in get_neighbors(array, current):
            if neighbor in closed_set:
                continue

            cost = block_costs[array[neighbor[0]][neighbor[1]]]
            tentative_gscore = gscore[current] + cost

            if neighbor not in open_set or tentative_gscore < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gscore
                fscore[neighbor] = gscore[neighbor] + heuristic(neighbor, goal)

                if neighbor not in open_set:
                    open_set.add(neighbor)  
                    
    return None

def mapping(track_string):
    ###Global Map*£¨%MP
    # Create a dictionary to map characters to values
    char_mapping = {'R': 255, 'G': 0, 'C':101, 'D':102, 'B':200, 'E':103, 'F':104, 'L':10}

    # Split the track string into lines and create a list of lists
    track_lines = track_string.split('\n')
    track_array = [[char_mapping[char] for char in line] for line in track_lines]

    # Convert the list of lists to a NumPy array
    track_array = np.array(track_array, dtype=np.uint8)

    ###Finding the apexes:
    # Create a dictionary to map characters to values
    char_mapping_apex = {'R': 255, 'G': 0, 'C':255, 'D':255, 'B':255, 'E':255, 'F':255, 'L':0}

    # Split the track string into lines and create a list of lists
    #track_lines = track_string.split('\n')
    track_apex = [[char_mapping_apex[char] for char in line] for line in track_lines]

    # Convert the list of lists to a NumPy array
    track_apex = np.array(track_apex, dtype=np.uint8)


    ###Defining the corners:
    Corner_1 = np.array([[255,255,255],[0,0,255],[0,0,255]])
    Corner_2 = np.array([[255,255,255],[255,0,0],[255,0,0]])
    Corner_3 = np.array([[0,0,255],[0,0,255],[255,255,255]])
    Corner_4 = np.array([[255,0,0],[255,0,0],[255,255,255]])

    ###Searching for corners:
    height = track_apex.shape[0]
    width = track_apex.shape[1]
    corners_coord = []
    corners_type = []



    for h in range(height-2):
        for w in range(width-2):
            F = fenetre([h,w],track_apex)
            if np.all(F == Corner_1):
                corners_coord.append([w+1,h-1])
                corners_coord.append([w+2,h])
                corners_coord.append([w+3,h+1])
                corners_type.append(1)
            if np.all(F == Corner_2):
                corners_coord.append([w-1,h+1])
                corners_coord.append([w,h])
                corners_coord.append([w+1,h-1])
                corners_type.append(2)
            if np.all(F == Corner_3):
                corners_coord.append([w+3,h+1])
                corners_coord.append([w+2,h+2])
                corners_coord.append([w+1,h+3])
                corners_type.append(3)
            if np.all(F == Corner_4):
                corners_coord.append([w-1,h+1])
                corners_coord.append([w,h+2])
                corners_coord.append([w+1,h+3])
                corners_type.append(4)


    ###Adding corners to the map
    track_final = np.copy(track_array)
    for corner in corners_coord:
        track_final[corner[1]][corner[0]] = 10

    ###Augmenting the scale
    useable_track = np.repeat(np.repeat(track_final,50,axis=0),50,axis=1)


    #### A*


    # Start and goal positions
    start = (150, 150)

    finish_positions = np.argwhere(track_array == 104)
    goal = (np.mean(finish_positions[:,0])*50 + 50/2., np.mean(finish_positions[:,1])*50 + 50/2.)
    logger.debug(goal)

    # Define block costs
    block_costs = {0: 2000, 15: 2000, 101: 1, 102: 1, 200: 1, 103: 1, 104: 1, 10: 1, 255:50}

    # Find the path using A*
    path = astar(useable_track, start, goal, block_costs)

    if path:
        logger.info("Path found:")
        logger.info("Success !")
    else:
        logger.error("No path found.")

    ###Adding A* info to the map

    track_traj = np.copy(track_array)
    track_passed = np.repeat(np.repeat(track_traj,50,axis=0),50,axis=1)


    ###Creating intermediate points to increase the learning
    #p = path.copy()

    p = []
    x_ini = path[0]
    p.append(x_ini)
    for x in path:
        if (np.absolute(x[0]-x_ini[0])+np.absolute(x[1]-x_ini[1])>150.):

            p.append(x)
            x_ini = x

    finish_positions = np.argwhere(track_array == 104)

    finish_positions = finish_positions*50 + (25,25)


    logger.debug("Positions of the finish line:")
    logger.debug(finish_positions)

    finish = (0,0)
    norm = 1e9
    for i in finish_positions:
        temp_norm = np.linalg.norm(p[-1] - i)
        if (temp_norm < norm):
            finish = (i[0],i[1])
            norm = temp_norm

    logger.debug("FINISH")
    logger.debug(finish)

    p.append(finish)

    size = 20
    nbr = 0
    for point in p:
        x, y = point
        track_passed[x - int(size/2):x + int(size/2) + 1, y - int(size/2):y + int(size/2) + 1] = 1000 + nbr
        nbr += size ** 2
        # for i in range(size):
        #     for j in range(size):
        #         track_passed[point[0]+i-int(size/2)][point[1]+j-int(size/2)] = 1000+nbr
        #         nbr+=1

    

    return track_passed,p







