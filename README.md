# Synthetic Motion Data Generation

This code repository includes synthetic training dataset generation process for the model described in paper: [Deep-Motion-Net: GNN-based volumetric organ shape reconstruction from single-view 2D projections](https://arxiv.org/abs/2407.06692).


## Getting Started

### Installation Instructions

We recommend that you create a new virtual environment for a clean installation of all relevant dependencies.

```
virtualenv smdg
source smdg/bin/activate
pip3 install --no-cache-dir numpy
pip3 install --no-cache-dir itk
pip3 install --no-cache-dir itk-rtk
pip3 install --no-cache-dir pydicom
pip3 install --no-cache-dir SimpleITK
pip3 install --no-cache-dir meshio
```

### Dataset Preparation

Paired sets of organ motion instances (i.e. deformed volumetric meshes in.vtk unstructured grid format) and corresponding kilo-voltage (kV) X-ray images are required for model training/validation. To train and evaluate the model, we use synthetically generated data from [SuPReMo](https://github-pages.ucl.ac.uk/SuPReMo/index.html) toolkit (Surrogate Parameterized Respiratory Motion Model). Plausible patient-specific motion patterns are extracted from 4D-CT images, and new synthetic instances are produced by interpolating and, within reasonable bounds, extrapolating from these with SuPReMo. 

The process is as follows:


#### Step 1 => Package _1_supremo_fit

The SuPReMo toolkit is used to analyse 4D-CT images, which produces a model of the motion present in the images linked to appropriate surrogate signals. 
Before start executing this step, you should first complete the following tasks:

 1. First, generate 4D-CT data (in nii.gz format) based on planning CT dicom images for a given patient case.
 2. Then acquire a surrogate signal by tracking diaphragm from the 4D-CT data using image processing techniques (using auto-thresholding technique).
 3. Next, register this 4D-CT data to a 3D-CBCT image volume (You can use 3D-Slicer toolkit for this).
 4. Subsequently, use these registered 4D-CT data to fit the SuPReMo model.

Once you have completed the above four steps, you must then run main.py file in _1_supremo_fit package. This will return the motion compensated reconstructed 3D-CT (MCR) image volume and the fitted motion model, which are then utilised to simulate new motion states by varying the input surrogate signal. The required parameters are below.

```
python main.py --patient_data_dir *** --reg_4DCT_dir *** --surr_signal_file *** --dynamic_list_file *** --ref_state_file ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.

```--reg_4DCT_dir``` => Root directory to registered 4D-CT (translation only registration with 3D-CBCT image volume) data. This registration can be done using SlicerANTs module in 3D-slicer toolkit.

```--surr_signal_file``` => Original surrogate signal file acquired by for example tracking the diaphragm using the 4D-CT data.

```--dynamic_list_file``` => File that consists of the absolute paths for all registered 4D-CT image volumes.

```--ref_state_file``` => nifti file which acting as the reference state when fitting with SuPReMo. This file should be in reg_4DCT_dir. You can use any registered 3D-CT image volume as the reference state.

For more information about other parameter settings, please look options.py file in _1_supremo_fit package.


#### Step 2 => Package _2_surr_signals_gen

This package is used to generate the different variants of the original surrogate signal. Each point on the curve/signal is randomly perturbed by a value in a predefined range. Extrapolating beyond this range is more likely to cause unrealistic motion and even folding in the resulting images.

```
python main.py --patient_data_dir *** --reg_4DCT_dir *** --surr_signal_file ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.

```--reg_4DCT_dir``` => Root directory to registered 4D-CT data.

```--surr_signal_file``` => Original surrogate signal file acquired by for example tracking the diaphragm using the 4D-CT data.

For more information about other parameter settings, please look options.py file in _2_surr_signals_gen package.


#### Step 3 => Package _3_simulated_data_gen

This package is used to simulate new motion states by varying the input surrogate signals. This step requires the motion-compensated reconstructed 3D-CT (MCR) image volume and the fitted motion model which output from the step 1. Moreover, the generated surrogate signals from step 2.

```
python main.py --patient_data_dir *** --reg_4DCT_dir *** --dynamic_list_file ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.

```--reg_4DCT_dir``` => Root directory to registered 4D-CT data.

```--dynamic_list_file``` => File that consists of the absolute paths for all registered 4D-CT image volumes.


####  Step 4 => Package _4_ref_img_converter

This package is used to convert anatomical coordinate system of the reference 3D-CT image volume compatible with nibabel package.

```
python main.py --patient_data_dir ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.


####  Step 5 => Package _5_simulated_imgs_converter

This package is used to convert anatomical coordinate system of the deformed 3D-CT volumes and their corresponding DVFs compatible with nibabel package.

```
python main.py --patient_data_dir ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.


#### Step 6 => Package _6_deform_meshes_gen

This package is used to generate deformed volumetric mesh configurations corresponding to the simulated deformed 3D-CT volumes.

```
python main.py --patient_data_dir ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.


#### Step 7 => Package _7_copy_meshes_cts

This package is used to opy all deformed 3D-CTs and deformed meshes into two separate folders since this will help to generate DRRs and split train/validation/test for model training.

```
python main.py --patient_data_dir ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.


#### Step 8 => Package _8_drrs_gen

This package is used to generate DRRs for each and every deformed 3D-CT image volumes for a given projection angles.

```
python main.py --patient_data_dir *** --raw_real_kv_dir ***
```
```--patient_data_dir``` => Root directory to store all generated data for a given patient case.

```--raw_real_kv_dir``` => Directory consists of in-treatment kV images for a given scan series in dicom format.


Additional note: To introduce more diversity into the synthetic motion instances and substantially deviate from the original 4D-CT data, we incorporated rigid motions by applying random translations/shifts along the LR, AP, and SI directions of the deformed 3D-CT image volumes. This is also advantageous during testing on real in-treatment kV images, as it reflects the variations in onboard patient setup across different scan series or fractions, which can potentially lead to shifts in the in-treatment kV images.


If you find this code is useful for your research, please consider citing the following paper:

```
@article{wijesinghe2024deep,
  title={Deep-Motion-Net: GNN-based volumetric organ shape reconstruction from single-view 2D projections},
  author={Wijesinghe, Isuru and Nix, Michael and Zakeri, Arezoo and Hokmabadi, Alireza and Al-Qaisieh, Bashar and Gooya, Ali and Taylor, Zeike A},
  journal={arXiv preprint arXiv:2407.06692},
  year={2024}
}
```