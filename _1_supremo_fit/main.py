from _1_supremo_fit.options import Options
from _1_supremo_fit.fit_supremo import SUPREMOFitter


if __name__ == '__main__':
    # 1. First generate 4D-CT data based on planning CT dicom images for a given patient (for example IDAPT775756)
    # using SuPReMo-utils-0.1
    # 2. Then acquire surrogate signal by tracking diaphragm from the 4D-CT data using image processing techniques
    # 3. Next register this 4D-CT data with a 3D-CBCT image volume using 3D-Slicer toolkit
    # 4. Subsequently use these registered 4D-CT data to fit the SuPReMo and generate synthetic dataset
    options = Options().parse_args()

    print('start fitting SuPReMo.......')
    SUPREMOFitter(options).execute()
    print('finish.')






