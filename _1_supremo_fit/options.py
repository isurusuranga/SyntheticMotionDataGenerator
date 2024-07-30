import os
import json
import argparse


class Options(object):
    """This class includes training options.

    It also includes shared options defined in Options.
    """

    def __init__(self):
        super(Options, self).__init__()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--log_dir', default='logs', help='Directory to store logs')
        self.parser.add_argument('--name', type=str, default='_1_supremo_fit', help='name of the experiment')

        # patient_data_dir => e.g. D:/cmake_nifity_reg_supremo/IDAP775756
        self.parser.add_argument('--patient_data_dir', required=True, help='Root directory to store all generated data '
                                                                           'This includes data when fitting SuPReMo '
                                                                           'and the data generate by varying the '
                                                                           'original surrogate signal. This directory '
                                                                           'also includes SuPReMo.exe as well.')
        # registered 4D-CT data root path. This path consists of surrogate signal file, dynamic list file and ref state.
        # 4D-CT data first register with 3D-CBCT image volume before start generating synthetic data
        # this helps to generate DRRs with same FOV of the in-treatment kV x-ray images for a given patient
        # reg_4DCT_dir => e.g. D:/cmake_nifti_reg_supremo/IDAP775756/sim4DCT/CT_CBCT_REGISTRATION/SlicerANTs/transformed_sorted
        self.parser.add_argument('--reg_4DCT_dir', required=True, help='Root directory to registered 4D-CT '
                                                                       '(translation only registration with '
                                                                       '3D-CBCT image volume) data. This registration '
                                                                       'can be done using SlicerANTs module in '
                                                                       '3D-slicer toolkit.')
        # surr_signal_file is stored in reg_4DCT_dir
        self.parser.add_argument('--surr_signal_file', required=True, help='Original surrogate signal file.')

        # dynamic_list_file is stored in reg_4DCT_dir
        self.parser.add_argument('--dynamic_list_file', required=True, help='File that consists of the absolute paths '
                                                                            'for all registered 4D-CT image volumes.')

        # ref_state_file => 4D_0_Linear.nii.gz
        self.parser.add_argument('--ref_state_file', required=True, help='nifti file which acting as the reference '
                                                                         'state when fitting with SuPReMo. This file '
                                                                         'should be in reg_4DCT_dir. You can use any '
                                                                         'registered 3D-CT image volume as the '
                                                                         'reference state.')

        # SUPREMO fitting config
        self.parser.add_argument('--max_fit_it', type=int, default=300, help='Number of supremo model fitting steps')
        self.parser.add_argument('--trans_type', type=int, default=0, help='Transformation type \n'
                                                                           '[0] = B-spline transformation\n'
                                                                           '[1] = Sliding B-spline transformation'
                                                                           '(requires signed distance map)", "<int>")')
        self.parser.add_argument('--be', type=float, default=0.99, help='Weight of the bending energy penalty term')

        self.parser.add_argument('--sx', type=int, default=10, help='Final grid spacing along the x axis in mm')
        self.parser.add_argument('--mcr_type', type=int, default=3, help="Specify type of motion compensated image "
                                                                         "reconstruction, where:\n "
                                                                         "[0] = No motion compensated image "
                                                                         "reconstruction(default)\n "
                                                                         "[1] = Weighted average of deformed dynamic "
                                                                         "images\n "
                                                                         "[2] = Super resolution(iterative back - "
                                                                         "projection) - restart recon\n "
                                                                         "[3] = Super resolution(iterative back - "
                                                                         "projection) - update recon")

        self.parser.add_argument('--max_mcr_it', type=int, default=5, help='Maximum number of iterations to use with '
                                                                           'iterative reconstruction methods')
        self.parser.add_argument('--max_switch_it', type=int, default=10, help='Maximum number of times to iterate '
                                                                               'between motion compensate image '
                                                                               'reconstruction and fitting the '
                                                                               'respiratory correspondence model')
        self.parser.add_argument('--ln', type=int, default=3, help='Number of level image pyramid levels to generate')

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
        if not os.path.exists(self.args.reg_4DCT_dir):
            os.makedirs(self.args.reg_4DCT_dir)

        # ref_state_file => e.g. D:/cmake_nifity_reg_supremo/IDAP775756/sim4DCT/CT_CBCT_REGISTRATION/SlicerANTs/transformed_sorted/4D_0_Linear.nii.gz
        self.args.ref_state_file = os.path.join(self.args.reg_4DCT_dir, self.args.ref_state_file)

        # orig_surr_sig_path => e.g. D:/cmake_nifity_reg_supremo/IDAP775756/sim4DCT/CT_CBCT_REGISTRATION/SlicerANTs/transformed_sorted/surrogate_IDAP775756_ApSi_Zsc.txt
        self.args.orig_surr_sig_path = os.path.join(self.args.reg_4DCT_dir, self.args.surr_signal_file)

        # dynamic_list_file => e.g. D:/cmake_nifity_reg_supremo/IDAP775756/sim4DCT/CT_CBCT_REGISTRATION/SlicerANTs/transformed_sorted/volumes_IDAP775756_fileList.txt
        self.args.dynamic_list_file = os.path.join(self.args.reg_4DCT_dir, self.args.dynamic_list_file)

        # initial supremo fitting results folder. This includes MCR.nii.gz, RCM.nii.gz, etc.
        self.args.supremo_fit_dir = os.path.join(self.args.patient_data_dir, 'outputSupRes')
        if not os.path.exists(self.args.supremo_fit_dir):
            os.makedirs(self.args.supremo_fit_dir)

        self.args.out_inter_MCR_dir = os.path.join(self.args.supremo_fit_dir, 'interMCR')
        if not os.path.exists(self.args.out_inter_MCR_dir):
            os.makedirs(self.args.out_inter_MCR_dir)

        self.args.out_sim_dyn_dir = os.path.join(self.args.supremo_fit_dir, 'SUPREMO_simDynDir')
        if not os.path.exists(self.args.out_sim_dyn_dir):
            os.makedirs(self.args.out_sim_dyn_dir)

        self.args.out_DVFs = os.path.join(self.args.supremo_fit_dir, 'SUPREMO_DVFs')
        if not os.path.exists(self.args.out_DVFs):
            os.makedirs(self.args.out_DVFs)

        self.args.out_RCM = os.path.join(self.args.supremo_fit_dir, 'RCM.nii.gz')
        self.args.out_MCR = os.path.join(self.args.supremo_fit_dir, 'MCR.nii.gz')

        self.save_dump()

        return self.args

    def save_dump(self):
        """Store all argument values to a json file.
        The default location is logs/expname/config.json.
        """
        if not os.path.exists(self.args.log_dir):
            os.makedirs(self.args.log_dir)
        with open(os.path.join(self.args.log_dir, "fit_supremo_config.json"), "w") as f:
            json.dump(vars(self.args), f, indent=4)
        return
