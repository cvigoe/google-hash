class Parser:
    def __init__(self):
        self.data = {"videoSizes": {}, "requests": {}, "caches": {}, "endpoints": {}}
        self.currentLine = 0
        self.lastLineProcessed = 0

    def process_file(self, path_to_file):
        self.dataFile = open(path_to_file, 'r').readlines()
        self.parseMetaData()
        self.parseVideoSizes()
        self.parseEndpointDescriptions()
        self.parseRequestDescriptions()
        self.buildCacheLookupStructure()
        # print self.data["caches"]

    def parseMetaData(self):
        startingLine = 0
        splitedLine = self.dataFile[startingLine].split(' ')
        self.data['V'] = int(splitedLine[0])
        self.data['E'] = int(splitedLine[1])
        self.data['R'] = int(splitedLine[2])
        self.data['C'] = int(splitedLine[3])
        self.data['X'] = int(splitedLine[4])

    def parseVideoSizes(self):
        startingLine = 1
        videoSizes = self.dataFile[startingLine].split(' ')
        for idx, videoSize in enumerate(videoSizes):
            self.data['videoSizes'][idx] = int(videoSize)

    def parseEndpointDescriptions(self):
        startingLine = 2
        counter = 0
        endpointDescriptionStart = 3

        while(counter < self.data['E']):
            firstLineInDescription = self.dataFile[startingLine].split(' ')

            endpointName = counter
            self.data['endpoints'][endpointName] = {}
            self.data['endpoints'][endpointName]['L'] = int(firstLineInDescription[0])
            self.data['endpoints'][endpointName]['K'] = int(firstLineInDescription[1])
            self.data['endpoints'][endpointName]['requests'] = {}
            self.data['endpoints'][endpointName]['connections'] = {}

            kCounter = 0
            while(kCounter < self.data['endpoints'][endpointName]['K']):
                lineNumber = startingLine+kCounter+1
                splitedLine = self.dataFile[lineNumber].split(' ')
                cacheId = int(splitedLine[0])
                latency = int(splitedLine[1])
                self.data['endpoints'][endpointName]['connections'][cacheId] = {"latency": latency}
                kCounter += 1
            counter += 1

            startingLine = lineNumber + 1
        self.lastLineProcessed = startingLine

    def parseRequestDescriptions(self):
        rCounter = 0
        startingLine = self.lastLineProcessed + 1
        # print startingLine
        # print self.data['R']
        while (rCounter < (self.data['R']-1)):
            splitedLine = self.dataFile[startingLine+rCounter].split(' ')
            requestedVideoId = int(splitedLine[0])
            idOfEndpointThatRequestsAreComingFrom = int(splitedLine[1])
            numberOfRequests = int(splitedLine[2])

            self.data['endpoints'][idOfEndpointThatRequestsAreComingFrom]['requests'][rCounter] = {
                "requestedVideoId": requestedVideoId,
                "idOfEndpointThatRequestsAreComingFrom": idOfEndpointThatRequestsAreComingFrom,
                "numberOfRequests": numberOfRequests
            }
            rCounter += 1

    def buildCacheLookupStructure(self):
        # loop over endpoints
        endPointIds = self.data['endpoints'].keys()
        for endPointId in endPointIds:
            endPoint = self.data['endpoints'][endPointId]
            cacheIds = endPoint['connections'].keys()
            for cacheId in cacheIds:
                self.data["caches"][cacheId] = {
                    "requests": endPoint['requests'],
                    "store": [],
                    "available": self.data['X']
                }






Parser().process_file('kittens.in')
