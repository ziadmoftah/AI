from copy import copy, deepcopy
from queue import PriorityQueue


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

    def StringTo2D(self, mazeStr,heristicValue):   #Changes the maze from the string format into a 2D array of Nodes
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
        self.path.clear()
        self.fullPath.clear()
        queueS = []
        queueE = []
        parentNodeE = None
        parentNodeS = None
        visitedS = set()
        visitedE = set()

        mazeE = deepcopy(self.maze)
        mazeS = deepcopy(self.maze)

        startNode = mazeS[self.startNode[0]][self.startNode[1]]
        endNode = mazeE[self.endNode[0]][self.endNode[1]]
        queueE.append(endNode)
        queueS.append(startNode)

        while queueS.__len__() > 0 and queueE.__len__() > 0:
            if queueS.__len__() > 0:
                parentNodeS = queueS.pop(0)
                visitedS.add(parentNodeS)
                self.fullPath.append(parentNodeS.id)
                tempE = []
                for i in queueE:

                    tempE.append(i.id)

                if parentNodeE != None and (parentNodeS.id == parentNodeE.id or parentNodeS.id in tempE):
                    if(parentNodeS.id in tempE):
                        bla = tempE.index(parentNodeS.id)
                        intersectNodeE = queueE[bla]
                        intersectNodeS = parentNodeS.previousNode
                    else:
                        intersectNodeS = parentNodeS
                        intersectNodeE = parentNodeE

                    #print(parentNodeS.id,parentNodeE.id)
                    #print(intersectNode.id)
                    break

                if parentNodeS.up != None and parentNodeS.up not in visitedS and parentNodeS.up.value != '#':
                    parentNodeS.up.previousNode = parentNodeS
                    visitedS.add(parentNodeS.up)
                    queueS.append(parentNodeS.up)
                if parentNodeS.down != None and parentNodeS.down not in visitedS and parentNodeS.down.value != '#':
                    parentNodeS.down.previousNode = parentNodeS
                    visitedS.add(parentNodeS.down)
                    queueS.append(parentNodeS.down)
                if parentNodeS.left != None and parentNodeS.left not in visitedS and parentNodeS.left.value != '#':
                    parentNodeS.left.previousNode = parentNodeS
                    visitedS.add(parentNodeS.left)
                    queueS.append(parentNodeS.left)
                if parentNodeS.right != None and parentNodeS.right not in visitedS and parentNodeS.right.value != '#':
                    parentNodeS.right.previousNode = parentNodeS
                    visitedS.add(parentNodeS.right)
                    queueS.append(parentNodeS.right)

            if queueE.__len__() > 0:
                parentNodeE = queueE.pop(0)
                visitedE.add(parentNodeE)
                self.fullPath.append(parentNodeE.id)

                tempS = []
                for i in queueS:
                    tempS.append(i.id)
                if parentNodeE == parentNodeS or parentNodeE.id in tempS:
                    if(parentNodeE in queueS):
                        bla = tempS.index(parentNodeE.id)
                        intersectNodeS = queueS[bla]
                        intersectNodeE = parentNodeE.previousNode
                    else:
                        intersectNodeS = parentNodeS
                        intersectNodeE = parentNodeE
                    break

                if parentNodeE.up != None and parentNodeE.up not in visitedE and parentNodeE.up.value != '#':
                    parentNodeE.up.previousNode = parentNodeE
                    visitedE.add(parentNodeE.up)
                    queueE.append(parentNodeE.up)
                if parentNodeE.down != None and parentNodeE.down not in visitedE and parentNodeE.down.value != '#':
                    parentNodeE.down.previousNode = parentNodeE
                    visitedE.add(parentNodeE.down)
                    queueE.append(parentNodeE.down)
                if parentNodeE.left != None and parentNodeE.left not in visitedE and parentNodeE.left.value != '#':
                    parentNodeE.left.previousNode = parentNodeE
                    visitedE.add(parentNodeE.left)
                    queueE.append(parentNodeE.left)
                if parentNodeE.right != None and parentNodeE.right not in visitedE and parentNodeE.right.value != '#':
                    parentNodeE.right.previousNode = parentNodeE
                    visitedE.add(parentNodeE.right)
                    queueE.append(parentNodeE.right)

        show = []
        while (intersectNodeS.previousNode != None):
            show.append(intersectNodeS.id)
            intersectNodeS = intersectNodeS.previousNode
        show.append(intersectNodeS.id)
        show.reverse()

        for i in show:
            self.path.append(i)
        while (intersectNodeE.previousNode != None):
            self.path.append(intersectNodeE.id)
            intersectNodeE = intersectNodeE.previousNode
        self.path.append(intersectNodeE.id)


        return self.path, self.fullPath


    def BFS(self):
        self.path.clear()
        self.fullPath.clear()
        startNode=self.maze[self.startNode[0]][self.startNode[1]]
        pq= PriorityQueue()
        startNode.gOfN=0
        pq.put((0,startNode.id))
        self.fullPath.append(startNode.id)
        while pq.empty()==False:
            index = pq.get()[1]
            parentNode = self.maze[index[0]][index[1]]
            if parentNode.value == 'E':
                break
            if parentNode.up != None and parentNode.up.id not in self.fullPath:

                parentNode.up.gOfN= parentNode.gOfN+parentNode.up.edgeCost
                parentNode.up.previousNode = parentNode
                pq.put((parentNode.up.edgeCost, parentNode.up.id))
                self.fullPath.append(parentNode.up.id)

            if parentNode.down != None and parentNode.down.id not in self.fullPath:
                parentNode.down.gOfN = parentNode.gOfN + parentNode.down.edgeCost
                parentNode.down.previousNode = parentNode
                pq.put((parentNode.down.edgeCost, parentNode.down.id))
                self.fullPath.append(parentNode.down.id)

            if parentNode.right != None and parentNode.right.id not in self.fullPath:
                parentNode.right.gOfN = parentNode.gOfN + parentNode.right.edgeCost
                parentNode.right.previousNode = parentNode
                pq.put((parentNode.right.edgeCost, parentNode.right.id))
                self.fullPath.append(parentNode.right.id)

            if parentNode.left != None and parentNode.left.id not in self.fullPath:
                parentNode.left.gOfN = parentNode.gOfN + parentNode.left.edgeCost
                parentNode.left.previousNode = parentNode
                pq.put((parentNode.left.edgeCost, parentNode.left.id))
                self.fullPath.append(parentNode.left.id)

        #get the full path
        #calculate total cost of the path
        self.totalCost=parentNode.gOfN

        #calculate the path
        while parentNode.previousNode != None:
            self.path.append(parentNode.id)
            parentNode=parentNode.previousNode

        self.path.append(startNode.id)
        self.path.reverse()
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


    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30,
                                                                                                             3, 100, 2, 15, 60, 100, 30,
                                                                                                             2 , 100, 2, 2, 2, 40, 30,
                                                                                                              2, 2, 100, 100, 3, 15, 30,
                                                                                                             100, 2 , 100, 0, 2, 100, 30])

    path, fullPath, TotalCost = searchAlgo.BFS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################
    '''



main()
