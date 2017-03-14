import random
import scipy.stats
from parser import Parser
import math

# Change Availability Threshold to make it work harder to fill up the space
AVAILABILITY_THRESHOLD = 10

def make_decision(cache_id, cache, request_id, request, endpoints):
	endpoint_id = request['endpoint']
	data_center_latency = endpoints[endpoint_id]['data_centre_latency']

	# Check if request comes from endpoint connected to cache
	if(endpoints[endpoint_id]['number_of_caches'] > 0):
		if(cache_id in endpoints[endpoint_id]['cache_latencies'].keys()):
			cache_latency = endpoints[endpoint_id]['cache_latencies'][cache_id]
		else:
			return False
	else:
		return False
	saving = data_center_latency - cache_latency

	# Add check if video already added
	if(request['video_id'] in cache['store']):
		return False

	requests = request['number_of_requests']

	# Add video size stats

	z_score = (saving - saving_means[cache_id]['mean'])*1.0 / saving_standard_deviations[cache_id]['standard_deviation']
	p_saving = scipy.stats.norm.cdf(z_score)

	z_score = (requests - request_means[cache_id]['mean'])*1.0 / request_standard_deviations[cache_id]['standard_deviation']
	p_request = scipy.stats.norm.cdf(z_score)

	probability = p_saving*p_request

	print("Probability of adding: " + str(probability))
	return random.uniform(0, 1) < probability

def calculate_saving_means(endpoints, saving_means):
	for endpoint_id, endpoint in endpoints.iteritems():
		for cache_id, cache_latency in endpoint['cache_latencies'].iteritems():
			saving = endpoint['data_centre_latency'] - cache_latency
			saving_means[cache_id]['mean'] += saving
			saving_means[cache_id]['n'] += 1

	for cache_id, stat in saving_means.iteritems():
		stat['mean'] = stat['mean']*1.0 / stat['n']
	print('Finished calculating saving means')

def calculate_saving_standard_deviations(endpoints, saving_standard_deviations):
	for endpoint_id, endpoint in endpoints.iteritems():
		for cache_id, cache_latency in endpoint['cache_latencies'].iteritems():
			saving = endpoint['data_centre_latency'] - cache_latency
			saving_standard_deviations[cache_id]['standard_deviation'] += (saving - saving_means[cache_id]['mean'])**2
			saving_standard_deviations[cache_id]['n'] += 1
	for cache_id, stat in saving_standard_deviations.iteritems():
		stat['standard_deviation'] = stat['standard_deviation']*1.0 / (stat['n'] - 1)
		stat['standard_deviation'] = math.sqrt(abs(stat['standard_deviation']))
	print('Finished calculating saving standard deviations')

def calculate_request_means(caches, request_means):
	for cache_id, cache in caches.iteritems():
		for request_id in cache['requests']:
			number_of_requests = requests[request_id]['number_of_requests']
			request_means[cache_id]['mean'] += number_of_requests
			request_means[cache_id]['n'] += 1
	
	for cache_id, stat in request_means.iteritems():
		stat['mean'] = stat['mean']*1.0 / stat['n']
	print('Finished calculating request means')

def calculate_request_standard_deviations(caches, request_standard_deviations):
	for cache_id, cache in caches.iteritems():
		for request_id in caches[cache_id]['requests']:
			number_of_requests = requests[request_id]['number_of_requests']
			request_standard_deviations[cache_id]['standard_deviation'] += (number_of_requests - request_means[cache_id]['mean'])**2
			request_standard_deviations[cache_id]['n'] += 1

	for cache_id, stat in request_standard_deviations.iteritems():
		stat['standard_deviation'] = stat['standard_deviation']*1.0 / (stat['n'] - 1)
		stat['standard_deviation'] = math.sqrt(abs(stat['standard_deviation']))
	print('Finished calculating request standard deviations')

def construct_stat_data(saving_means, saving_standard_deviations, request_means, request_standard_deviations):
	for i in range(total_number_of_caches):
		saving_means[i] = {'mean': 0, 'n': 0}
		request_means[i] = {'mean': 0, 'n': 0}
		saving_standard_deviations[i] = {'standard_deviation': 0, 'n': 0}
		request_standard_deviations[i] = {'standard_deviation': 0, 'n': 0}

# Parse data
print('Parsing data...')
data = Parser().process_file('kittens.in')
endpoints = data['endpoints']
caches = data['caches']
requests = data['requests']
number_of_videos = data['V']
number_of_endpoints = data['E']
number_of_request_items = data['R']
total_number_of_caches = data['C']
capacity = data['X']
videos = data['videos']

# Construct data structures for statistics
print('Constructing data structures for statistics...')
saving_means = {}
saving_standard_deviations = {}
request_means = {}
request_standard_deviations = {}
construct_stat_data(saving_means, saving_standard_deviations, request_means, request_standard_deviations)

# Calculate statistics
print('Calculating statistics...')
calculate_saving_means(endpoints, saving_means)
calculate_saving_standard_deviations(endpoints, saving_standard_deviations)
calculate_request_means(caches, request_means)
calculate_request_standard_deviations(caches, request_standard_deviations)

# Make decisions!
for cache_id, cache in caches.iteritems():
	for request_id in cache['requests']:
		if(cache['available'] > AVAILABILITY_THRESHOLD):
			print("Making decision for request " + str(request_id) + " for cache " + str(cache_id))
			if(make_decision(cache_id, cache, request_id, requests[request_id], endpoints)):
				print("Add it!")
				video_id = requests[request_id]['video_id']
				cache['store'].add(video_id)
				cache['available'] -= videos[video_id]
			else:
				print("Soz!")

# Output solution
output = open('solution.txt', 'w')
output.write(str(total_number_of_caches))
output.write('\n')

for cache_id, cache in caches.iteritems():
	for video_id in cache['store']:
		output.write(str(video_id) + " ")
	output.write('\n')

output.close()
