from _7_copy_meshes_cts.options import Options
from _7_copy_meshes_cts.copy_deformed_cts_meshes import copy_deformed_cts_meshes_dirs


if __name__ == '__main__':

    options = Options().parse_args()

    copy_deformed_cts_meshes_dirs(options)






