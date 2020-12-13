
class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function

    def __init__(self, value, id = None, up = None, down = None, left = None, right = None):
        self.id = id
        self.up = up
        self. down = down
        self.left = left
        self.right = right
        self.value = value




class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    maze = []       # Represents list of lists of nodes of the maze
    startNode = []  # id of the starting node
    endNode = []    # id of the ending node

    def __init__(self, mazeStr, heristicValue=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        SearchAlgorithms.StringTo2D(self,mazeStr,heristicValue)
        pass

    def StringTo2D(self, mazeStr,heristicValue):
        rowCount = 1
        colCount = 0
        index = 0
        flag = False
        for i in mazeStr:
            index += 1
            if i == ' ':
                rowCount += 1
                if flag == False:
                    flag = True
                    colCount = int(index/2)

        tempMaze = []

        for i in range(rowCount):
            col = []
            for j in range(colCount):
                col.append(Node('A'))
            tempMaze.append(col)

        index = 0
        rowIndex = 0
        colIndex = 0
        for i in mazeStr:
            if i != ',' and i != ' ':

                tempMaze[rowIndex][colIndex].value = i
                tempMaze[rowIndex][colIndex].id = (rowIndex, colIndex)
                if heristicValue == None:
                    tempMaze[rowIndex][colIndex].edgeCost = 0
                else:
                    tempMaze[rowIndex][colIndex].edgeCost = heristicValue[index]
                index += 1
                if i == 'S':
                    self.startNode = [rowIndex, colIndex]
                if i == 'E':
                    self.endNode = [rowIndex, colIndex]

                colIndex += 1
                if colIndex == colCount:
                    colIndex = 0
                    rowIndex += 1


        rowIndex = 0
        colIndex = 0
        for i in mazeStr:
            if i != ',' and i != ' ':
                if rowIndex != 0:
                    tempMaze[rowIndex][colIndex].up = tempMaze[rowIndex - 1][colIndex]
                if rowIndex != rowCount - 1:
                    tempMaze[rowIndex][colIndex].down = tempMaze[rowIndex + 1][colIndex]
                if colIndex != 0:
                    tempMaze[rowIndex][colIndex].left = tempMaze[rowIndex][colIndex - 1]
                if colIndex != colCount - 1:
                    tempMaze[rowIndex][colIndex].right = tempMaze[rowIndex][colIndex + 1]


                colIndex += 1
                if colIndex == colCount:
                    colIndex = 0
                    rowIndex += 1

        self.maze = tempMaze





    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath.clear()
        self.path.clear()
        max_depth = sum(len(row) for row in self.maze)
        self.DLS_Solve(max_depth, self.maze[self.startNode[0]][self.startNode[1]], None)
        self.CorrectPath()
        return self.path, self.fullPath


    # returns 1 -> solution, returns 0 -> cutoff, return -1 -> no solution
    def DLS_Solve(self, depth, current_node, previous_node):
        if self.IsSolved(current_node.id):
            self.fullPath.append(current_node.id)
            current_node.previousNode = previous_node
            return 1
        if depth == 0:
            return 0
        cutoff = 0
        if current_node.id in self.fullPath:
            return -1
        current_node.previousNode = previous_node
        self.fullPath.append(current_node.id)
        children = self.GetChildren(current_node)
        for child in children:
            ret = self.DLS_Solve(depth - 1, child, current_node)
            if ret == 0:    # cutoff happened
                cutoff = 1
            elif ret != -1:
                return ret
        if cutoff == 1:
            return 0
        else:
            return -1



    def GetChildren(self, current_node):
        children = []
        if current_node.down != None and current_node.down.value != '#':
            children.append(current_node.down)
        if current_node.up != None and current_node.up.value != '#':
            children.append(current_node.up)
        if current_node.right != None and current_node.right.value != '#':
            children.append(current_node.right)
        if current_node.left != None and current_node.left.value != '#':
            children.append(current_node.left)
        return children

    def CorrectPath(self):
        current_node = self.maze[self.endNode[0]][self.endNode[1]]
        while current_node != None:
            self.path.append(current_node.id)
            current_node = current_node.previousNode
        self.path.reverse()

    def IsSolved(self , state):     # Returns 1 if the end point is reached
        if self.endNode[0] == state[0] and self.endNode[1] == state[1]:
            return 1
        else:
            return 0


    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes




        return self.path, self.fullPath

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        return self.path, self.fullPath, self.totalCost



def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
    '''
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BDS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################
    
    
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.BFS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################
    '''



main()
