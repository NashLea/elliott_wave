import algorithm
import math

cacheSubProblem = {}

class ElliottWaveProblem(algorithm.SearchProblem):
    
    def __init__(self, startIndex, endIndex, stockForDateIndex, step, partialSequence):
        self.WAVE_0 = 'wave_0'
        self.WAVE_1 = 'wave_1'
        self.WAVE_2 = 'wave_2'
        self.WAVE_3 = 'wave_3'
        self.WAVE_4 = 'wave_4'
        self.WAVE_5 = 'wave_5'
        self.WAVE_A = 'wave_A'
        self.WAVE_B = 'wave_B'
        self.WAVE_C = 'wave_C'

        self.stockForDateIndex = stockForDateIndex
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.step = step
        self.partialSequence = partialSequence
        self.cacheMinPoint = {}
        self.cacheMaxPoint = {}
        
    def startState(self):
        # state := (currentWaveType, currentWaveEndIndex, isPositiveTrend, LongestDuration, startPriceW1, endPriceW1, startPriceWA)
        return (None, None, None, 0, None, None, None)
        
    def isEnd(self, state):
        if self.partialSequence:
            return state[1] == self.endIndex
        else:
            return state[0] == self.WAVE_C

    def getActionAndCost(self, waveType, startIndex, endIndex):
        if self.step == 1:
            return ((waveType, endIndex, []), math.log(3 ** (endIndex - startIndex)))
        
        newStep = self.step / 30 + 1

        result = cacheSubProblem.get((startIndex, endIndex, newStep))
        if result == None:
            subProblem = ElliottWaveProblem(startIndex, endIndex, self.stockForDateIndex, newStep, partialSequence=False)
            ucs = algorithm.UniformCostSearch()
            ucs.solve(subProblem)
        
            if ucs.actions == None:
                # No solution was found. It's not good.
                result = ((waveType, endIndex, []), float('inf'))
            else:
                result = ((waveType, endIndex, ucs.actions), ucs.totalCost)

            cacheSubProblem[(startIndex, endIndex, newStep)] = result

        return result
    
    def getMin(self, startIndex, duration):
        endIndex = min(startIndex + duration, self.endIndex)
        result = self.cacheMinPoint.get((startIndex, endIndex))
        if result == None:
            result = min((self.stockForDateIndex(index), index) for index in range(startIndex, endIndex))
            self.cacheMinPoint[(startIndex, endIndex)] = result
        return result

    def getMax(self, startIndex, duration):
        endIndex = min(startIndex + duration, self.endIndex)
        result = self.cacheMaxPoint.get((startIndex, endIndex))
        if result == None:
            result = max((self.stockForDateIndex(index), index) for index in range(startIndex, endIndex))
            self.cacheMaxPoint[(startIndex, endIndex)] = result
        return result
    
    def makeNextState(self, waveType, endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA):
        return (waveType, endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA)
    
    def succAndCost(self, state):
        currentWaveType, currentWaveEndIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA = state
        result = []
        
        if currentWaveType == None:
            # When partial sequence is allowed, the first wave can be anything
            action = (self.WAVE_0, self.startIndex, [])
            result += [(action, self.makeNextState(self.WAVE_0, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 0)]
            result += [(action, self.makeNextState(self.WAVE_0, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 0)]
            
            if self.partialSequence:
                result += [(action, self.makeNextState(self.WAVE_1, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 1)]
                result += [(action, self.makeNextState(self.WAVE_1, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 1)]

                result += [(action, self.makeNextState(self.WAVE_2, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 2)]
                result += [(action, self.makeNextState(self.WAVE_2, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 2)]

                result += [(action, self.makeNextState(self.WAVE_3, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 3)]
                result += [(action, self.makeNextState(self.WAVE_3, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 3)]

                result += [(action, self.makeNextState(self.WAVE_4, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 4)]
                result += [(action, self.makeNextState(self.WAVE_4, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 4)]

                result += [(action, self.makeNextState(self.WAVE_5, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 5)]
                result += [(action, self.makeNextState(self.WAVE_5, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 5)]

                result += [(action, self.makeNextState(self.WAVE_A, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 6)]
                result += [(action, self.makeNextState(self.WAVE_A, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 6)]

                result += [(action, self.makeNextState(self.WAVE_B, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 7)]
                result += [(action, self.makeNextState(self.WAVE_B, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 7)]

                result += [(action, self.makeNextState(self.WAVE_C, self.startIndex, True, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 8)]
                result += [(action, self.makeNextState(self.WAVE_C, self.startIndex, False, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA), 8)]

        if currentWaveType == self.WAVE_0:
            # Let's find wave 1
            #
            startPriceW1 = self.stockForDateIndex(self.startIndex)
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceW1, endIndex = self.getMax(endIndex, self.step) if isPositiveTrend else self.getMin(endIndex, self.step)

                if (startPriceW1 <= endPriceW1) != isPositiveTrend:
                    break

                newState = self.makeNextState(self.WAVE_1, endIndex, isPositiveTrend, endIndex - self.startIndex, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_1, self.startIndex, endIndex)
                result += [(action, newState, cost)]

        elif currentWaveType == self.WAVE_1:
            # Find wave 2.
            #
            # At any point in wave 2, the price shall be in w1's territory
            startPriceW2 = self.stockForDateIndex(currentWaveEndIndex)
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceW2, endIndex = self.getMin(endIndex, self.step) if isPositiveTrend else self.getMax(endIndex, self.step)
                if (startPriceW2 >= endPriceW2) != isPositiveTrend:
                    # trend check
                    break
                
                if startPriceW1 != None:
                    if (startPriceW1 < endPriceW2) != isPositiveTrend:
                        break
                    
                if longestDurationSoFar < endIndex - currentWaveEndIndex:
                    longestDurationSoFar = endIndex - currentWaveEndIndex
                    
                newState = self.makeNextState(self.WAVE_2, endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_2, currentWaveEndIndex, endIndex)
                result += [(action, newState, cost)]

        elif currentWaveType == self.WAVE_2:
            # Find wave 3
            #
            # It must be longer than W1 and W2.
            #
            startPriceW3 = self.stockForDateIndex(currentWaveEndIndex)
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceW3, endIndex = self.getMax(endIndex, self.step) if isPositiveTrend else self.getMin(endIndex, self.step)

                if endIndex - currentWaveEndIndex < longestDurationSoFar:
                    continue

                if (startPriceW3 <= endPriceW3) != isPositiveTrend:
                    break
                
                newState = self.makeNextState(self.WAVE_3, endIndex, isPositiveTrend, endIndex - currentWaveEndIndex, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_3, currentWaveEndIndex, endIndex)
                result += [(action, newState, cost)]

        elif currentWaveType == self.WAVE_3:
            # Find wave 4
            #
            # It must not enter W1's territory.
            
            startPriceW4 = self.stockForDateIndex(currentWaveEndIndex)
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceW4, endIndex = self.getMin(endIndex, self.step) if isPositiveTrend else self.getMax(endIndex, self.step)
                if (startPriceW4 >= endPriceW4) != isPositiveTrend:
                    continue

                if (endPriceW1 < endPriceW4) != isPositiveTrend:
                    break
                
                newState = self.makeNextState(self.WAVE_4, endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_4, currentWaveEndIndex, endIndex)
                result += [(action, newState, cost)]

        elif currentWaveType == self.WAVE_4:
            # Find wave 5
            #
            # It cannot be longer than the longest one so far
            startPriceW5 = self.stockForDateIndex(currentWaveEndIndex)
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceW5, endIndex = self.getMax(endIndex, self.step) if isPositiveTrend else self.getMin(endIndex, self.step)
                
                if (startPriceW5 <= endPriceW5) != isPositiveTrend:
                    break
                
                newState = self.makeNextState(self.WAVE_5, endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_5, currentWaveEndIndex, endIndex)
                result += [(action, newState, cost)]

        elif currentWaveType == self.WAVE_5:
            # Find wave A
            #
            # It cannot be longer than the longest one so far
            startPriceWA = self.stockForDateIndex(currentWaveEndIndex)
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceWA, endIndex = self.getMin(endIndex, self.step) if isPositiveTrend else self.getMax(endIndex, self.step)

                if (startPriceWA >= endPriceWA) != isPositiveTrend:
                    break

                newState = self.makeNextState(self.WAVE_A, endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_A, currentWaveEndIndex, endIndex)
                result += [(action, newState, cost)]

        elif currentWaveType == self.WAVE_A:
            # Find wave B
            #
            # It cannot go beyond startPriceWA
            startPriceWB = self.stockForDateIndex(currentWaveEndIndex)
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceWB, endIndex = self.getMax(endIndex, self.step) if isPositiveTrend else self.getMin(endIndex, self.step)
                
                if (startPriceWB <= endPriceWB) != isPositiveTrend:
                    break

                newState = self.makeNextState(self.WAVE_B, endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_B, currentWaveEndIndex, endIndex)
                result += [(action, newState, cost)]

                
        elif currentWaveType == self.WAVE_B:
            # Find wave C
            startPriceWC = self.stockForDateIndex(currentWaveEndIndex)
            endPriceWC = startPriceWC
            looksGood = True
            for endIndex in range(currentWaveEndIndex + 1, self.endIndex, self.step):
                endPriceWC, endIndex = self.getMin(endIndex, self.step) if isPositiveTrend else self.getMax(endIndex, self.step)
                
                if (startPriceWC >= endPriceWC) != isPositiveTrend:
                    looksGood = False
                    break
            
            if looksGood:
                newState = self.makeNextState(self.WAVE_C, self.endIndex, isPositiveTrend, longestDurationSoFar, startPriceW1, endPriceW1, startPriceWA)
                action, cost = self.getActionAndCost(self.WAVE_C, currentWaveEndIndex, self.endIndex)
                result += [(action, newState, cost)]

                
        return result

stocks = [
    0, 1, 2, 3,               # 1
    2, 1,                     # 2
    2, 3, 4, 5, 5, 4, 6, 7,   # 3
    6, 5,                     # 4
    6, 7, 8, 9,               # 5
    8, 7, 6,                  # A
    7,                        # B
    5, 3                      # C
]

problem = ElliottWaveProblem(0, len(stocks), lambda x:stocks[x], step=1, partialSequence=False)
ucs = algorithm.UniformCostSearch()
ucs.solve(problem)

lastEndIndex = 0
for action in ucs.actions:
#    print action
#    print action - lastEndIndex
    lastEndIndex = action

