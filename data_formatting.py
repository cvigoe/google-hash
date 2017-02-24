# Statistics data structures
saving_means = {cache_id: {'mean': 0, 'n': 0}, 
				cache_id: {'mean': 0, 'n': 0}, 
				cache_id: {'mean': 0, 'n': 0}}

saving_standard_deviations = {cache_id: {'standard_deviation': 0, 'n': 0}, 
							  cache_id: {'standard_deviation': 0, 'n': 0}, 
							  cache_id: {'standard_deviation': 0, 'n': 0}}

request_means = {cache_id: {'mean': 0, 'n': 0}, 
				 cache_id: {'mean': 0, 'n': 0}, 
				 cache_id: {'mean': 0, 'n': 0}}

request_standard_deviations = {cache_id: {'standard_deviation': 0, 'n': 0}, 
							   cache_id: {'standard_deviation': 0, 'n': 0}, 
							   cache_id: {'standard_deviation': 0, 'n': 0}}



# Data data structures
endpoints = { endpoint_id: {'cache_latencies': { cache_id: cache_latency, cache_id: cache_latency, cache_id: cache_latency, cache_id: cache_latency }, 'data_centre_latency': 2000},
			  endpoint_id: {'cache_latencies': {}, 'data_centre_latency': 3000},
			  endpoint_id: {'cache_latencies': { cache_id: cache_latency, cache_id: cache_latency }, 'data_centre_latency': 4200},
			  endpoint_id: {'cache_latencies': { cache_id: cache_latency, cache_id: cache_latency, cache_id: cache_latency, cache_id: cache_latency }, 'data_centre_latency': 1100},																	
}
			  
caches = { cache_id: {'store': {}, 'available': availability, 'requests': [request_id, request_id, request_id]},
		   cache_id: {'store': {}, 'available': availability, 'requests': [request_id, request_id, request_id]},
		   cache_id: {'store': {}, 'available': availability, 'requests': [request_id, request_id, request_id]},
		   cache_id: {'store': {}, 'available': availability, 'requests': [request_id, request_id, request_id]},
		   cache_id: {'store': {}, 'available': availability, 'requests': [request_id, request_id, request_id]},
		   cache_id: {'store': {}, 'available': availability, 'requests': [request_id, request_id, request_id]}
}

requests = { request_id: {'number_of_requests': number_of_requests, 'video_id': video_id, 'endpoint': endpoint_id},
		     request_id: {'number_of_requests': number_of_requests, 'video_id': video_id, 'endpoint': endpoint_id},
		     request_id: {'number_of_requests': number_of_requests, 'video_id': video_id, 'endpoint': endpoint_id},
	    	 request_id: {'number_of_requests': number_of_requests, 'video_id': video_id, 'endpoint': endpoint_id},
		     request_id: {'number_of_requests': number_of_requests, 'video_id': video_id, 'endpoint': endpoint_id},
		     request_id: {'number_of_requests': number_of_requests, 'video_id': video_id, 'endpoint': endpoint_id}
}
