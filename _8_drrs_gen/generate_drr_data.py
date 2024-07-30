import os
import pydicom as dicom
import itk
from itk import RTK as rtk
import numpy as np


def generate_drrs(inputFile=None, outputFile=None, sid=1000., sdd=1536., gantryAngle=0.,
                  projOffsetX=0., projOffsetY=0., outOfPlaneAngle=0., inPlaneAngle=0.,
                  sourceOffsetX=0., sourceOffsetY=0., dx=512, dy=512):
    CT = itk.imread(inputFile, pixel_type=itk.F)
    # The CT volume is not correct orientation compatible to the RTK convention and point (0,0,0) mm is not in the CT
    # image and this is the default centre of rotation in RTK. Therefore  change the origin and the direction to use
    # RTK convention to get the correct DRR as expected. the input of the Joseph-Filter needs to be oriented in the
    # y-direction. In RTK, the rotation axis is y. changed the direction and the image origin of the image volume to
    # have the volume in the xz-layer in the y-direction. Three rotation angles are used to define the orientation of
    # the detector. The ZXY convention of Euler angles is used for detector orientation where GantryAngle is the
    # rotation around y, OutOfPlaneAngle the rotation around x and InPlaneAngle the rotation around z.

    # change the direction and origin to align with the RTK convention
    CTDirection = np.zeros([3, 3])
    CTDirection[0, 0] = 1.
    CTDirection[1, 2] = 1.
    CTDirection[2, 1] = 1.
    CT.SetDirection(itk.matrix_from_array(CTDirection))
    CT.SetOrigin([CT.GetOrigin()[0], CT.GetOrigin()[2], -CT.GetOrigin()[1]])
    CTarray = itk.array_view_from_image(CT)
    # add 1000 to CT numbers to put air at 0
    CTarray += 1000

    # Defines the image type
    Dimension_CT = 3
    PixelType = itk.F
    ImageType = itk.Image[PixelType, Dimension_CT]

    # Create a stack of empty projection images
    ConstantImageSourceType = rtk.ConstantImageSource[ImageType]
    constantImageSource = ConstantImageSourceType.New()
    # Set origin and spacing based on the Elekta configuration
    constantImageSource.SetOrigin([-204.4, -204.4, 0])
    constantImageSource.SetSpacing([0.8, 0.8, 0.8])
    constantImageSource.SetSize([dx, dy, 1])
    constantImageSource.SetConstant(0.)

    # Defines the RTK geometry object
    geometry = rtk.ThreeDCircularProjectionGeometry.New()

    geometry.AddProjection(sid, sdd, gantryAngle, -projOffsetX, projOffsetY, outOfPlaneAngle, inPlaneAngle,
                           sourceOffsetX, sourceOffsetY)

    REIType = rtk.JosephForwardProjectionImageFilter[ImageType, ImageType]
    rei = REIType.New()

    rei.SetGeometry(geometry)
    rei.SetInput(0, constantImageSource.GetOutput())
    rei.SetInput(1, CT)
    rei.Update()

    Dimension = 3
    OutputPixelType = itk.UC
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    RescaleType = itk.RescaleIntensityImageFilter[ImageType, OutputImageType]
    rescaler = RescaleType.New()
    rescaler.SetOutputMinimum(0)
    rescaler.SetOutputMaximum(255)
    rescaler.SetInput(rei.GetOutput())
    rescaler.Update()

    # Out of some reason, the computed projection is up sided-down.
    # Here we use a FlipImageFilter to flip the images in y direction.
    FlipFilterType = itk.FlipImageFilter[OutputImageType]
    flipFilter = FlipFilterType.New()

    FlipAxesArray = itk.FixedArray[itk.D, 3]()
    FlipAxesArray[0] = 0
    FlipAxesArray[1] = 1
    FlipAxesArray[2] = 0

    flipFilter.SetFlipAxes(FlipAxesArray)
    flipFilter.SetInput(rescaler.GetOutput())
    flipFilter.Update()

    WriteType = itk.ImageFileWriter[OutputImageType]
    writer = WriteType.New()
    writer.SetFileName(outputFile)
    writer.SetInput(flipFilter.GetOutput())
    writer.Update()


class DRRGenerator(object):
    def __init__(self, options):
        self.options = options
        self.dataFolder = self.options.all_deformed_ct_dir
        self.outputFolder = self.options.all_drr_dir
        self.rawRealKVFolder = self.options.raw_real_kv_dir

    def generate(self):

        all_img_vol_names = [x for x in os.listdir(self.dataFolder) if x.endswith(".nii.gz")]

        for i, relative_ct_path in enumerate(all_img_vol_names):
            ct_vol_path = os.path.join(self.dataFolder, relative_ct_path)

            drr_img_name = relative_ct_path.rsplit('.', 2)[0]

            all_real_kv_names = [x for x in os.listdir(self.rawRealKVFolder) if x.endswith(".dcm")]

            for j, relative_kv_path in enumerate(all_real_kv_names):
                kVImgPath = os.path.join(self.rawRealKVFolder, relative_kv_path)
                ds = dicom.dcmread(kVImgPath)

                angle = float(ds.get("PositionerPrimaryAngle"))

                # read FOV origin
                fovOriginX = float(ds.get("FieldOfViewOrigin")[0])
                fovOriginY = float(ds.get("FieldOfViewOrigin")[1])

                drr_img_rel_path = drr_img_name + '_' + str(angle)
                output_drr_path = os.path.join(self.outputFolder, drr_img_rel_path + ".png")

                generate_drrs(inputFile=ct_vol_path, outputFile=output_drr_path, gantryAngle=angle,
                              projOffsetX=fovOriginX, projOffsetY=fovOriginY)
