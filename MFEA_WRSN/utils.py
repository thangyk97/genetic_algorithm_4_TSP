import numpy as np

def read_data_wrsn(s)->dict:
    with open(s, 'r') as file:
        # Number of nodes
        num_nodes = int(get_number_of(file.readline())[0])
        # EM
        EM = get_number_of(file.readline())[0]
        # v
        v = get_number_of(file.readline())[0]
        # U
        U = get_number_of(file.readline())[0]
        # PM
        PM = get_number_of(file.readline())[0]
        # Emax
        Emax = get_number_of(file.readline())[0]
        # Emin
        Emin = get_number_of(file.readline())[0]
        # Cordination and p[i]
        file.readline()
        p_information = []
        for _ in range(num_nodes + 1):
            p_information.append(get_number_of(file.readline()))
        cordination = [c[0:-1] for c in p_information]
        p = [c[-1] for c in p_information]
        # Hamilton cycle
        hamilton_cycle = [int(c) for c in file.readline().split() if c.isdigit()]
        # length
        length = get_number_of(file.readline())[0]

    return {
        'num_nodes': num_nodes,
        'EM': EM,
        'v': v,
        'U': U,
        'PM': PM,
        'Emax': Emax,
        'Emin': Emin,
        'cordination': cordination,
        'p': p,
        'hamilton_cycle': hamilton_cycle,
        'length': length,
    }

def get_number_of(s)->list:
    out = []
    for c in s.split():
        try :
            t = float(c)
        except ValueError as _:
            continue
        out.append(t)
    return out

def calculate_distances(cordination)->list:
    n = len(cordination)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = np.sqrt((cordination[i][0] - cordination[j][0])**2 + (cordination[i][1] - cordination[j][1])**2)
    return matrix

def calculate_T(data)->float:
    T = float('inf')
    for pi in data['p']:
        if pi != 0:
            temp = (data['Emax'] - data['Emin']) / (pi)
            if temp < T:
                T = temp
    return T

def get_distance(data, gens)->float:
    distance = 0
    for i in range(len(gens)-1):
        distance += data['distances'][gens[i], gens[i + 1]]
    return distance

def get_max_needed_energy(data, gens)->float:
    _max = 0
    service_station_index = [i for i, v in enumerate(gens) if v == 0]
    # Loop per each part cycle, if car is out of energy in the part cycle, return True
    for i in range(len(service_station_index)-1):
        temp = gens[service_station_index[i]: service_station_index[i+1]]
        part_cycle_distance = 0.0
        # Calculate distance of the part cycle
        for j in range(len(temp) - 1):
            part_cycle_distance += data['distances'][temp[j], temp[j + 1]]
        # Check E' < E
        if ((part_cycle_distance / data['v']) * data['PM']) > _max: 
            _max = ((part_cycle_distance / data['v']) * data['PM'])
    return _max

def get_sum_to_i(data, T)->float:
    _sum = 0
    for i in range(data['num_nodes']):
        _sum += data['p'][i] * T / data['U']
    return _sum

if __name__ == "__main__":
    """Test functions"""
    import os
    d = read_data_wrsn(os.getcwd() + "/../datatsp/situation1.txt")
    print(calculate_T(d))
    # m = calculate_distances([[1,1], [0,0]])
    # print(m)