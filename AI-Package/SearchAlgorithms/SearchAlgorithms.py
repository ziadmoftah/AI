
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

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    maze = []
    startNode = []
    endNode = []

    def __init__(self, mazeStr, heristicValue=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        SearchAlgorithms.StringTo2D(self,mazeStr)
        pass

    def StringTo2D(self, mazeStr):
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


        rowIndex = 0
        colIndex = 0
        for i in mazeStr:
            if i != ',' and i != ' ':


                tempMaze[rowIndex][colIndex].value = i
                tempMaze[rowIndex][colIndex].id = (rowIndex, colIndex)
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
                    tempMaze[rowIndex][colIndex].up = tempMaze[rowIndex - 1][colIndex].id
                if rowIndex != rowCount - 1:
                    tempMaze[rowIndex][colIndex].down = tempMaze[rowIndex + 1][colIndex].id
                if colIndex != 0:
                    tempMaze[rowIndex][colIndex].left = tempMaze[rowIndex][colIndex - 1].id
                if colIndex != colCount - 1:
                    tempMaze[rowIndex][colIndex].right = tempMaze[rowIndex][colIndex + 1].id

                colIndex += 1
                if colIndex == colCount:
                    colIndex = 0
                    rowIndex += 1

        self.maze = tempMaze




    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        return self.path, self.fullPath

    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        queueS = []
        queueE = []
        parentNodeE = None

        visitedS = set()
        visitedE = set()
        startNode = self.maze[self.startNode[0]][self.startNode[1]]
        endNode = self.maze[self.endNode[0]][self.endNode[1]]
        queueE.append(endNode)
        queueS.append(startNode)

        while queueS.__len__() > 0 and queueE.__len__() > 0:
            if queueS.__len__() > 0:
                parentNodeS = queueS.pop(0)
                visitedS.add(parentNodeS.id)
                self.fullPath.append(parentNodeS.id)

                if parentNodeS in queueE or parentNodeS == parentNodeE:

                    break

                if parentNodeS.up != None and parentNodeS.up not in visitedS and parentNodeS.id[0]-1 >= 0 and self.maze[parentNodeS.id[0]-1][parentNodeS.id[1]].value != '#':
                    visitedS.add(parentNodeS.up)
                    queueS.append(self.maze[parentNodeS.id[0]][parentNodeS.id[1]])
                if parentNodeS.down != None and parentNodeS.down not in visitedS and self.maze[parentNodeS.id[0]+1][parentNodeS.id[1]].value != '#':
                    visitedS.add(parentNodeS.down)
                    queueS.append(parentNodeS.down)
                if parentNodeS.left != None and parentNodeS.left not in visitedS and self.maze[parentNodeS.id[0]][parentNodeS.id[1]-1].value != '#':
                    visitedS.add(parentNodeS.left)
                    queueS.append(parentNodeS.left)
                if parentNodeS.right != None and parentNodeS.right not in visitedS and self.maze[parentNodeS.id[0]][parentNodeS.id[1]+1].value != '#':
                    visitedS.add(parentNodeS.right)
                    queueS.append(parentNodeS.right)



            if queueE.__len__() > 0:
                parentNodeE = queueE.pop(0)
                visitedE.add(parentNodeE.id)
                self.fullPath.append(parentNodeE.id)

                if parentNodeE in queueS or parentNodeE == parentNodeS:
                    break
                if parentNodeE.up != None and parentNodeE.up not in visitedE:
                    visitedE.add(parentNodeE.up)
                    queueE.append(parentNodeE.up)
                if parentNodeE.down != None and parentNodeE.down not in visitedE:
                    visitedE.add(parentNodeE.down)
                    queueE.append(parentNodeE.down)
                if parentNodeE.left != None and parentNodeE.left not in visitedE:
                    visitedE.add(parentNodeE.left)
                    queueE.append(parentNodeE.left)
                if parentNodeE.right != None and parentNodeE.right not in visitedE:
                    visitedE.add(parentNodeE.right)
                    queueE.append(parentNodeE.right)



        return self.path, self.fullPath

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        return self.path, self.fullPath, self.totalCost



def main():
    '''searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
    '''
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BDS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################

    '''searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
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
