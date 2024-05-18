import simpy
import numpy as np

base_mean_intervale_ts = 10.7
service_time_10_robots = 1.9
total_sim_time = 40000
max_warmup_period = 3000
n_replications = 30


def truck_generator(env, intervale_ts, service_time, queue):
    while True:
        yield env.timeout(np.random.exponential(intervale_ts))
        env.process(unload_truck(env, service_time, queue))

def unload_truck(env, service_time, queue):
    arrival_time = env.now
    with queue.request() as request:
        yield request
        yield env.timeout(np.random.exponential(service_time))
        departure_time = env.now
        wait_time = departure_time - arrival_time
        att_ts.append(wait_time)
        n_in_queue.append(len(queue.queue))
        depart_ts.append(departure_time)
        arrival_times.append(arrival_time)


def simulate_ecocentre(intervale_ts):
    env = simpy.Environment()
    queue = simpy.Resource(env, capacity=1)
    global att_ts, n_in_queue, depart_ts, arrival_times
    att_ts = []
    n_in_queue = []
    depart_ts = []
    arrival_times = []
    env.process(truck_generator(env, intervale_ts, service_time_10_robots, queue))
    env.run(until=total_sim_time)
    return att_ts, n_in_queue, depart_ts, arrival_times

