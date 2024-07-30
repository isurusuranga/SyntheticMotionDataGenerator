from _5_simulated_imgs_converter.options import Options
from _5_simulated_imgs_converter.simulated_imgs_converter import DeformImageConverter


if __name__ == '__main__':

    options = Options().parse_args()

    print('converting deformed CT and DVF image volumes.......')
    DeformImageConverter(options.supremo_gen_data_dir).convert()
    print('finish.')






