from _3_simulated_data_gen.options import Options
from _3_simulated_data_gen.generate_simulated_data import SimulatedDataGenerator


if __name__ == '__main__':

    options = Options().parse_args()

    print('start generating synthetic data.......')
    SimulatedDataGenerator(options).generate()
    print('finish.')






