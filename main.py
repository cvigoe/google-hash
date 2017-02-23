import random
import scipy.stats
from parser import Parser

def make_decision(cache, request):
	data_center_latency = request['endpoint']['data_centre_latency']
	cache_latency = request['endpoint'][cache['cache_id']]
	saving = data_centre_latency - cache_latency

	requests = request['number_of_requests']

	z_score = (saving - saving_means['cache_id']['mean']) / saving_standard_deviations['cache_id']['standard_deviation']
	p_saving = scipy.stats.norm.cdf(z_score)

	z_score = (requests - request_means['cache_id']['mean']) / request_standard_deviations['cache_id']['standard_deviation']
	p_request = scipy.stats.norm.cdf(z_score)

	return random.uniform(0, 1) < p_saving*p_request

def calculate_saving_means(endpoints, saving_means):
	for endpoint in endpoints:
		for cache in endpoint['caches']:
			saving_means[cache['cache_id']]['mean'] += (endpoint['data_centre_latency'] - endpoint['cache_id']['cache_latency'])
			saving_means[cache['cache_id']]['n'] += 1

	for stat in saving_means:
		stat['mean'] = stat['mean'] / stat['n']

def calculate_saving_standard_deviations(endpoints, saving_standard_deviations):
	for endpoint in endpoints:
		for cache in endpoint['caches']:
			saving_standard_deviations[cache['cache_id']]['standard_deviation'] += ((endpoint['data_centre_latency'] - endpoint['cache_id']['cache_latency']) - saving_means[cache['cache_id']]['mean'])^2
			saving_standard_deviations[cache['cache_id']]['n'] += 1

	for stat in saving_standard_deviations:
		stat['standard_deviation'] = stat['standard_deviation'] / (stat['n'] - 1)
		stat['standard_deviation'] = math.sqrt(abs(stat['standard_deviation']))

def calculate_request_means(caches, request_means):
	for cache in caches:
		for request in cache['requests']:
			request_means[cache['cache_id']]['mean'] += (request['number_of_requests'])
			request_means[cache['cache_id']]['n'] += 1

	for stat in request_means:
		stat['mean'] = stat['mean'] / stat['n']


def calculate_request_standard_deviations(caches, request_standard_deviations):
	for cache in caches:
		for request in cache['requests']:
			request_standard_deviations[cache['cache_id']]['standard_deviation'] += (request['number_of_requests'] - request_means[cache['cache_id']]['mean'])^2
			request_standard_deviations[cache['cache_id']]['n'] += 1

	for stat in request_standard_deviations:
		stat['standard_deviation'] = stat['standard_deviation'] / (stat['n'] - 1)
		stat['standard_deviation'] = math.sqrt(abs(stat['standard_deviation']))



data = Parser().process_file('kittens.in')


availability_threshold = 10

cache1 = {'requests': [request1, request2, request3], 'store': [], 'available': 100}

saving_means = { 0: {'mean': 0, 'n': 0},  1: {'mean': 0, 'n': 0}, 2: {'mean': 0, 'n': 0} }

caches = [cache1, cache2, cache3]
endpoints = []

saving_means = []
saving_standard_deviations = []
request_means = []
request_standard_deviations = []

calculate_saving_means(endpoints, saving_means)
calculate_saving_standard_deviations(endpoints, saving_standard_deviations)
calculate_request_means(caches, request_means)
calculate_request_standard_deviations(caches, request_standard_deviations)

for cache in caches:
	for request in cache['requests']:
		if(cache['available'] < availability_threshold):
			print("Make decision...")
			if(make_decision(cache, request)):
				print("Add it!")
				cache['store'].append(request['video_id'])
			else:
				print("Soz!")
