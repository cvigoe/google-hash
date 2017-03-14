class Parser:
    def __init__(self):
        self.data = {"videos": {}, "requests": {}, "caches": {}, "endpoints": {}}
        self.currentLine = 0
        self.lastLineProcessed = 0

    def process_file(self, path_to_file):
        self.dataFile = open(path_to_file, 'r').readlines()
        self.parseMetaData()
        self.buildCacheLookup()
        self.parseVideos()
        self.parseEndpointDescriptions()
        self.parseRequestDescriptions()
        return self.data

    def parseMetaData(self):
        print('Parsing Meta Data...')
        startingLine = 0
        splitedLine = self.dataFile[startingLine].split(' ')
        self.data['V'] = int(splitedLine[0])
        self.data['E'] = int(splitedLine[1])
        self.data['R'] = int(splitedLine[2])
        self.data['C'] = int(splitedLine[3])
        self.data['X'] = int(splitedLine[4])

    def parseVideos(self):
        print('Parsing Videos...')
        startingLine = 1
        videoSizes = self.dataFile[startingLine].split(' ')
        for video_id, videoSize in enumerate(videoSizes):
            self.data['videos'][video_id] = int(videoSize)

    def parseEndpointDescriptions(self):
        print('Parsing Endpoint Descriptions...')
        startingLine = 2
        counter = 0
        endpointDescriptionStart = 3

        while(counter < self.data['E']):
            firstLineInDescription = self.dataFile[startingLine].split(' ')

            endpoint_id = counter
            self.data['endpoints'][endpoint_id] = {}
            self.data['endpoints'][endpoint_id]['data_centre_latency'] = int(firstLineInDescription[0])
            self.data['endpoints'][endpoint_id]['number_of_caches'] = int(firstLineInDescription[1])
            self.data['endpoints'][endpoint_id]['cache_latencies'] = {}

            number_of_caches_counter = 0
            while(number_of_caches_counter < self.data['endpoints'][endpoint_id]['number_of_caches']):
                lineNumber = startingLine+number_of_caches_counter+1
                splitedLine = self.dataFile[lineNumber].split(' ')
                cache_id = int(splitedLine[0])
                latency = int(splitedLine[1])
                self.data['endpoints'][endpoint_id]['cache_latencies'][cache_id] = latency
                number_of_caches_counter += 1
            counter += 1
            print('Endpoint: ' + str(endpoint_id))

            startingLine = lineNumber + 1
        self.lastLineProcessed = startingLine

    def parseRequestDescriptions(self):
        print('Parsing Request Descriptions...')
        rCounter = 0
        startingLine = self.lastLineProcessed + 1

        while (rCounter < (self.data['R'])):
            splitedLine = self.dataFile[startingLine+rCounter-1].split(' ')
            requestedVideoId = int(splitedLine[0])
            idOfEndpointThatRequestsAreComingFrom = int(splitedLine[1])
            numberOfRequests = int(splitedLine[2])

            self.data['requests'][rCounter] = {'number_of_requests': numberOfRequests, 'video_id': requestedVideoId, 'endpoint': idOfEndpointThatRequestsAreComingFrom}
           
            for cache_id in self.data['endpoints'][idOfEndpointThatRequestsAreComingFrom]['cache_latencies'].keys():
                self.data['caches'][cache_id]['requests'].add(rCounter)

            rCounter += 1
            print('Request: ' + str(rCounter))

    def buildCacheLookup(self):
        print('Building Caches...')
        availability = self.data['X']
        cache_id = 0
        while(cache_id < (self.data['C'])):
            print(cache_id)
            self.data['caches'][cache_id] = {'store': set(), 'available': availability, 'requests': set()}
            cache_id += 1
