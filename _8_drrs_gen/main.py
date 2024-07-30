from _8_drrs_gen.options import Options
from _8_drrs_gen.generate_drr_data import DRRGenerator


if __name__ == '__main__':

    options = Options().parse_args()

    print('start generating DRRs.......')
    DRRGenerator(options).generate()
    print('finish.')






