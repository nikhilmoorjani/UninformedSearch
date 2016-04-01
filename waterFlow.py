from collections import deque
import sys

class TestCase(object):
    def __init__(self):
        self.typeOfAlgo = ''
        self.sourceNode = ''
        self.destinations = []
        self.middleNodes = []
        self.numberOfPipes = 0
        self.startTime = 0
        self.pipes = []

class Pipe():
    def __init__(self):
        self.startNode = ''
        self.endNode = ''
        self.length = 0
        self.offPeriods = 0
        self.offPeriodLowerBound = []
        self.offPeriodUpperBound = []
        self.pathCost = 0

class Node():
    def __init__(self,state):
        self.state = state
        self.cost = 0
        self.parent = 0
        self.parentState = ''
        self.id = 0
        self.depth = 0

def formAdjacenyList(pipes):
    graph_dict =  {}
    for edge in pipes:
        if edge.startNode in graph_dict:
                graph_dict[edge.startNode].append(edge.endNode)
        else:
            graph_dict.update({edge.startNode:[edge.endNode]})
    for key in graph_dict:
        graph_dict[key].sort()
    return graph_dict

def GetString(str):
    if(str is None):
        return str
    else:
        return str.strip()

def bfs(graph,startNode,goal):
    pastCost = 0  
    frontier = deque();
    node = Node(startNode)
    node.cost = 0
    node.depth = 0
    node.parentState = ' '
    if(node.state in goal):
        return node
    frontier.append(node)
    explored = []
    while(1):
        if(len(frontier) <= 0):
            return -1  #failure
        node = frontier.popleft()       
        if(node.state in goal):
             return node
        if node.state in graph:
            for child in graph[node.state]:
                inExplored = False
                inFrontier = False
                for c  in explored:
                    if(c.state == child):
                        inExplored = True
                        break
                for c  in frontier:
                    if(c.state == child):
                        inFrontier = True
                        break
                if(inFrontier == False and inExplored == False):             
                    n = Node(child)
                    n.parent = node.state
                    n.cost = node.cost + 1
                    frontier.append(n)
        explored.append(node)

def dfs(graph,startNode,goal):
    pastCost = 0
    for key in graph:
        graph[key].sort(reverse = True)
    
    frontier = deque();
    node = Node(startNode)
    node.cost = 0
    node.depth = 0
    node.parentState = ''
    if(node.state in goal):
        return node
    frontier.append(node)
    explored = []
    while(1):
        if(len(frontier) <= 0):
            return -1  #failure
        node = frontier.pop()
        if(node.state in goal):
           return node
        if node.state in graph.keys():       
            for child in graph[node.state]:
                inExplored = False
                inFrontier = False
                childRemove = Node("None")
                for c  in explored:
                    if(c.state == child):
                        inExplored = True
                        break
                for c  in frontier:
                    if(c.state == child):
                        inFrontier = True
                        childRemove = c
                        break
                if(inFrontier == True):
                    frontier.remove(childRemove)
                if(inExplored == False):             
                    n = Node(child)
                    n.parent = node.state
                    n.cost = node.cost + 1
                    frontier.append(n)
        explored.append(node)

def UCSImplementation(testCase):
    failure = "None"
    open = list()
    closed = list()
    node = Node(testCase.sourceNode)
    node.id = 1
    node.parent = 0
    node.cost = testCase.startTime
    node.depth = 0
    node.state = testCase.sourceNode
    open.append(node)
    #pathCost = 0
    children = deque()
    while(1):
        if(len(open) <= 0):
            return failure
        currentNode = open.pop(0)
        if(currentNode.state in testCase.destinations):
            return currentNode
        for pipe in testCase.pipes:
            if(currentNode.state == pipe.startNode):
                canEnter = True
                if(pipe.offPeriods > 0):
                   timeToEnter = currentNode.cost          
                   for index in xrange(len(pipe.offPeriodLowerBound)):
                        normalizedTime = timeToEnter%24
                        if(normalizedTime>= pipe.offPeriodLowerBound[index] and 
                          normalizedTime <= pipe.offPeriodUpperBound[index]):
                           canEnter = False
                           break
                if(canEnter is True):
                    child = Node(pipe.endNode)
                    child.cost = currentNode.cost + pipe.length
                    child.parentState = currentNode.state
                    child.depth = currentNode.depth + 1
                    children.append(child)
            while len(children) > 0 :
                    child = children.popleft()
                    isInOpen = any(x.state == child.state for x in open)
                    isInClosed = any(x.state == child.state for x in closed)
                    if (isInOpen == False and isInClosed == False ):
                        open.append(child)
                    elif (isInOpen == True):
                        for val in open:
                            if(val.state == child.state):
                                nodeToCompare = val
                                break
                        if(val.cost > child.cost):
                            open.remove(val)
                            open.append(child)
                    elif (isInClosed == True):
                        for val in closed:
                            if(val.state == child.state):
                                nodeToCompare = val
                                break
                        if(val.cost > child.cost):
                            closed.remove(val)
                            open.append(child)
            closed.append(currentNode)
            open.sort(key = lambda x: (x.cost,x.state))
               
