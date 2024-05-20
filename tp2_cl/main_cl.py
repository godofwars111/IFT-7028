import simpy
import numpy as np


def truck(env, truck_idx, arrival_time, unload_time, robot):

    # Wait until the truck arrives
    yield env.timeout(arrival_time - env.now)
    print(f"Truck {truck_idx} arrived at {env.now}")
    trucks_times[str(truck_idx)] = dict()
    trucks_times[str(truck_idx)]['arrival'] = env.now

    with robot.request() as request:
        # Request the robot for unloading
        yield request
        #print(f"Truck {truck_idx} starts unloading at {env.now}")
        trucks_times[str(truck_idx)]['unloading_start'] = env.now
        waiting = trucks_times[str(truck_idx)]['unloading_start'] - trucks_times[str(truck_idx)]['arrival']
        trucks_times[str(truck_idx)]['waiting_time'] = waiting

        yield env.timeout(unload_time)
        print(f"Truck {truck_idx} finished unloading at {env.now}")
        trucks_times[str(truck_idx)]['unloading_end'] = env.now
        global nb_unloaded_trucks
        nb_unloaded_trucks += 1


def monitor(env, ressource):
    while True:
        queue_length.append(len(ressource.queue))
        if len(unloaded_trucks_per_minute) == 0:
            unloaded_trucks_per_minute.append(nb_unloaded_trucks)
        else:
            unloaded_trucks_per_minute.append(nb_unloaded_trucks - sum(unloaded_trucks_per_minute))
        # Execute every minute

        yield env.timeout(1)


def get_unloading_time(nb_robots):
    if nb_robots == 2:
        expected_value = 9.4
    elif nb_robots == 3:
        expected_value = 6.9
    elif nb_robots == 5:
        expected_value = 4.8
    elif nb_robots == 7:
        expected_value = 3.1
    elif nb_robots == 10:
        expected_value = 1.9
    else:
        raise Exception('Invalid number of robots')
    return expected_value


def simulate_ecocenter(nb_robots, interval_time):

    unloading_time = get_unloading_time(nb_robots)

    # Initialize the simulation environment
    env = simpy.Environment()

    # Create a robot resource with 1 capacity (only one truck can be unloaded at a time)
    robot = simpy.Resource(env, capacity=1)

    global trucks_times, queue_length, nb_unloaded_trucks, unloaded_trucks_per_minute, nb_unloaded_trucks
    trucks_times = dict()
    queue_length = []
    nb_unloaded_trucks = 0
    unloaded_trucks_per_minute = []

    np.random.seed(42)

    # Generate the list of Truck objects
    arrival = 0
    i = 0
    while arrival < 40000:
        i += 1
        interval = round(np.random.exponential(interval_time))
        service = round(np.random.exponential(unloading_time))
        env.process(truck(env, i, arrival, service, robot))
        arrival += interval

    env.process(monitor(env, robot))

    # Run the simulation
    env.run(until=40000)

    # Remove truck that were not unloaded (they would be unloaded but after maximum minute of simulation)
    occupation = []
    filtered_truck_times = dict()
    for key in trucks_times.keys():
        if 'unloading_end' in trucks_times[key].keys():
            filtered_truck_times[key] = trucks_times[key]
            filtered_truck_times[key]['waiting_time'] = \
                filtered_truck_times[key]['unloading_start'] - \
                filtered_truck_times[key]['arrival']

            start_unloading = trucks_times[str(key)]['unloading_start']
            end_unloading = trucks_times[str(key)]['unloading_end']
            occupation.extend([False] * (start_unloading - len(occupation)))
            occupation.extend([True] * (end_unloading - len(occupation)))

    trucks_times = filtered_truck_times

    return trucks_times, queue_length, occupation, unloaded_trucks_per_minute


def main(nb_reps, nb_robot, interval_time):
    reps_avg_queue_length = []
    reps_avg_waiting = []
    reps_avg_occupation = []
    reps_avg_unloaded_trucks_per_min = []
    for rep in range(nb_reps):
        print(f'Rep: {rep+1}')
        trucks_times, queue_length, occupation, unloaded_trucks_per_minute = simulate_ecocenter(nb_robot, interval_time)

        reps_avg_queue_length.append(sum(queue_length) / len(queue_length))

        truck_waiting_times = [trucks_times[k]['waiting_time'] for k in trucks_times]
        if len(truck_waiting_times) == 0:
            reps_avg_waiting.append(0)
        else:
            reps_avg_waiting.append(sum(truck_waiting_times) / len(truck_waiting_times))

        if len(occupation) == 0:
            reps_avg_occupation.append(0)
        else:
            reps_avg_occupation.append(sum(occupation) / len(occupation))

        reps_avg_unloaded_trucks_per_min.append(sum(unloaded_trucks_per_minute) / len(unloaded_trucks_per_minute))

    print(f'reps_avg_queue_length: {sum(reps_avg_queue_length) / len(reps_avg_queue_length)}')
    print(f'reps_avg_waiting: {sum(reps_avg_waiting) / len(reps_avg_waiting)}')
    print(f'reps_avg_occupation: {sum(reps_avg_occupation) / len(reps_avg_occupation)}')
    print(f'reps_avg_unloaded_trucks_per_min: {sum(reps_avg_unloaded_trucks_per_min) / len(reps_avg_unloaded_trucks_per_min)}')


for nb_robots in [2]:
    main(1, nb_robot=nb_robots, interval_time=10.7)
