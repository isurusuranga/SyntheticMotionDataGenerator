import subprocess


class SUPREMOFitter(object):
    def __init__(self, options):
        self.options = options
        self.refState = self.options.ref_state_file
        self.dynamicVolsFile = self.options.dynamic_list_file
        self.surrSignalFile = self.options.orig_surr_sig_path
        self.outRCMFile = self.options.out_RCM
        self.outMCRFile = self.options.out_MCR
        self.outInterMCRDir = self.options.out_inter_MCR_dir
        self.outSimDynDir = self.options.out_sim_dyn_dir
        self.outDVFsDir = self.options.out_DVFs

    def execute(self):
        cmd = self.options.supremo_exe + " "
        refState_arg = "-refState " + self.refState + " "
        dynamic_args = "-dynamic 10 " + self.dynamicVolsFile + " "
        surr_args = "-surr 2 " + self.surrSignalFile + " "
        outRCM = "-outRCM " + self.outRCMFile + " "
        outInterMCR_arg = "-outInterMCR " + self.outInterMCRDir + "/ "
        outMCR = "-outMCR " + self.outMCRFile + " "
        outSimDyn = "-outSimDyn " + self.outSimDynDir + "/ "
        outDVFs = "-outDVFs " + self.outDVFsDir + "/ "
        maxFitIt = "-maxFitIt " + str(self.options.max_fit_it) + " "
        transType = "-transType " + str(self.options.trans_type) + " "
        be = "-be " + str(self.options.be) + " "
        sx = "-sx " + str(self.options.sx) + " "
        mcrType = "-mcrType " + str(self.options.mcr_type) + " "
        maxMCRIt = "-maxMCRIt " + str(self.options.max_mcr_it) + " "
        maxSwitchIt = "-maxSwitchIt " + str(self.options.max_switch_it) + " "
        ln = "-ln " + str(self.options.ln)

        command_str = cmd + refState_arg + dynamic_args + surr_args + outRCM + outInterMCR_arg + outMCR +\
                      outSimDyn + outDVFs + maxFitIt + transType + be + sx + mcrType + maxMCRIt + maxSwitchIt + ln

        p = subprocess.run(command_str, capture_output=True, text=True)
        print(p.stderr)