def main():
    try:                     
        outputFileContent = []
        #filename = sys.argv[2]
        inputFile  = open("inputFile.txt","r")
        #inputFile = open(filename,"r")
        if inputFile.mode == 'r':
            contents =  inputFile.read().splitlines()       
            numberOfTestCases = contents.pop(0)
        # print numberOfTestCases
        inputFile.close()
        testCases= []
        case = []
        for count in range(len(contents)):
            if(contents[count] == "BFS" or contents[count] == "DFS" or contents[count] == "UCS"):          
                if(count == 0 or (count > 1 and contents[count - 1] == '')):
                    case = []
                    testCases.append(case)
            case.append(contents[count])        
        lstTestCases = []

        for case in testCases:
            test = TestCase()
            test.typeOfAlgo = GetString(case[0])
            test.sourceNode = GetString(case[1])
            test.destinations = case[2].split()
            if(case[3] != ''):
                test.middleNodes = case[3].split()
            test.numberOfPipes = int(case[4])
            #isInt
            for pipeCount in range(test.numberOfPipes):
                newPipe = Pipe()    
                tempPipe = case[4+pipeCount +1].split()
                newPipe.startNode = GetString(tempPipe[0])
                newPipe.endNode = GetString(tempPipe[1])
                newPipe.length = int(tempPipe[2])
                newPipe.offPeriods = int(tempPipe[3])
                if(newPipe.offPeriods != 0):
                    for offCount in range(newPipe.offPeriods):
                        offIntervals = tempPipe[3 + offCount +1].split('-')
                        newPipe.offPeriodLowerBound.append(int(offIntervals[0]))
                        newPipe.offPeriodUpperBound.append(int(offIntervals[1]))
                test.pipes.append(newPipe)	
            test.startTime = int(case[4+test.numberOfPipes + 1])
            lstTestCases.append(test)
        for testCase in lstTestCases:
            try:
                if testCase.typeOfAlgo == "UCS":
                      output =  UCSImplementation(testCase)
                      toWrite = "None"
                      if(output == "None"):
                          toWrite = "None"
                      else:
                          cost = output.cost%24
                          toWrite = str(output.state) + " " + str(cost)
                      outputFileContent.append(toWrite)

                else:
                     graph = formAdjacenyList(testCase.pipes)
                     if(testCase.typeOfAlgo == "DFS") :
                         results = []
                         toW = "None"
                         result = dfs(graph,testCase.sourceNode,testCase.destinations)
                         if(result is not -1):
                             results.append(result)

                         if(len(results) > 0):
                            results.sort(key = lambda x : x.cost)
                            sol = results.pop(0)
                            cost = (sol.cost + testCase.startTime)%24 
                            dest = sol.state
                            toW = str(dest) + " " + str(cost)
                         outputFileContent.append(toW)
                     if(testCase.typeOfAlgo == "BFS") :
                         outputs = []
                         toW = "None"
                         solution = bfs(graph,testCase.sourceNode,testCase.destinations)
                         if(solution is not -1):
                             outputs.append(solution)

                         if(len(outputs) > 0):
                            outputs.sort(key = lambda x : x.cost)
                            sol = outputs.pop(0)
                            cost =  (sol.cost + testCase.startTime)%24  
                            dest = sol.state
                            toW = str(dest) + " " + str(cost)
                         outputFileContent.append(toW)
            except:
                 outputFileContent.append("None")

        f = open("output.txt","w+") 
        for out in outputFileContent:
            f.write(out)
            f.write("\n")
        f.close()
    except Exception as e:
        f = open("output.txt","w+") 
        for out in outputFileContent:
            f.write(out)
            f.write("\n")
        f.write("None")
        f.close()
        
if __name__ == '__main__':
    main();



