from build import build
import os
import numpy as np
import random
from pytictoc import TicToc

ALL_SATS_FILE = ["..", "active.txt"]
USED_SATS_FILE = ["sats_to_use.txt"]
SAVE_DIR = ["..", "data"]

# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)))
for x in SAVE_DIR:
    save_location = os.path.join(save_location, x)
if not os.path.exists(save_location):
    os.makedirs(save_location)


def mutation(input_string):
    rand_pos = random.randint(0, len(input_string)-1)
    if input_string[0][rand_pos] == 0:
        input_string[:][rand_pos] = 1
    else:
        input_string[:][rand_pos] = 0
    return np.array(input_string)




t = TicToc()

# for j in range(10):
#     input_string = np.full(82, False)

#     for i in range(100):
#         input_string = mutation(input_string)
#         while np.sum(input_string) < 4:
#             input_string = mutation(input_string)
#         t.tic()
#         c_t = build(input_string, primary)
#         t.toc()
######################

from geneticalgorithm import geneticalgorithm as ga

# There are 2^num_sats total combinations

num_iterations = 10
pop_size = 100
mutat = 0.1
# 0.01
# 0.5

algorithm_param = {'max_num_iteration': num_iterations,\
                   'population_size':pop_size,\
                   'mutation_probability':mutat,\
                   'elit_ratio': 0,\
                   'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}

model=ga(function=build,dimension=20,variable_type='bool',algorithm_parameters=algorithm_param)

t.tic()
model.run()
print("-----------")
print("For GA with", num_iterations, "iterations,", pop_size, "population size and", mutat, "mutation probability")
t.toc()

convergence=model.report
solution=model.output_dict

print(convergence)
print(solution)


print(model)

######################

# inputs = np.full((100,82), 0)
# while np.sum(inputs) < 4:
#     inputs = mutation(inputs)

# import pygad
# ga_instance = pygad.GA(num_generations=100,
#                        sol_per_pop=100,
#                        num_genes=82,
#                        num_parents_mating=2,
#                        fitness_func=build,
#                        mutation_type="random",
#                        mutation_probability=0.1,
#                        initial_population=inputs)

# ga_instance.run()

# ga_instance.plot_fitness()
