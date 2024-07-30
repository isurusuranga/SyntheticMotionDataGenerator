import os
import json
import argparse


class Options(object):
    """This class includes options.
    """

    def __init__(self):
        super(Options, self).__init__()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--log_dir', default='logs', help='Directory to store logs')
        self.parser.add_argument('--name', type=str, default='simulated_data_gen', help='name of the experiment')

        # patient_data_dir => e.g. D:/cmake_nifity_reg_supremo/IDAP775756
        self.parser.add_argument('--patient_data_dir', required=True, help='Root directory to store all generated data '
                                                                           'This includes data when fitting SuPReMo '
                                                                           'and the data generate by varying the '
                                                                           'original surrogate signal. This directory '
                                                                           'also includes SuPReMo.exe as well.')
        # registered 4D-CT data root path
        # 4D-CT data first register with 3D-CBCT image volume before start generating synthetic data
        # this helps to generate DRRs with same FOV of the in-treatment kV x-ray images for a given patient
        # reg_4DCT_dir => e.g. D:/cmake_nifti_reg_supremo/IDAP775756/sim4DCT/CT_CBCT_REGISTRATION/SlicerANTs/transformed_sorted
        self.parser.add_argument('--reg_4DCT_dir', required=True, help='Root directory to registered 4D-CT '
                                                                       '(translation only registration with '
                                                                       '3D-CBCT image volume) data. This registration '
                                                                       'can be done using SlicerANTs module in '
                                                                       '3D-slicer toolkit.')

        # dynamic_list_file is stored in reg_4DCT_dir
        self.parser.add_argument('--dynamic_list_file', required=True, help='File that consists of the absolute paths '
                                                                            'for all registered 4D-CT image volumes.')

    def parse_args(self):
        """Parse input arguments."""
        self.args = self.parser.parse_args()

        self.args.log_dir = os.path.join(os.path.abspath(self.args.log_dir), self.args.name)
        if not os.path.exists(self.args.log_dir):
            os.makedirs(self.args.log_dir)

        # patient_data_dir => e.g. D:/cmake_nifti_reg_supremo/IDAP775756
        self.args.patient_data_dir = os.path.abspath(self.args.patient_data_dir)
        if not os.path.exists(self.args.patient_data_dir):
            os.makedirs(self.args.patient_data_dir)

        self.args.supremo_exe = os.path.join(self.args.patient_data_dir, 'runSupremo.exe')

        self.args.reg_4DCT_dir = os.path.abspath(self.args.reg_4DCT_dir)

        # dynamic_list_file => e.g. D:/cmake_nifity_reg_supremo/IDAP775756/sim4DCT/CT_CBCT_REGISTRATION/SlicerANTs/transformed_sorted/volumes_IDAP775756_fileList.txt
        self.args.dynamic_list_file = os.path.join(self.args.reg_4DCT_dir, self.args.dynamic_list_file)

        # initial supremo fitting results folder. This includes MCR.nii.gz, RCM.nii.gz, etc.
        self.args.supremo_fit_dir = os.path.join(self.args.patient_data_dir, 'outputSupRes')

        self.args.surr_save_dir = os.path.join(self.args.patient_data_dir, 'surrogate_signals')

        self.args.supremo_gen_data_dir = os.path.join(self.args.patient_data_dir, 'gen_data')
        if not os.path.exists(self.args.supremo_gen_data_dir):
            os.makedirs(self.args.supremo_gen_data_dir)

        self.save_dump()

        return self.args

    def save_dump(self):
        """Store all argument values to a json file.
        The default location is logs/expname/config.json.
        """
        if not os.path.exists(self.args.log_dir):
            os.makedirs(self.args.log_dir)
        with open(os.path.join(self.args.log_dir, "synthetic_data_gen_config.json"), "w") as f:
            json.dump(vars(self.args), f, indent=4)
        return
