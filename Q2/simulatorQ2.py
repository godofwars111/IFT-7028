import simpy
import numpy as np

# Paramètres de la simulation
mean_intervale_ts = 10.7
service_times = {
    2: 9.4,
    3: 6.9,
    5: 4.8,
    7: 3.1,
    10: 1.9
}
total_sim_time = 40000  # Durée totale de la simulation en minutes
initial_warmup_period = 2000  # Période d'échauffement initiale
n_replications = 30  # Nombre de réplications

# Processus de génération des camions
def truck_generator(env, intervale_ts, service_time, queue):
    while True:
        yield env.timeout(np.random.exponential(intervale_ts))
        env.process(unload_truck(env, service_time, queue))

# Processus de déchargement/trie des camions
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

# Fonction de simulation
def simulate_ecocentre(n_robots):
    env = simpy.Environment()
    queue = simpy.Resource(env, capacity=1)
    global att_ts, n_in_queue, depart_ts, arrival_times
    att_ts = []
    n_in_queue = []
    depart_ts = []
    arrival_times = []
    env.process(truck_generator(env, mean_intervale_ts, service_times[n_robots], queue))
    env.run(until=total_sim_time)
    return att_ts, n_in_queue, depart_ts, arrival_times

# Fonction pour calculer les indicateurs de performance
def calculate_performance(att_ts, n_in_queue, depart_ts, warmup_period):
    att_ts = np.array(att_ts)
    n_in_queue = np.array(n_in_queue)
    depart_ts = np.array(depart_ts)

    valid_indices = depart_ts > warmup_period
    att_ts = att_ts[valid_indices]
    n_in_queue = n_in_queue[valid_indices]

    avg_wait_time = np.mean(att_ts)
    n_moy_cam_queue = np.mean(n_in_queue)
    n_cam_min = len(att_ts) / (total_sim_time - warmup_period)
    utilisation = np.mean(att_ts) / mean_intervale_ts

    return avg_wait_time, n_moy_cam_queue, n_cam_min, utilisation

