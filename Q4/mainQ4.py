import simpy
import numpy as np
from scipy import stats
from simulatorQ4 import simulate_ecocentre



base_mean_intervale_ts = 10.7
service_time_10_robots = 1.9
total_sim_time = 40000
max_warmup_period = 10000
n_replications = 30



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
    utilisation = n_cam_min * service_time_10_robots

    return avg_wait_time, n_moy_cam_queue, n_cam_min, utilisation


def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    h = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, mean - h, mean + h


def main():

    intervale_moy_ts = [10.7, 9.0, 7.5, 6.0, 5.0, 4.0]
    results = {intervale_ts: [] for intervale_ts in intervale_moy_ts}

    for intervale_ts in intervale_moy_ts:
        for _ in range(n_replications):
            att_ts, n_in_queue, depart_ts, arrival_times = simulate_ecocentre(intervale_ts)
            performance = calculate_performance(att_ts, n_in_queue, depart_ts,max_warmup_period)
            results[intervale_ts].append(performance)

    indicateurs = ['avg_wait_time', 'n_moy_cam_queue', 'n_cam_min', 'utilisation']
    f_results = {indicateur: {} for indicateur in indicateurs}

    for intervale_ts in intervale_moy_ts:
        performances = np.array(results[intervale_ts])
        for i, indicateur in enumerate(indicateurs):
            data = performances[:, i]
            mean, ci_bas, ci_haut = confidence_interval(data)
            f_results[indicateur][intervale_ts] = (mean, ci_bas, ci_haut)

    print("Intervales de confiance (95%) pour les indicateur de performance après la période d'échauffement :")
    header = "{:<25} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Indicateur", "10.7 min", "9.0 min", "7.5 min", "6.0 min", "5.0 min", "4.0 min")
    print(header)
    for indicateur in indicateurs:
        row = [indicateur]
        for intervale_ts in intervale_moy_ts:
            mean, ci_bas, ci_haut = f_results[indicateur][intervale_ts]
            row.append(f"{mean:.2f} [{ci_bas:.2f}, {ci_haut:.2f}]")
        print("{:<25} {:<20} {:<20} {:<20} {:<20} {:<20}".format(*row))

    print("\nAnalyse des résultats:")
    for intervale_ts in intervale_moy_ts:
        avg_wait_time, ci_bas, ci_haut = f_results['avg_wait_time'][intervale_ts]
        n_moy_cam_queue, _, _ = f_results['n_moy_cam_queue'][intervale_ts]
        n_cam_min, _, _ = f_results['n_cam_min'][intervale_ts]
        utilisation, _, _ = f_results['utilisation'][intervale_ts]
        print(f"Pour un temps moyen entre arrivées de {intervale_ts} minutes:")
        print(f"  - Temps d'attente moyen: {avg_wait_time:.2f} minutes")
        print(f"  - Nombre moyen de camions dans la queue: {n_moy_cam_queue:.2f}")
        print(f"  - Utilsation: {n_cam_min:.2f} camions par minute")
        print(f"  - Taux d'occupation: {utilisation:.2f}")


if __name__ == "__main__":
    main()