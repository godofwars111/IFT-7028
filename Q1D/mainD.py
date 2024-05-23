
import numpy as np
from simulatorD import simulate_ecocentre
from simulatorD import plot_indicateurs


mean_intervale_ts = 10.7
service_times = {
    2: 9.4,
    3: 6.9,
    5: 4.8,
    7: 3.1,
    10: 1.9
}

warmup_times = {
    2: 6000,
    3: 6000,
    5: 5000,
    7: 4000,
    10: 3000
}


total_sim_time = 40000
initial_warmup_period = 2000


def main():

    n_robots_list = [2, 3, 5, 7, 10]
    warmup_periods = {}


    max_warmup_period = max(warmup_times.values())

    f_results = {}
    for n_robots in n_robots_list:
        att_ts, n_in_queue, depart_ts, arrival_times = simulate_ecocentre(n_robots)

        plot_indicateurs(att_ts, n_in_queue, depart_ts, arrival_times, max_warmup_period,
                        f'{n_robots} Robots',n_robots)


        avg_wait_time = np.mean(att_ts[max_warmup_period:])
        n_moy_cam_queue = np.mean(n_in_queue[max_warmup_period:])
        n_cam_min = len(att_ts[max_warmup_period:]) / (total_sim_time - max_warmup_period)
        utilisation = np.mean(att_ts) / mean_intervale_ts

        f_results[n_robots] = {
            'avg_wait_time': avg_wait_time,
            'n_moy_cam_queue': n_moy_cam_queue,
            'n_cam_min': n_cam_min,
            'utilisation': utilisation
        }

    print("Indicateurs de performance après la période d'échauffement :")
    print(f_results)
    print("Période d'échauffement utilisée pour tous les scénarios :")
    print(max_warmup_period)


if __name__ == "__main__":
    main()