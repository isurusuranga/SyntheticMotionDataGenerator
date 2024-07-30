from _6_deform_meshes_gen.options import Options
from _6_deform_meshes_gen.deform_meshes_gen import DeformMeshesGenerator


if __name__ == '__main__':

    options = Options().parse_args()

    print('start generating deformed meshes......')
    DeformMeshesGenerator(options).generate()
    print('finish.')






