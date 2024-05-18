import numpy as np
from simulatorA import simulate_ecocentre
from simulatorA import plot_indicateurs

mean_intervale_ts = 10.7
service_times = {
    2: 9.4,
    3: 6.9,
    5: 4.8,
    7: 3.1,
    10: 1.9
}
total_sim_time = 40000


def main():

    n_robots_list = [2, 3, 5, 7, 10]
    results = {}

    for n_robots in n_robots_list:
        att_ts, n_in_queue, depart_ts, arrival_times = simulate_ecocentre(n_robots)
        plot_indicateurs(att_ts, n_in_queue, depart_ts, arrival_times, f'{n_robots} Robots',n_robots)


        avg_wait_time = np.mean(att_ts)
        n_moy_cam_queue = np.mean(n_in_queue)
        n_cam_min = len(att_ts) / (total_sim_time)
        utilisation = np.mean(att_ts) / mean_intervale_ts

        results[n_robots] = {
            'avg_wait_time': avg_wait_time,
            'n_moy_cam_queue': n_moy_cam_queue,
            'n_cam_min': n_cam_min,
            'utilisation': utilisation
        }

    print(results)



if __name__ == "__main__":
    main()
