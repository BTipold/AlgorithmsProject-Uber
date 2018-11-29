####################
### BRIAN TIPOLD ###
### UBER PATHING ###
####################

### INIT ###
import sys
import csv
import random

#CONSTANTS
INFINITY = sys.maxsize

#VARIABLES
graph = []                  # graph
requests = []               # list of requests
networkCSV = open('network.csv', 'r')
requestsCSV = open('requests.csv', 'r')
totalWaitTime = 0           # total wait time is initialized
listOfUbers = []            # list to hold uber drivers
numOfCustomers = 0          # total number of customers/requests

#DIJKSTRA'S ALGORITHM
def timeOfShortestPath(startLocation, endLocation):
    if startLocation == endLocation:    # if trying to compute distance between the same node
        return 0                        # the distance is zero
    distances = []                      # initialize list to hold shortest distances
    previous = []                       # initialize list to hold the previous node it came through
    for i in range(0, 50):              # for each node in graph
        previous.append(None)           # last node is none
        distances.append(INFINITY)      # current best distance is infinity
    distances[startLocation] = 0        # best distance to starting node is zero
    visited = []                        # nothing in the visited list
    current = startLocation             # current node is start location
    while endLocation not in visited:   # when end node is in the visited list, the shortest path is found
        smallestDistanceNotVisited = INFINITY                                   # initialize variable to hold current shortest path
        for i in range(0,50):                                                   # for each node in graph
            if distances[i]<smallestDistanceNotVisited and i not in visited:    # pick shortest distance
                smallestDistanceNotVisited = distances[i]
                current = i
        for i in range(0, 50):                                                  # for each node in graph
            if graph[current][i] != 0 and i not in visited:                     # for each possible neighbour not visited yet
                if graph[current][i] + distances[current] < distances[i]:       # if smaller than whats currently in distances
                    distances[i] = graph[current][i]+distances[current]         # update distances
                    previous[i] = current
        visited.append(current)         # add current node to visited list
    return distances[endLocation]       # once the while loop breaks, return the distance of end node

#CLASSES
class uber:
    def __init__(self, startLocation):                                  # constructor
        self.startLocation = startLocation                              # start location of driver
        self.currentRequest = request(0, startLocation, startLocation)  # current job the driver is working on
        self.queuedRequest = None                                       # job queue if too many requests come in


class request:
    def __init__(self, startTime, startLocation, endLocation):
        self.startTime = startTime
        self.startLocation = startLocation - 1
        self.endLocation = endLocation - 1
        self.lengthOfJob = timeOfShortestPath(startLocation - 1, endLocation - 1)


#IMPORT CSV
dataReader = csv.reader(networkCSV, delimiter=',')                      # imports
for row in dataReader:
    graph.append(row)
    for i in range(0, 50):
        row[i] = int(row[i])
dataReader = csv.reader(requestsCSV, delimiter=',')
for row in dataReader:
    tempTime = int(row[0])
    tempStart = int(row[1])
    tempEnd = int(row[2])
    requests.append(request(tempTime, tempStart, tempEnd))
numOfCustomers = len(requests)

### ALGORITHM ###
numOfUbers = int(input("Input number of Ubers: "))          # take user input

if numOfUbers < 2 or numOfUbers > 50:                       # throw exception if bad input
    print("Enter a number between 2 and 50")
    exit(1)

#LIST OF DRIVERS
for i in range(0, numOfUbers):                              # create drivers
    listOfUbers.append(uber(random.randint(0, 49)))         # initialize them at random locations

#HANDLE THE FIRST REQUEST
closestUber = -1            # give first request to whichever driver is closest
temp = INFINITY
for i in range(0, numOfUbers):
    tempWaitTime = timeOfShortestPath(listOfUbers[i].startLocation, requests[0].startLocation)
    if tempWaitTime<temp:
        temp = tempWaitTime
        closestUber = i
listOfUbers[closestUber].currentRequest = requests[0]

#CALCULATE THE REST OF THE REQUEST
for i in range(1, numOfCustomers):          # for each request
    shortestWaitTime = INFINITY             # variable for current best wait time
    closestUber = -1                        # current closest uber
    deltaTime = requests[i].startTime - requests[i - 1].startTime # time since last request
    for j in range(0, numOfUbers):          # for each uber
        if listOfUbers[j].queuedRequest == None:    # if there is a request
            timeLeftInCurrentJob = max(0, listOfUbers[j].currentRequest.lengthOfJob - deltaTime)
            timeToNextPickup = timeOfShortestPath(listOfUbers[j].currentRequest.endLocation, requests[i].startLocation)
            tempWaitTime = timeLeftInCurrentJob + timeToNextPickup
        else:                                       # if there is not a request
            timeToQueuedRequest = timeOfShortestPath(listOfUbers[j].currentRequest.endLocation, listOfUbers[j].queuedRequest.startLocation)
            timeToNextPickup = timeOfShortestPath(listOfUbers[j].queuedRequest.endLocation, requests[i].startLocation)
            tempWaitTime = max(0, listOfUbers[j].currentRequest.lengthOfJob - deltaTime + listOfUbers[j].queuedRequest.startTime + timeToQueuedRequest) + timeToNextPickup
            listOfUbers[j].queuedRequest = None     # queued job is handled, so remove it
        if tempWaitTime < shortestWaitTime:         # update current best wait time
            shortestWaitTime = tempWaitTime
            closestUber = j
    if listOfUbers[closestUber].currentRequest.lengthOfJob - deltaTime > 0: # if the uber cant complete his current job,
        listOfUbers[closestUber].queuedRequest = requests[i]                # add it to queue
    else:                                                                   # otherwise
        listOfUbers[closestUber].currentRequest = requests[i]               # update current job with the new one
    totalWaitTime += shortestWaitTime                                       # handle a new request and add it to wait time

print("Wait time is: ", totalWaitTime)                                      # output wait time
print("Average wait time is: ", round(totalWaitTime / 300, 2))              # output avg wait time

while i != 'q':
    i = input("press 'q' to quit:")