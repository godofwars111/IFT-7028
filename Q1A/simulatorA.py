import matplotlib.pyplot as plt
import numpy as np
import simpy

service_times = {
    2: 9.4,
    3: 6.9,
    5: 4.8,
    7: 3.1,
    10: 1.9
}
total_sim_time = 40000
mean_intervale_ts = 10.7


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



def cumulative_average(data):
    return np.cumsum(data) / np.arange(1, len(data) + 1)



def plot_indicateurs(att_ts, n_in_queue, depart_ts, arrival_times, title,n_robots):
    avg_wait_time = cumulative_average(att_ts)
    n_moy_cam_queue = cumulative_average(n_in_queue)


    n_cam_min = np.arange(1, len(depart_ts) + 1) / depart_ts

    busy_times = np.array(
        [min(service_times[n_robots], depart_ts[i] - arrival_times[i]) for i in range(len(depart_ts))])
    cumulative_busy_time = np.cumsum(busy_times)
    utilisation = cumulative_busy_time / depart_ts

    fig, axs = plt.subplots(4, 1, figsize=(12, 24))

    axs[0].plot(depart_ts, avg_wait_time)
    axs[0].set_title(f' Attente moyen ({title})')
    axs[0].set_xlabel('Temps (minutes)')
    axs[0].set_ylabel('Temps moyen attente (minutes)')

    axs[1].plot(depart_ts, n_moy_cam_queue)
    axs[1].set_title(f'Nombre moyen camion ({title})')
    axs[1].set_xlabel('Temps (minutes)')
    axs[1].set_ylabel('Nombre moyen camion dans la fil')

    axs[2].plot(depart_ts, n_cam_min)
    axs[2].set_title(f'Camion par minute  ({title})')
    axs[2].set_xlabel('Temps (minutes)')
    axs[2].set_ylabel('n_cam_min (Camion par minute)')

    axs[3].plot(depart_ts, utilisation)
    axs[3].set_title(f'Temps utilisation ({title})')
    axs[3].set_xlabel('Temps (minutes)')
    axs[3].set_ylabel('utilisation')
    
    plt.tight_layout()
    plt.show()