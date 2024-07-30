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
        self.parser.add_argument('--name', type=str, default='deformed_meshes_gen', help='name of the experiment')

        # patient_data_dir => e.g. D:/cmake_nifity_reg_supremo/IDAP775756
        self.parser.add_argument('--patient_data_dir', required=True, help='Root directory to store all generated data '
                                                                           'This includes data when fitting SuPReMo '
                                                                           'and the data generate by varying the '
                                                                           'original surrogate signal. This directory '
                                                                           'also includes SuPReMo.exe as well.')

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

        self.args.itk_ref_mcr_dir = os.path.join(self.args.patient_data_dir, 'ITK_REF_MCR')

        self.args.supremo_gen_data_dir = os.path.join(self.args.patient_data_dir, 'gen_data')

        # this folder contains the reference mesh configuration in .vtk format.
        # if the reference mesh doesn't exist in the path, you should copy them or change the ref_mesh_dir path location
        self.args.ref_mesh_dir = os.path.join(self.args.patient_data_dir, 'REF_MESH_GEN/mesh')
        if not os.path.exists(self.args.ref_mesh_dir):
            os.makedirs(self.args.ref_mesh_dir)

        self.save_dump()

        return self.args

    def save_dump(self):
        """Store all argument values to a json file.
        The default location is logs/expname/config.json.
        """
        if not os.path.exists(self.args.log_dir):
            os.makedirs(self.args.log_dir)
        with open(os.path.join(self.args.log_dir, "deform_meshes_gen_config.json"), "w") as f:
            json.dump(vars(self.args), f, indent=4)
        return
