import numpy as np
from simulatorB import simulate_ecocentre
from simulatorB import plot_indicateurs


mean_intervale_ts = 10.7
service_times = {
    2: 9.4,
    3: 6.9,
    5: 4.8,
    7: 3.1,
    10: 1.9
}
total_sim_time = 40000

warmup_times = {
    2: 10000,
    3: 3000,
    5: 2500,
    7: 2000,
    10: 1000
}

def main():

    n_robots_list = [2, 3, 5, 7, 10]
    results = {}
    warmup_periods = {}

    for n_robots in n_robots_list:
        att_ts, n_in_queue, depart_ts, arrival_times = simulate_ecocentre(n_robots)
        plot_indicateurs(att_ts, n_in_queue, depart_ts, arrival_times, f'{n_robots} Robots',n_robots)


        visual_warmup_period = warmup_times[n_robots]

        avg_wait_time = np.mean(att_ts[visual_warmup_period:])
        n_moy_cam_queue = np.mean(n_in_queue[visual_warmup_period:])
        n_cam_min = len(att_ts[visual_warmup_period:]) / (total_sim_time - visual_warmup_period)
        utilisation = np.mean(att_ts) / mean_intervale_ts

        results[n_robots] = {
            'avg_wait_time': avg_wait_time,
            'n_moy_cam_queue': n_moy_cam_queue,
            'n_cam_min': n_cam_min,
            'utilisation': utilisation
        }

        warmup_periods[n_robots] = visual_warmup_period

    print("Indicateurs de performance après la période d'échauffement :")
    print(results)
    print("Périodes d'échauffement déterminées :")
    print(warmup_periods)



if __name__ == "__main__":
    main()
