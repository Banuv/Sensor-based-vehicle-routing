import format

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(heatmap_matrix, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given heatmap_matrix"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    goal_node = Node(None, end)
    goal_node.g = goal_node.h = goal_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == goal_node:
            path = []
            total_cost = 0
            movement_cost = 0
            heuristic_cost = 0
            current = current_node
            while current is not None:
                path.append(current.position)
                total_cost = total_cost + current.f
                movement_cost = movement_cost + current.g
                heuristic_cost = heuristic_cost + current.h 
                current = current.parent
            return path[::-1],total_cost,movement_cost,heuristic_cost # Return reversed path and total costs

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(heatmap_matrix) - 1) or node_position[0] < 0 or node_position[1] > (len(heatmap_matrix[len(heatmap_matrix)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            #if heatmap_matrix[node_position[0]][node_position[1]] != 0:
            #    continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + heatmap_matrix[child.position[0]][child.position[1]]
#           print (child.g)
            child.h = ((child.position[0] - goal_node.position[0]) ** 2) + ((child.position[1] - goal_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():

    heatmap_matrix = format.format()
    print("heatmap matrix:")
    print(heatmap_matrix)
    startx, starty = input("Enter start co-ordinates here: ").split()
    endx, endy = input("Enter end co-ordinates here: ").split()
    start = (int(startx), int(starty))
    end = (int(endx), int(endy))

    path,total_cost,movement_cost,heuristic_cost, = astar(heatmap_matrix, start, end)
    print("The optimal path is:")
    print(path)
    for i in range(len(heatmap_matrix)):
        for j in range (0, 4):
            for p in range(len(path)):
                if i == path[p][0] and j == path[p][1]:
                    heatmap_matrix[i][j] = '*'
    
    
    for i in reversed((heatmap_matrix)):
        print(i) 
    
      
    print("Total cost:"+ str(total_cost))
    print("movement_cost:"+ str(movement_cost))
    print("heuristic_cost:"+ str(heuristic_cost))
    


if __name__ == '__main__':
    main()

