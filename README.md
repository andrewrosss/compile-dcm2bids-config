# compile-dcm2bids-config

A small script intended to combine `dcm2bids` config files into a single config file while preserving the integrity of each separate config file's various `IntendedFor` fields.

## Usage

```bash
$ compile-dcm2bids-config --help
usage: compile-dcm2bids-config [-h] [-o OUT_FILE] in_file [in_file ...]

Combine multiple dcm2bids config files into a single config file.

positional arguments:
  in_file               The JSON config files to combine

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_FILE, --out-file OUT_FILE
                        The file to write the combined config file to. If not specified outputs are written to stdout.
```

## Getting Started

Suppose you have two config files:

```json
// example/config1.json
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

```json
// example/config2.json
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
      "IntendedFor": 2
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
      "IntendedFor": 4
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
                  {'dataType': 'func',
                   'modalityLabel': 'bold',
                   'customLabels': 'task-rest',
                   'criteria': {'SeriesDescription': 'rs_fMRI'},
                   'sidecarChanges': {'SeriesDescription': 'rsfMRI'}},
                  {'dataType': 'fmap',
                   'modalityLabel': 'fmap',
                   'criteria': {'SidecarFilename': '*echo-3*'},
                   'IntendedFor': 4}]}
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

## TODO

- Add e2e tests
