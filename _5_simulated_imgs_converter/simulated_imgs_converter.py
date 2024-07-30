import os
import SimpleITK as sitk
import numpy as np


def get_nibabel_compatible_img_from_itk(itk_image) -> np.ndarray:
    spacing = np.array(itk_image.GetSpacing())
    direction_lps = np.array(itk_image.GetDirection())
    origin_lps = np.array(itk_image.GetOrigin())
    rotation_lps = direction_lps.reshape(3, 3)

    FLIPXY_33 = np.diag([-1, -1, 1])
    rotation_ras = np.dot(FLIPXY_33, rotation_lps)
    rotation_ras_zoom = rotation_ras * spacing
    translation_ras = np.dot(FLIPXY_33, origin_lps)

    voxel_spacing = np.sqrt(np.sum(rotation_ras_zoom * rotation_ras_zoom, axis=0))

    # setup other image physical characteristics
    itk_image.SetOrigin(tuple(translation_ras))
    itk_image.SetSpacing(tuple(voxel_spacing))
    itk_image.SetDirection(tuple(rotation_ras.ravel()))

    return itk_image


class DeformImageConverter(object):
    def __init__(self, dataFolder, endsWithExt='.nii.gz'):
        self.dataFolder = dataFolder
        self.endsWithExt = endsWithExt

    def execute(self, data_folder, output_folder):
        all_img_vol_names = [x for x in os.listdir(data_folder) if x.endswith(".nii.gz")]

        for i, relative_path in enumerate(all_img_vol_names):
            img_vol_path = os.path.join(data_folder, relative_path)

            output_nifti_Path = os.path.join(output_folder, relative_path)

            image = sitk.ReadImage(img_vol_path)
            image_out = get_nibabel_compatible_img_from_itk(image)

            sitk.WriteImage(image_out, output_nifti_Path)

    def convert(self):
        data_folder_paths = os.listdir(self.dataFolder)
        for index, rel_path in enumerate(data_folder_paths):
            abs_folder_path = os.path.join(self.dataFolder, rel_path)
            dvf_input_folder_path = os.path.join(abs_folder_path, 'SUPREMO_DVFs')

            simdyndir_input_folder_path = os.path.join(abs_folder_path, 'SUPREMO_simDynDir')

            dvf_output_folder_path = os.path.join(abs_folder_path, 'ITK_DVFs')
            simdyndir_output_folder_path = os.path.join(abs_folder_path, 'ITK_simDynDir')

            self.execute(dvf_input_folder_path, dvf_output_folder_path)
            self.execute(simdyndir_input_folder_path, simdyndir_output_folder_path)
