import os
import sys
module_path = os.path.abspath(os.path.join('..', '..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)
    print(f'Module path {module_path} loaded')
data_path = os.path.abspath(os.path.join('..', '..', 'data'))
print(f'Using data_path: {data_path}')

from ess.datalabs import is_spice_volume_mounted

if is_spice_volume_mounted():
    print(f'SPICE volume ENABLED. Consider use the helpers in ess.datalabs package')
else:
    print(f'SPICE volume DISABLED. Kernels will be provided as data by the user')
