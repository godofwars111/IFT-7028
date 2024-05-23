
import numpy as np
from scipy import stats
from simulatorQ2 import simulate_ecocentre
from simulatorQ2 import calculate_performance


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
n_replications = 50  # Nombre de réplications


warmup_times = {
    2: 6000,
    3: 6000,
    5: 5000,
    7: 4000,
    10: 3000
}


# Fonction pour calculer les Intervales de confiance
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    h = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, mean - h, mean + h

def main():

    n_robots_list = [2, 3, 5, 7, 10]
    results = {n_robots: [] for n_robots in n_robots_list}
    warmup_periods = {}


    for n_robots in n_robots_list:
        att_ts, n_in_queue, depart_ts, arrival_times = simulate_ecocentre(n_robots)
        visual_warmup_period = warmup_times[n_robots]
        warmup_periods[n_robots] = visual_warmup_period


    max_warmup_period = max(warmup_periods.values())


    for n_robots in n_robots_list:
        for _ in range(n_replications):
            att_ts, n_in_queue, depart_ts, arrival_times = simulate_ecocentre(n_robots)
            performance = calculate_performance(att_ts, n_in_queue, depart_ts, max_warmup_period,n_robots)
            results[n_robots].append(performance)


    indicateurs = ['avg_wait_time', 'n_moy_cam_queue', 'n_cam_min', 'utilisation']
    f_results = {indicateur: {} for indicateur in indicateurs}

    for n_robots in n_robots_list:
        performances = np.array(results[n_robots])
        for i, indicateur in enumerate(indicateurs):
            data = performances[:, i]
            mean, ci_bas, ci_haut = confidence_interval(data)
            f_results[indicateur][n_robots] = (mean, ci_bas, ci_haut)


    print("Intervales de confiance (95%) pour les indicateurs de performance après la période d'échauffement :")
    header = "{:<15} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Indicateur", "2 Robots", "3 Robots", "5 Robots", "7 Robots", "10 Robots")
    print(header)
    for indicateur in indicateurs:
        row = [indicateur]
        for n_robots in n_robots_list:
            mean, ci_bas, ci_haut = f_results[indicateur][n_robots]
            row.append(f"{mean:.2f} [{ci_bas:.2f}, {ci_haut:.2f}]")
        print("{:<15} {:<20} {:<20} {:<20} {:<20} {:<20}".format(*row))


if __name__ == "__main__":
    main()
