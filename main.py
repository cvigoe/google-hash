import random
import scipy.stats
from parser import Parser
import math

def make_decision(cache, request):
	data_center_latency = request['endpoint']['data_centre_latency']
	cache_id = cache['cache_id']
	# cache['cache_latencies'][request['endpoint']['endpoint_id']]

	endpoint_id = request['endpoint']['endpoint_id']

	if(endpoint_id in cache['cache_latencies']):
		cache_latency = cache['cache_latencies'][endpoint_id]
	else:
		return False
	saving = data_center_latency - cache_latency

	requests = request['number_of_requests']

	z_score = (saving - saving_means[cache_id]['mean']) / saving_standard_deviations[cache_id]['standard_deviation']
	p_saving = scipy.stats.norm.cdf(z_score)

	z_score = (requests - request_means[cache_id]['mean']) / request_standard_deviations[cache_id]['standard_deviation']
	p_request = scipy.stats.norm.cdf(z_score)

	return random.uniform(0, 1) < p_saving*p_request

def calculate_saving_means(endpoints, saving_means):
	for endpoint in endpoints:
		for cache in endpoint['caches']:
			saving_means[cache['cache_id']]['mean'] += (endpoint['data_centre_latency'] - cache['cache_latencies'][endpoint['endpoint_id']])
			saving_means[cache['cache_id']]['n'] += 1

	for value, key in enumerate(saving_means):
		saving_means[value]['mean'] = saving_means[value]['mean'] / saving_means[value]['n']

def calculate_saving_standard_deviations(endpoints, saving_standard_deviations):
	for endpoint in endpoints:
		for cache in endpoint['caches']:
			saving_standard_deviations[cache['cache_id']]['standard_deviation'] += ((endpoint['data_centre_latency'] - cache['cache_latencies'][endpoint['endpoint_id']]) - saving_means[cache['cache_id']]['mean'])^2
			saving_standard_deviations[cache['cache_id']]['n'] += 1

	for value, key in enumerate(saving_standard_deviations):
		saving_standard_deviations[value]['standard_deviation'] = saving_standard_deviations[value]['standard_deviation'] / (saving_standard_deviations[value]['n'] - 1)
		saving_standard_deviations[value]['standard_deviation'] = math.sqrt(abs(saving_standard_deviations[value]['standard_deviation']))

def calculate_request_means(caches, request_means):
	for cache in caches:
		for request in cache['requests']:
			request_means[cache['cache_id']]['mean'] += (request['number_of_requests'])
			request_means[cache['cache_id']]['n'] += 1

	for value, key in enumerate(request_means):
		request_means[value]['mean'] = request_means[value]['mean'] / request_means[value]['n']

def calculate_request_standard_deviations(caches, request_standard_deviations):
	for cache in caches:
		for request in cache['requests']:
			request_standard_deviations[cache['cache_id']]['standard_deviation'] += (request['number_of_requests'] - request_means[cache['cache_id']]['mean'])^2
			request_standard_deviations[cache['cache_id']]['n'] += 1

	for value, key in enumerate(saving_standard_deviations):
		request_standard_deviations[value]['standard_deviation'] = request_standard_deviations[value]['standard_deviation'] / (request_standard_deviations[value]['n'] - 1)
		request_standard_deviations[value]['standard_deviation'] = math.sqrt(abs(request_standard_deviations[value]['standard_deviation']))

# print(data)

availability_threshold = 10


request1 = {'number_of_requests': 10, 'video_id': 1, 'endpoint': 0}
request2 = {'number_of_requests': 30, 'video_id': 3, 'endpoint': 0}
request3 = {'number_of_requests': 100, 'video_id': 2, 'endpoint': 0}

cache1 = {'requests': [request1, request2, request3], 'store': [], 'available': 100, 'cache_id': 0, 'cache_latencies': {0: 400, 1: 200}}
cache2 = {'requests': [request1, request2, request3], 'store': [], 'available': 100, 'cache_id': 1, 'cache_latencies': {0: 40, 1: 100}}
cache3 = {'requests': [request1, request2, request3], 'store': [], 'available': 100, 'cache_id': 2, 'cache_latencies': {0: 20, 2: 200}}

endpoint1 = {'caches': [cache1, cache2, cache3], 'data_centre_latency': 200, 'endpoint_id': 0 }
endpoint2 = {'caches': [cache1, cache2], 'data_centre_latency': 200, 'endpoint_id': 1 }
endpoint3 = {'caches': [cache3], 'data_centre_latency': 200, 'endpoint_id': 2 }

request1['endpoint'] = endpoint1
request2['endpoint'] = endpoint2
request3['endpoint'] = endpoint3

saving_means = { 0: {'mean': 0, 'n': 0},  1: {'mean': 0, 'n': 0}, 2: {'mean': 0, 'n': 0} }

caches = data.caches
endpoints = data.endpoints

caches = [cache1, cache2, cache3]
endpoints = [endpoint1, endpoint2, endpoint3]

saving_means = {0: {'mean': 0, 'n': 0}, 1: {'mean': 0, 'n': 0}, 2: {'mean': 0, 'n': 0}}
saving_standard_deviations = {0: {'standard_deviation': 0, 'n': 0}, 1: {'standard_deviation': 0, 'n': 0}, 2: {'standard_deviation': 0, 'n': 0}}
request_means = {0: {'mean': 0, 'n': 0}, 1: {'mean': 0, 'n': 0}, 2: {'mean': 0, 'n': 0}}
request_standard_deviations = {0: {'standard_deviation': 0, 'n': 0}, 1: {'standard_deviation': 0, 'n': 0}, 2: {'standard_deviation': 0, 'n': 0}}

calculate_saving_means(endpoints, saving_means)
calculate_saving_standard_deviations(endpoints, saving_standard_deviations)
calculate_request_means(caches, request_means)
calculate_request_standard_deviations(caches, request_standard_deviations)

for cache in caches:
	for request in cache['requests']:
		if(cache['available'] > availability_threshold):
			print("Make decision...")
			if(make_decision(cache, request)):
				print("Add it!")
				cache['store'].append(request['video_id'])
			else:
				print("Soz!")
