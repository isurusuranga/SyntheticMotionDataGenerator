import os
import subprocess
import glob


class SimulatedDataGenerator(object):
    def __init__(self, options):
        self.options = options
        self.surrSignalTxtFiles = glob.glob(os.path.join(self.options.surr_save_dir, '*.txt'))
        self.inputBasePath = self.options.patient_data_dir
        self.outputBasePath = self.options.supremo_gen_data_dir
        self.mcrPath = os.path.join(self.options.supremo_fit_dir, 'MCR.nii.gz')
        self.rcmPath = os.path.join(self.options.supremo_fit_dir, 'RCM_t00.nii.gz')
        self.dynamicVolsPath = self.options.dynamic_list_file

    def generate(self):
        for i, updatedSurrPath in enumerate(self.surrSignalTxtFiles):
            # get the surrogate signal number
            sigNo = os.path.basename(updatedSurrPath).rsplit('.', 1)[0].rsplit('_', 1)[1]
            # create output folder
            outPath = os.path.join(self.outputBasePath, 'out_change_' + str(sigNo))
            os.mkdir(outPath)

            out_rcm_path = os.path.join(outPath, 'RCM_copy.nii.gz')

            sim_dyn_path = os.path.join(outPath, 'SUPREMO_simDynDir')
            if not os.path.exists(sim_dyn_path):
                os.makedirs(sim_dyn_path)

            out_dvfs_path = os.path.join(outPath, 'SUPREMO_DVFs')
            if not os.path.exists(out_dvfs_path):
                os.makedirs(out_dvfs_path)

            itk_simDyn_path = os.path.join(outPath, 'ITK_simDynDir')
            if not os.path.exists(itk_simDyn_path):
                os.makedirs(itk_simDyn_path)

            itk_dvfs_path = os.path.join(outPath, 'ITK_DVFs')
            if not os.path.exists(itk_dvfs_path):
                os.makedirs(itk_dvfs_path)

            # this folder is to save interpolated mesh points based on DVF image volumes =>
            # Interpolate_Mesh_Points_from_DVFs_nifti script
            deformed_mesh_path = os.path.join(outPath, 'deformedMeshes')
            if not os.path.exists(deformed_mesh_path):
                os.makedirs(deformed_mesh_path)

            cmd = self.options.supremo_exe + " "
            refState_arg = "-refState " + self.mcrPath + " "
            inRCM_arg = "-inRCM " + self.rcmPath + " "
            dynamic_args = "-dynamic 10 " + self.dynamicVolsPath + " "
            surr_args = "-surr 2 " + updatedSurrPath + " "
            outRCM = "-outRCM " + out_rcm_path + " "
            maxFitIt = "-maxFitIt 0 "
            mcrType = "-mcrType 0 "
            maxMCRIt = "-maxMCRIt 0 "
            sx = "-sx 10 "
            outSimDyn = "-outSimDyn " + sim_dyn_path + "/ "
            outDVFs = "-outDVFs " + out_dvfs_path + "/"

            command_str = cmd + refState_arg + inRCM_arg + dynamic_args + surr_args + outRCM + maxFitIt + mcrType + \
                          maxMCRIt + sx + outSimDyn + outDVFs

            p = subprocess.run(command_str, capture_output=True, text=True)
            print(p.stderr)

            # rename simulated dynamic files with prefix change_{i} to recognize uniquely
            for file in os.listdir(sim_dyn_path):
                os.rename(os.path.join(sim_dyn_path, file),
                          os.path.join(sim_dyn_path, 'change_' + str(sigNo) + '_' + file))

            for file in os.listdir(out_dvfs_path):
                os.rename(os.path.join(out_dvfs_path, file),
                          os.path.join(out_dvfs_path, 'change_' + str(sigNo) + '_' + file))
