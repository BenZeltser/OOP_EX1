import math


from ElevatorCall import CallForElevator
import static
import heapq
from DoubleLinkedList import DoubleLinkedList, Node
import ElevatorAlgo
import Heap
import threading

'''
    ***TODO***
    1.
    
'''
# Columns:
# 1 - same String as always
# 2 - Time
# 3 - SRC
# 4 - DST
# 5 NOT RELEVANT
# 6 - THE INDEXED ELEVATOR TO ALLOCATE 4 THE CALL

class Elevator:
    global upCalls, downCalls, list_of_calls
    upCalls = []
    downCalls = []
    list_of_calls = []
    global ERROR, DOWN, LEVEL, UP, OPEN, CLOSE
    ERROR = -2
    DOWN = -1
    LEVEL = 0
    UP = 1
    OPEN = 1
    CLOSE = 0
    #PlaceHolders:
    time=DST=SRC=a_call=0

    def __init__(self, _id, _speed, _minFloor, _maxFloor, _closeTime, _openTime, _startTime, _stopTime):
        self.callType = None
        self._id = _id
        self._speed = _speed
        self._minFloor = _minFloor
        self._maxFloor = _maxFloor
        self._closeTime = _closeTime
        self._openTime = _openTime
        self._startTime = _startTime
        self._stopTime = _stopTime

        self.state = LEVEL
        self.currentFloor = Node(self._minFloor)
        self.callType
        if int(_id)%2==0:
            self.callType = UP
        else:
            self.callType = DOWN

        '''
        Initiate a Doubly Linked List 
        '''
        # init floorSet
        curr = self.currentFloor
        self.floorSet = DoubleLinkedList(curr)

        i = curr.get_data()
        while i < self._maxFloor:
            self.floorSet.insert_end(curr.get_data() + i)
            i += 1

        '''
        Send the Node curr back to 0
        '''
        temp = self.currentFloor
        while temp.get_data() > 0:
            temp = temp.get_prev()
        self.currentFloor = temp

    @staticmethod
    def addCall(call=CallForElevator):
        list_of_calls.append(call)

    @staticmethod
    def removeCall():
        list_of_calls.remove()

    def getCallType(self):
        return self.callType

    def getUpCall(self, call=CallForElevator(a_call,time,SRC,DST)):
        upCalls.append(call.get_SRC())  # add the call
        upCalls.append(call.get_DST())
        while upCalls.__sizeof__() > 0:
            # GOTO SRC THEN GOTO DST
            heapq.heapify(upCalls)  # either O(1) or O(log(N))
            self.goto(heapq.heappop(upCalls))  # go the the most relevant call
            self.goto(heapq.heappop(upCalls))  # go the the most relevant call
            self.state = UP

        self.state = LEVEL

    def getDownCall(self, call=CallForElevator(a_call,time,SRC,DST)):
        downCalls.append(call.get_SRC())  # add the call
        while downCalls.__sizeof__() > 0:
            Heap.maxheapify(downCalls)  # either O(1) or O(log(N))
            #GOTO SRC THEN GOTO DST
            self.goto(heapq.heappop(downCalls))  # go the the most relevant call
            self.goto(heapq.heappop(downCalls))  # go the the most relevant call
            self.state = DOWN
        #timecount
        self.state = LEVEL

    def getID(self):
        return self._id

    def getSpeed(self):
        return self._speed

    def getMinFloor(self):
        return self._minFloor

    def getMaxFloor(self):
        return self._maxFloor

    def getCloseTime(self):
        return self._closeTime

    def getOpenTime(self):
        return self._openTime

    def getStartTime(self):
        return self._startTime

    def getStopTime(self):
        return self._stopTime

    def getState(self):
        return self.state

    def calculateTime(self,dif):
        OT=self.getOpenTime()
        CT=self.getCloseTime()
        startT=self.getStartTime()
        stopT=self.getStopTime()
        SP=self.getSpeed()
        return CT+startT+(dif/SP)+OT+stopT

    def getPos(self):
        return self.currentFloor.get_data()

    def get_dest(self):
        return self.list_of_calls.index(len(list_of_calls)-1)

    def goto(self, floor):
        mySource=self.getPos()
        if self.currentFloor > floor:
            self.state = DOWN
            while self.currentFloor.get_data() > floor:
                currentFloor = currentFloor.get_prev()
                if upCalls.index(0)==currentFloor:
                    heapq.heappop(upCalls)
                    myTime=self.calculateTime(math.fabs(mySource-currentFloor))
                    mySource=currentFloor
                    CallForElevator.addTime(myTime)
                    for i in len(list_of_calls):
                        if list_of_calls[i].isDone()==1:
                            list_of_calls.pop(i)
            self.state=LEVEL

        elif (self.currentFloor < floor):
            while self.currentFloor.get_data() > floor:
                currentFloor = currentFloor.get_next()
                if downCalls.index(0)==currentFloor:
                    heapq.heappop(downCalls) #pops the call but not counting time
                self.state = UP
            self.state = OPEN
            self.state = CLOSE
            self.state=LEVEL
        else:
            self.state = LEVEL
