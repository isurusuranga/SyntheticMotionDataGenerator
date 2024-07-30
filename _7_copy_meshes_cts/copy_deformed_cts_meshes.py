import os
import shutil


def copy_deformed_cts_meshes_dirs(options):

    gen_instances_path = os.path.join(options.patient_data_dir, 'gen_data')
    folder_list = os.listdir(gen_instances_path)

    for i, folder_name in enumerate(folder_list):
        main_folder_path = os.path.join(gen_instances_path, folder_name)

        simulated_folder_path = os.path.join(main_folder_path, 'SUPREMO_simDynDir')
        all_simulated_img_vol_names = [x for x in os.listdir(simulated_folder_path) if x.endswith(".nii.gz")]

        for j, relative_simulated_path in enumerate(all_simulated_img_vol_names):
            source_deformed_CT = os.path.join(simulated_folder_path, relative_simulated_path)
            target_deformed_CT = os.path.join(options.all_deformed_ct_dir, relative_simulated_path)

            shutil.copy(source_deformed_CT, target_deformed_CT)

        simulated_meshes_folder_path = os.path.join(main_folder_path, 'deformedMeshes')
        all_simulated_mesh_names = [x for x in os.listdir(simulated_meshes_folder_path) if x.endswith(".vtk")]

        for index, relative_simulated_mesh_path in enumerate(all_simulated_mesh_names):
            source_deformed_mesh = os.path.join(simulated_meshes_folder_path, relative_simulated_mesh_path)
            target_deformed_mesh = os.path.join(options.all_deformed_meshes_dir, relative_simulated_mesh_path)

            shutil.copy(source_deformed_mesh, target_deformed_mesh)
