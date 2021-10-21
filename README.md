# compile-dcm2bids-config

Combine [`dcm2bids`](https://github.com/unfmontreal/Dcm2Bids) and [`d2b`](https://github.com/d2b-dev/d2b) config files into a single config file while preserving the integrity of each separate config file's various `IntendedFor` fields.

[![PyPI Version](https://img.shields.io/pypi/v/compile-dcm2bids-config.svg)](https://pypi.org/project/compile-dcm2bids-config/) [![codecov](https://codecov.io/gh/andrewrosss/compile-dcm2bids-config/branch/master/graph/badge.svg?token=BrgPPqwxv4)](https://codecov.io/gh/andrewrosss/compile-dcm2bids-config)
[![Tests](https://github.com/andrewrosss/compile-dcm2bids-config/actions/workflows/test.yaml/badge.svg)](https://github.com/andrewrosss/compile-dcm2bids-config/actions/workflows/test.yaml)
[![Code Style](https://github.com/andrewrosss/compile-dcm2bids-config/actions/workflows/lint.yaml/badge.svg)](https://github.com/andrewrosss/compile-dcm2bids-config/actions/workflows/lint.yaml)
[![Type Check](https://github.com/andrewrosss/compile-dcm2bids-config/actions/workflows/type-check.yaml/badge.svg)](https://github.com/andrewrosss/compile-dcm2bids-config/actions/workflows/type-check.yaml)

## Installation

For the basic functionality:

```bash
pip install compile-dcm2bids-config
```

If you have config files written in YAML you can install the `yaml` extra, for example:

```bash
pip install 'compile-dcm2bids-config[yaml]'
```

## Usage

```bash
$ compile-dcm2bids-config --help
usage: compile-dcm2bids-config [-h] [-o OUT_FILE] [-v] in_file [in_file ...]

Combine multiple dcm2bids config files into a single config file.

positional arguments:
  in_file               The JSON config files to combine

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_FILE, --out-file OUT_FILE
                        The file to write the combined config file to. If not specified
                        outputs are written to stdout.
  -v, --version         show program's version number and exit
```

## Getting Started

Suppose you have two config files:

**`example/config1.json`:**

```json
{
  "descriptions": [
    {
      "dataType": "anat",
      "modalityLabel": "SWI",
      "criteria": {
        "SeriesDescription": "*SWI*"
      }
    },
    {
      "dataType": "fmap",
      "modalityLabel": "fmap",
      "criteria": {
        "SidecarFilename": "*echo-4*"
      },
      "IntendedFor": 0
    }
  ]
}
```

**`example/config2.json`:**

```json
{
  "descriptions": [
    {
      "dataType": "dwi",
      "modalityLabel": "dwi",
      "criteria": {
        "SeriesDescription": "*DWI*"
      }
    },
    {
      "dataType": "anat",
      "modalityLabel": "SWI",
      "criteria": {
        "SeriesDescription": "*SWI*"
      }
    },
    {
      "id": "my-func",
      "dataType": "func",
      "modalityLabel": "bold",
      "customLabels": "task-rest",
      "criteria": {
        "SeriesDescription": "rs_fMRI"
      },
      "sidecarChanges": {
        "SeriesDescription": "rsfMRI"
      }
    },
    {
      "dataType": "fmap",
      "modalityLabel": "fmap",
      "criteria": {
        "SidecarFilename": "*echo-3*"
      },
      "IntendedFor": [0, "my-func"]
    }
  ]
}
```

Then we can combine the two using the following command (outputs are written to stdout by default):

```bash
$ compile-dcm2bids-config example/config1.json example/config2.json
{
  "descriptions": [
    {
      "dataType": "anat",
      "modalityLabel": "SWI",
      "criteria": {
        "SeriesDescription": "*SWI*"
      }
    },
    {
      "dataType": "fmap",
      "modalityLabel": "fmap",
      "criteria": {
        "SidecarFilename": "*echo-4*"
      },
      "IntendedFor": 0
    },
    {
      "dataType": "dwi",
      "modalityLabel": "dwi",
      "criteria": {
        "SeriesDescription": "*DWI*"
      }
    },
    {
      "dataType": "anat",
      "modalityLabel": "SWI",
      "criteria": {
        "SeriesDescription": "*SWI*"
      }
    },
    {
      "id": "my-func",
      "dataType": "func",
      "modalityLabel": "bold",
      "customLabels": "task-rest",
      "criteria": {
        "SeriesDescription": "rs_fMRI"
      },
      "sidecarChanges": {
        "SeriesDescription": "rsfMRI"
      }
    },
    {
      "dataType": "fmap",
      "modalityLabel": "fmap",
      "criteria": {
        "SidecarFilename": "*echo-3*"
      },
      "IntendedFor": [
        2,
        "my-func"
      ]
    }
  ]
}
```

Notice that the `IntendedFor` fields have been updated appropriately.

## Python API

You can also use this tool from within python:

```python
import json
from pathlib import Path
from pprint import pp

from compile_dcm2bids_config import combine_config


config1 = json.loads(Path("example/config1.json").read_text())
config2 = json.loads(Path("example/config2.json").read_text())

all_together = combine_config([config1, config2])

pp(all_together)
```

The result being:

```python
{'descriptions': [{'dataType': 'anat',
                   'modalityLabel': 'SWI',
                   'criteria': {'SeriesDescription': '*SWI*'}},
                  {'dataType': 'fmap',
                   'modalityLabel': 'fmap',
                   'criteria': {'SidecarFilename': '*echo-4*'},
                   'IntendedFor': 0},
                  {'dataType': 'dwi',
                   'modalityLabel': 'dwi',
                   'criteria': {'SeriesDescription': '*DWI*'}},
                  {'dataType': 'anat',
                   'modalityLabel': 'SWI',
                   'criteria': {'SeriesDescription': '*SWI*'}},
                  {'id': 'my-func',
                   'dataType': 'func',
                   'modalityLabel': 'bold',
                   'customLabels': 'task-rest',
                   'criteria': {'SeriesDescription': 'rs_fMRI'},
                   'sidecarChanges': {'SeriesDescription': 'rsfMRI'}},
                  {'dataType': 'fmap',
                   'modalityLabel': 'fmap',
                   'criteria': {'SidecarFilename': '*echo-3*'},
                   'IntendedFor': [2, 'my-func']}]}
```

## YAML Configuration Files

This package can handle [`dcm2bids`](https://github.com/unfmontreal/Dcm2Bids) (or [`d2b`](https://github.com/d2b-dev/d2b)) configuration files written in YAML, the user just has to install the `PyYAML` package, either separately:

```bash
pip install pyyaml
```

or all at once via the installation "extra":

```bash
pip install 'compile-dcm2bids-config[yaml]'
```

If PyYAML is available, then configuration files ending with `.yml` or `.yaml` can be passed as input files:

```bash
compile-dcm2bids-config config1.json config2.yaml > combined.json
```

The combined configuration file can also be formatted as YAML by adding the `--to-yaml` flag:

```bash
compile-dcm2bids-config --to-yaml config1.json config2.yaml > combined.yaml
```

## Contributing

1. Have or install a recent version of `poetry` (version >= 1.1)
1. Fork the repo
1. Setup a virtual environment (however you prefer)
1. Run `poetry install`
1. Run `pre-commit install`
1. Add your changes (adding/updating tests is always nice too)
1. Commit your changes + push to your fork
1. Open a PR
