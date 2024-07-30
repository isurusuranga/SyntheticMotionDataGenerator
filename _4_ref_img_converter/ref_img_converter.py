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


class RefImageConverter(object):
    def __init__(self, inputFile, outputFolder):
        self.inputFile = inputFile

        inputFileNameWithExt = os.path.basename(self.inputFile)
        self.outputFile = os.path.join(outputFolder, inputFileNameWithExt)

    def convert(self):
        mcr_image = sitk.ReadImage(self.inputFile)
        updated_mcr_image = get_nibabel_compatible_img_from_itk(mcr_image)

        sitk.WriteImage(updated_mcr_image, self.outputFile)
