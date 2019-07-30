import configparser
from typing import Any, Mapping

from rozental_as_a_service.config import CONFIG_SECTION_NAME


def get_params_from_config(config_path: str) -> Mapping[str, Any]:
    config = configparser.ConfigParser()
    config.read(config_path)
    if not config.has_section(CONFIG_SECTION_NAME):
        return {}
    params = dict(config[CONFIG_SECTION_NAME])
    if 'processes' in params:
        params['processes'] = int(params['processes'])  # type: ignore
    if 'exclude' in params:
        params['exclude'] = params['exclude'].split(',')  # type: ignore
    if 'exit_zero' in params:
        params['exit_zero'] = params['exit_zero'] == 'True'  # type: ignore
    if 'reorder_vocabulary' in params:
        params['reorder_vocabulary'] = params['reorder_vocabulary'] == 'True'  # type: ignore
    if 'process_dots' in params:
        params['process_dots'] = params['process_dots'] == 'True'  # type: ignore
    if 'verbosity' in params:
        params['verbosity'] = int(params['verbosity'])  # type: ignore
    return params
