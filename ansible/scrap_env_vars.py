# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Alexander Drozdov <alexander.drozdov@celadon.ae>

import os

RESERVED_VARS = ['BITBUCKET_COMMIT']

env_dict_with_expanded_paths = {k: os.path.expandvars(v) for k, v in os.environ.items()}

BB_ENV_DICT = {
    k: v for k, v in env_dict_with_expanded_paths.items()
    if k.startswith('BOT_') or k in RESERVED_VARS
}

output_env_file = os.path.join(f'{BB_ENV_DICT["BOT_ROOT_DIR"]}',
                               *['ansible',
                                 'roles',
                                 'deploy',
                                 'build',
                                 f'{BB_ENV_DICT["BOT_PROJECT_NAME"]}.env']
                               )
with open(output_env_file, 'w+') as f:
    f.writelines(f'{k}="{v}"\n' for k, v in BB_ENV_DICT.items())
