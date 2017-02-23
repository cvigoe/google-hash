availability_threshold = 10

cache1 = {'requests': [request1, request2, request3], 'store': [], 'available': 100}

saving_means = { 0: {'mean': 0, 'n': 0},  1: {'mean': 0, 'n': 0}, 2: {'mean': 0, 'n': 0} }

caches = [cache1, cache2, cache3]

for cache in caches:
	for request in cache['requests']:
		if(cache['available'] < availability_threshold):
			if(make_decision(cache, request)):
				cache['store'].append(request['video_id'])


def make_decision(cache, request):
	data_center_latency = request['endpoint']['data_centre_latency']
	cache_latency = request['endpoint'][cache['cache_id']]
	saving = data_centre_latency - cache_latency

	z_score = (saving - saving_means['cache_id']['mean']) / saving_standard_deviations['cache_id']
	p_value = scipy.stats.norm.sf(abs(z_score))
	return random.uniform(0, 1) < p_value

def calculate_saving_mean(endpoints, saving_mean):
	for endpoint in endpoints:
		for cache in endpoint['caches']:
			saving_means[cache['cache_id']]['mean'] += (endpoint['data_centre_latency'] - endpoint['cache_id']['cache_latency'])
			saving_means[cache['cache_id']]['n'] += 1

	for stat in saving_means:
		stat['mean'] = stat['mean'] / stat['n']


def calculate_saving_standard_deviation():





def calculate_request_mean():


def calculate_request_standard_deviation():