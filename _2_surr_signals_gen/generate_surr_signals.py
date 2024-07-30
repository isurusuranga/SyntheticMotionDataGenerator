import os
import numpy as np
import random
import numpy.polynomial.polynomial as poly


class SurrogateSignalsGenerator(object):
    def __init__(self, options):
        self.originalSurrogateSignalsPath = options.orig_surr_sig_path
        self.saveDir = options.surr_save_dir
        self.startPoint = options.start_point
        self.numSurrSignals = options.num_surr_signals
        self.varyRange = options.signal_vary_range

    def generate(self):
        file = open(self.originalSurrogateSignalsPath, "r")

        surr_1 = []
        surr_2 = []

        for line in file:
            # Let's split the line into an array called "fields" using the " " as a separator:
            fields = line.strip().split(" ")

            # and let's extract the data:
            surr_1.append(float(fields[0]))
            surr_2.append(float(fields[1]))

        file.close()

        x = np.arange(1, 11)
        fixed_val = self.varyRange
        dx = 1

        orignal_name_str = os.path.basename(self.originalSurrogateSignalsPath).rsplit('.', 1)[0]

        for cnt in range(self.startPoint, self.numSurrSignals):

            temp_random_point_list = []

            for index in range(0, 10):
                surr_1_temp = random.uniform(surr_1[index] + fixed_val, surr_1[index] - fixed_val)
                temp_random_point_list.append(surr_1_temp)

            # fit a cubic curve for these 10 random points and then interpolate
            coefs = poly.polyfit(x, np.array(temp_random_point_list), 3)
            # interpolate y values as surrogate signal 1 from fitted cubic function
            temp_surr_1_list = poly.polyval(x, coefs)

            temp_surr_2_list = -np.gradient(temp_surr_1_list, dx)

            temp_file_name = orignal_name_str + '_change_' + str(cnt) + '.txt'
            temp_file_path = os.path.join(self.saveDir, temp_file_name)

            data = np.column_stack([temp_surr_1_list, temp_surr_2_list])

            np.savetxt(temp_file_path, data, fmt=['%f', '%f'])

