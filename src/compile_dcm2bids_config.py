import argparse
import json
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Union


__version__ = "1.2.0.post0"


def main():
    parser = _create_parser()
    args = parser.parse_args()

    if hasattr(args, "handler"):
        return args.handler(args)

    parser.print_help()


def _create_parser() -> argparse.ArgumentParser:
    description = "Combine multiple dcm2bids config files into a single config file."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "in_file",
        nargs="+",
        type=Path,
        help="The JSON config files to combine",
    )
    parser.add_argument(
        "-o",
        "--out-file",
        type=argparse.FileType("w", encoding="utf8"),
        default="-",
        help="The file to write the combined config file to. If not "
        "specified outputs are written to stdout.",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.set_defaults(handler=_handler)

    return parser


def _handler(args: argparse.Namespace):
    in_files: list[Path] = args.in_file
    out_file: TextIOWrapper = args.out_file
    # load all the config files passed as arguments
    configs = [json.loads(fp.read_text()) for fp in in_files]
    # combine the config files into one config
    combined_config = combine_config(configs)
    # write the combined config file to disk
    with out_file as f:
        # we output like this because json.dump(obj, f) doesn't add a trailing new-line
        f.write(json.dumps(combined_config, indent=2) + "\n")


def combine_config(input_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Combine multiple dcm2bids config dicts into a single config dict.

    Args:
        input_configs (list[dict[str, Any]]): A list of dcm2bids configs (dicts)

    Returns:
        dict[str, Any]: The combined/merged config dict.
    """

    config_collection = ConfigCollection(input_configs)
    return config_collection.combined()


@dataclass
class ConfigCollection:
    configs: List[Dict[str, Any]] = field(default_factory=list)

    def combined(self):
        return {**self.top_level_params(), "descriptions": list(self.descriptions())}

    def top_level_params(self):
        params = {}
        for config in self.configs:
            c = deepcopy(config)
            c.pop("descriptions", None)
            for k, v in c.items():
                if k in params and params[k] != v:
                    raise TopLevelParameterError(k, params[k], v)
                params[k] = v

        return params

    def descriptions(self) -> Iterator[Dict[str, Any]]:
        seen_ids = set()
        offset = 0
        for config in self.configs:
            descriptions: Union[List[Dict[str, Any]], None] = config.get("descriptions")
            if descriptions is None:
                continue
            for description in descriptions:
                desc_id = description.get("id")
                if isinstance(desc_id, str) and desc_id in seen_ids:
                    raise DescriptionIdError(desc_id)
                elif isinstance(desc_id, str):
                    seen_ids.add(desc_id)

                yield update_intended_for(description, offset)

            offset += len(descriptions)


TIntendedFor = Union[int, str, List[Union[int, str]], None]


def update_intended_for(description: Dict[str, Any], offset: int) -> Dict[str, Any]:
    _description = deepcopy(description)
    intended_for: TIntendedFor = _description.get("IntendedFor")
    if intended_for is None:
        return _description
    elif isinstance(intended_for, str):
        _description["IntendedFor"] = intended_for
    elif isinstance(intended_for, int):
        _description["IntendedFor"] = intended_for + offset
    elif isinstance(intended_for, list):
        _intended_for: List[Union[int, str]] = []
        for i in intended_for:
            if isinstance(i, str):
                _intended_for.append(i)
            elif isinstance(i, int):
                _intended_for.append(i + offset)
            else:
                m = f"IntendedFor must be 'int' or 'str'. Found [{_intended_for}]"
                raise ValueError(m)
        _description["IntendedFor"] = _intended_for
    else:
        m = f"IntendedFor must be int, str or (int | str)[]. Found [{intended_for}]"
        raise ValueError(m)

    return _description


class ConfigurationConflictError(ValueError):
    """Conflicting configuration values"""


class TopLevelParameterError(ConfigurationConflictError):
    def __init__(self, parameter, value1, value2):
        self.parameter = parameter
        self.value1 = value1
        self.value2 = value2
        super().__init__(
            f"Cannot reconcile values [{self.value1!r}] and [{self.value2!r}] "
            f"for top-level configuration parameter [{parameter!r}]",
        )


class DescriptionIdError(ConfigurationConflictError):
    def __init__(self, description_id: str):
        self.description_id = description_id
        super().__init__(f"Found multiple descriptions with ID [{description_id!r}]")


if __name__ == "__main__":
    exit(main())
