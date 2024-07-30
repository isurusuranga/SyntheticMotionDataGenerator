from _4_ref_img_converter.options import Options
from _4_ref_img_converter.ref_img_converter import RefImageConverter


if __name__ == '__main__':

    options = Options().parse_args()

    print('converting reference CT image volume.......')
    RefImageConverter(options.MCR, options.itk_ref_mcr_dir).convert()
    print('finish.')






