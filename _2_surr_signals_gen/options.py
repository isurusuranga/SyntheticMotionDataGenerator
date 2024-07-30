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
        self.parser.add_argument('--name', type=str, default='surrogate_signals_gen', help='name of the experiment')

        # patient_data_dir => e.g. D:/cmake_nifity_reg_supremo/IDAP775756
        self.parser.add_argument('--patient_data_dir', required=True, help='Root directory to store all generated data '
                                                                           'This includes data when fitting SuPReMo '
                                                                           'and the data generate by varying the '
                                                                           'original surrogate signal. This directory '
                                                                           'also includes SuPReMo.exe as well.')

        # acquired surr_signal_file is stored in reg_4DCT_dir.
        self.parser.add_argument('--reg_4DCT_dir', required=True, help='Root directory to registered 4D-CT '
                                                                       '(translation only registration with '
                                                                       '3D-CBCT image volume) data. This registration '
                                                                       'can be done using SlicerANTs module in '
                                                                       '3D-slicer toolkit.')

        self.parser.add_argument('--surr_signal_file', required=True, help='Original surrogate signal file.')

        self.parser.add_argument('--signal_vary_range', type=float, default=0.4,
                                 help='Each point on the surrogate signal is randomly perturbed within the range')

        self.parser.add_argument('--start_point', type=int, default=0, help='Surrogate signal versions start from')
        self.parser.add_argument('--num_surr_signals', type=int, default=10,
                                 help='Number of surrogate signals need to be generated')

    def parse_args(self):
        """Parse input arguments."""
        self.args = self.parser.parse_args()

        self.args.log_dir = os.path.join(os.path.abspath(self.args.log_dir), self.args.name)

        # patient_data_dir => e.g. D:/cmake_nifti_reg_supremo/IDAP775756
        self.args.patient_data_dir = os.path.abspath(self.args.patient_data_dir)

        self.args.reg_4DCT_dir = os.path.abspath(self.args.reg_4DCT_dir)

        # orig_surr_sig_path => e.g. D:/cmake_nifity_reg_supremo/IDAP775756/sim4DCT/CT_CBCT_REGISTRATION/SlicerANTs/transformed_sorted/surrogate_IDAP775756_ApSi_Zsc.txt
        self.args.orig_surr_sig_path = os.path.join(self.args.reg_4DCT_dir, self.args.surr_signal_file)

        self.args.surr_save_dir = os.path.join(self.args.patient_data_dir, 'surrogate_signals')
        if not os.path.exists(self.args.surr_save_dir):
            os.makedirs(self.args.surr_save_dir)

        self.save_dump()

        return self.args

    def save_dump(self):
        """Store all argument values to a json file.
        The default location is logs/experiment_name/config.json.
        """
        if not os.path.exists(self.args.log_dir):
            os.makedirs(self.args.log_dir)
        with open(os.path.join(self.args.log_dir, "surrogate_signals_gen_config.json"), "w") as f:
            json.dump(vars(self.args), f, indent=4)
        return
