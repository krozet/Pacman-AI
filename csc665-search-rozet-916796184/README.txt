Keawa Rozet
916796184

Question 1:
I use a stack and push nodes to the frontier that consist of a position, direction, and a path. The stack is popped and the position is checked if its a goal state and also if it has been visited before. If it hasn't been visited before, then it's successors are added to the stack if they also haven't been visited before.

Question 2:
I use a queue and push nodes to the frontier that consist of a position, direction, and a path. The queue is popped and the position is checked if its a goal state and also if it has been visited before. If it hasn't been visited before, then it's successors are added to the queue if they also haven't been visited before.

Question 3:
I use a priority queue and push nodes to the frontier that consist of a position, direction, current cost, path, and cost. The priority queue is popped and the position is checked if its a goal state and also if it has been visited before. If it hasn't been visited before, then it's successors are added to the priority queue if they also haven't been visited before.

Question 4:
I use a priority queue and push nodes to the frontier that consist of a position, direction, current cost, path, and total cost. The priority queue is popped and the position is checked if its a goal state and also if it has been visited before. If it hasn't been visited before, then it's successors are added to the priority queue with a new calculated cost of adding the heuristic value to the current cost if they also haven't been visited before.

Question 5:
getStartState:
  Initializes corners to false and checks if starting position is on a corner. It returns corners state and starting position.
isGoalState:
  Checks if pacman is in the same position as a corner. If all corners have been visited, then isGoalState returns true.
getSuccessors:
  Checks if pacman is in the same position as a corner. Then it appends all the surrounding locations that do not hit a wall to the successors list and returns that.

Question 6:
All corners are checked and if a corner hasn't be visited, then the distance to the corner is calculated using mazeDistance(). The distance to the closest corner is returned.

Question 7:
All food dots are checked and the max distance to the food is returned.

Question 8:
The problem is passed into breadthFirstSearch and returned.
