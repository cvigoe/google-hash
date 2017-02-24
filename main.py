import random
import scipy.stats
from parser import Parser
import math

AVAILABILITY_THRESHOLD = 10

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
	for endpoint_id, endpoint in endpoints.iteritems():
		for cache_id, cache_latency in endpoint['cache_latencies'].iteritems:
			saving = endpoint['data_centre_latency'] - cache_latency
			saving_means[cache_id]['mean'] += saving
			saving_means[cache_id]['n'] += 1

	for cache_id, stat in saving_means.iteritems():
		stat['mean'] = stat['mean'] / stat['n']

def calculate_saving_standard_deviations(endpoints, saving_standard_deviations):
	for endpoint_id, endpoint in endpoints.iteritems():
		for cache_id, cache_latency in endpoint['cache_latencies'].iteritems:
			saving = endpoint['data_centre_latency'] - cache_latency
			saving_standard_deviations[cache_id]['standard_deviation'] += (saving - saving_means[cache_id]['mean'])^2
			saving_standard_deviations[cache_id]['n'] += 1
	for cache_id, stat in saving_standard_deviations.iteritems():
		stat['standard_deviation'] = stat['standard_deviation'] / (stat['n'] - 1)
		stat['standard_deviation'] = math.sqrt(abs(stat['standard_deviation']))

def calculate_request_means(caches, request_means):
	for cache_id, cache in caches.iteritems():
		for request_id in caches['requests']:
			number_of_requests = requests[request_id]['number_of_requests']
			request_means[cache_id]['mean'] += number_of_requests
			request_means[cache_id]['n'] += 1
	
	for cache_id, stat in request_means.iteritems():
		stat['mean'] = stat['mean'] / stat['n']

def calculate_request_standard_deviations(caches, request_standard_deviations):
	for cache_id, cache in caches.iteritems():
		for request_id in caches['requests']:
			number_of_requests = requests[request_id]['number_of_requests']
			request_standard_deviations[cache_id]['standard_deviation'] += (number_of_requests - request_means[cache_id]['mean'])^2
			request_standard_deviations[cache_id]['n'] += 1

	for cache_id, stat in request_standard_deviations.iteritems():
		stat['standard_deviation'] = stat['standard_deviation'] / (stat['n'] - 1)
		stat['standard_deviation'] = math.sqrt(abs(stat['standard_deviation']))

def construct_stat_data(saving_means, saving_standard_deviations, request_means, request_standard_deviations):
	# CONSTRUCT DATA STRUCTURES AS IN data_formatting.py


# Parse data
data = Parser().process_file('kittens.in')
endpoints = data['endpoints']
caches = data['caches']
requests = data['requests']

# Construct data structures for statistics
saving_means = {}
saving_standard_deviations = {}
request_means = {}
request_standard_deviations = {}
construct_stat_data(saving_means, saving_standard_deviations, request_means, request_standard_deviations)

# Calculate statistics
calculate_saving_means(endpoints, saving_means)
calculate_saving_standard_deviations(endpoints, saving_standard_deviations)
calculate_request_means(caches, request_means)
calculate_request_standard_deviations(caches, request_standard_deviations)

# UPDATE THESE LINES TO REFLECT NEW DATA STRUCTURES
for cache in caches:
	for request in cache['requests']:
		if(cache['available'] > AVAILABILITY_THRESHOLD):
			print("Make decision...")
			if(make_decision(cache, request)):
				print("Add it!")
				cache['store'].append(request['video_id'])
			else:
				print("Soz!")
