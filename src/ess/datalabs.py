import os
import glob
import re
from datetime import datetime

PATH_VALUES_PATTERN = r'PATH_VALUES\s+=\s+\([^\)]*\)'

def get_kernel_root():
    return '/data/spice/data/SPICE'

def is_spice_volume_mounted():
    return os.path.exists(get_kernel_root())

def check_spice_volume_mounted():
    if not is_spice_volume_mounted():
        raise Exception(f'SPICE volume not mounted. Check the Datalabs environment')

def check_mission_available(name):
    check_spice_volume_mounted()
    available = get_missions()
    if name not in available:
        raise Exception(f'Mission not available.  Try one of {available}')

def get_missions():
    check_spice_volume_mounted()
    return [os.path.basename(path) for path in glob.glob(os.path.join(get_kernel_root(), '*'))]
        
def get_mks(mission):
    check_mission_available(mission)
    return glob.glob(os.path.join(get_kernel_root(), mission, 'kernels', 'mk/**.tm'))

def get_mission_kernel(mission, *path_args):
    check_mission_available(mission)
    path = os.path.join(get_kernel_root(), mission, 'kernels', *path_args)
    if not os.path.exists(path):
        raise Exception(f'Kernel not available at {mission}')
    return path

def get_metakernel_content(mission, metakernel):
    path = get_mission_kernel(mission, 'mk', metakernel)
    with open(path, 'r') as reader:
        return reader.read()
    
def get_local_metakernel(mission, metakernel):
    content = get_metakernel_content(mission, metakernel)
    mission_kernel_path = os.path.join(get_kernel_root(), mission, 'kernels')
    content = re.sub(PATH_VALUES_PATTERN, f"PATH_VALUES = ('{mission_kernel_path}')", content)
    new_path = __get_timestamp() + metakernel
    with open(new_path, 'w') as writer:
        writer.write(content)
    return new_path
    
def __get_timestamp():
    return datetime.now().strftime("%Y%m%dT%H%M%S")