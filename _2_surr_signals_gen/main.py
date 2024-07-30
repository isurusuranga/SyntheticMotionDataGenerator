from _2_surr_signals_gen.options import Options
from _2_surr_signals_gen.generate_surr_signals import SurrogateSignalsGenerator


if __name__ == '__main__':

    options = Options().parse_args()

    print('start generating surrogate signals.......')
    SurrogateSignalsGenerator(options).generate()
    print('finish.')






