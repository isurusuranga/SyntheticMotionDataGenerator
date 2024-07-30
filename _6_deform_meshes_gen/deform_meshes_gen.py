import os
import numpy as np
import SimpleITK as sitk
import meshio
import copy


class DeformMeshesGenerator(object):
    def __init__(self, options):
        refCTFilePath = os.path.join(options.itk_ref_mcr_dir, 'MCR.nii.gz')
        referenceImg = sitk.ReadImage(refCTFilePath)
        self.referenceImagePhysicalPoints = sitk.PhysicalPointSource(outputPixelType=sitk.sitkVectorFloat64,
                                                                     size=referenceImg.GetSize(),
                                                                     origin=referenceImg.GetOrigin(),
                                                                     spacing=referenceImg.GetSpacing(),
                                                                     direction=referenceImg.GetDirection())

        refMeshPath = os.path.join(options.ref_mesh_dir, 'MCR.vtk')
        self.refMesh = meshio.read(refMeshPath)
        self.dataDir = options.supremo_gen_data_dir

    def generate(self):

        folder_list = os.listdir(self.dataDir)

        for i, folder_name in enumerate(folder_list):
            main_folder_path = os.path.join(self.dataDir, folder_name)
            dvf_folder_path = os.path.join(main_folder_path, 'ITK_DVFs')

            # create a folder to save deformed meshes for each case
            deformed_mesh_path = os.path.join(main_folder_path, 'deformedMeshes')

            if not os.path.exists(deformed_mesh_path):
                os.mkdir(deformed_mesh_path)

            dvf_vol_names = [x for x in os.listdir(dvf_folder_path) if x.endswith(".nii.gz")]

            for j, relative_dvf_path in enumerate(dvf_vol_names):
                dvf_img_path = os.path.join(dvf_folder_path, relative_dvf_path)
                # read dvf image volume which is in nifti format with dim 5
                dvf_image = sitk.ReadImage(dvf_img_path)

                corrected_dvf_image = sitk.Compose(
                    [
                        sitk.VectorIndexSelectionCast(dvf_image, 0, sitk.sitkFloat64),
                        sitk.VectorIndexSelectionCast(dvf_image, 1, sitk.sitkFloat64),
                        sitk.VectorIndexSelectionCast(dvf_image, 2, sitk.sitkFloat64),
                    ]
                )

                # create the SimpleITK representation of the DVF transformation, which differs from the dvf_image
                # generate displacement vector field
                sitk_dvf = sitk.DisplacementFieldTransform(self.referenceImagePhysicalPoints - corrected_dvf_image)

                reference_mesh_duplicate = copy.deepcopy(self.refMesh)

                transformed_physical_points = []

                # transform each point in the mesh using a displacement field
                for index in range(0, reference_mesh_duplicate.points.shape[0]):
                    transformed_physical_points.append(sitk_dvf.TransformPoint(reference_mesh_duplicate.points[index]))

                # convert the list of tuples into 2D numpy array
                list_tuples_to_numpy_2d_array = np.array([*transformed_physical_points])
                # assign transformed points as the new mesh points to teh copy of a reference mesh
                reference_mesh_duplicate.points = list_tuples_to_numpy_2d_array

                dvf_img_name_split = relative_dvf_path.split('DVF', 1)
                new_mesh_name_with_ext = dvf_img_name_split[0] + 'simDyn' + dvf_img_name_split[1].rsplit('.', 2)[
                    0] + '.vtk'
                new_mesh_save_path = os.path.join(deformed_mesh_path, new_mesh_name_with_ext)

                # write new mesh to the disk using meshio
                meshio.write(new_mesh_save_path, reference_mesh_duplicate, binary=False)

