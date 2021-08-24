from typing import Any
from typing import Dict
from typing import List

import pytest
from compile_dcm2bids_config import combine_config


@pytest.mark.parametrize(
    ["input_configs", "expected_config"],
    [
        # one config, empty description
        ([{"descriptions": []}], {"descriptions": []}),
        # multiple configs, empty descriptions
        ([{"descriptions": []}, {"descriptions": []}], {"descriptions": []}),
        # one config, descriptions without IntendedFor
        ([{"descriptions": [{}, {}]}], {"descriptions": [{}, {}]}),
        # multiple configs, descriptions without IntendedFor
        (
            [{"descriptions": [{}, {}]}, {"descriptions": [{}, {}, {}]}],
            {"descriptions": [{}, {}, {}, {}, {}]},
        ),
        # one config, descriptions with integer IntendedFor
        (
            [{"descriptions": [{}, {"IntendedFor": 0}, {}, {"IntendedFor": 2}]}],
            {"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": [2]}]},
        ),
        # multiple configs, descriptions with integer IntendedFor
        (
            [
                {"descriptions": [{}, {"IntendedFor": 0}, {}, {"IntendedFor": 2}]},
                {"descriptions": [{}, {}, {"IntendedFor": 1}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {"IntendedFor": [0]},
                    {},
                    {"IntendedFor": [2]},
                    {},
                    {},
                    {"IntendedFor": [5]},
                    {},
                ],
            },
        ),
        # one config, descriptions with length-one list as IntendedFor
        (
            [{"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": [2]}]}],
            {"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": [2]}]},
        ),
        # one config, descriptions with mixed-type IntendedFor
        (
            [{"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": 2}]}],
            {"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": [2]}]},
        ),
        # one config, descriptions with list as IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {},
                        {"IntendedFor": [0, 1]},
                        {},
                        {"IntendedFor": [3]},
                    ],
                },
            ],
            {
                "descriptions": [
                    {},
                    {},
                    {"IntendedFor": [0, 1]},
                    {},
                    {"IntendedFor": [3]},
                ],
            },
        ),
        # multiple configs, descriptions with length-one list IntendedFor
        (
            [
                {"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": [2]}]},
                {"descriptions": [{}, {}, {"IntendedFor": [1]}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {"IntendedFor": [0]},
                    {},
                    {"IntendedFor": [2]},
                    {},
                    {},
                    {"IntendedFor": [5]},
                    {},
                ],
            },
        ),
        # multiple configs, descriptions with list IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {},
                        {"IntendedFor": [0, 1]},
                        {},
                        {"IntendedFor": [3]},
                    ],
                },
                {"descriptions": [{}, {}, {}, {"IntendedFor": [1, 4]}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {},
                    {"IntendedFor": [0, 1]},
                    {},
                    {"IntendedFor": [3]},
                    {},
                    {},
                    {},
                    {"IntendedFor": [6, 9]},
                    {},
                ],
            },
        ),
        # multiple configs, descriptions with mixed-type IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {},
                        {"IntendedFor": [0, 3]},
                        {},
                        {"IntendedFor": 3},
                    ],
                },
                {"descriptions": [{}, {}, {}, {"IntendedFor": 4}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {},
                    {"IntendedFor": [0, 3]},
                    {},
                    {"IntendedFor": [3]},
                    {},
                    {},
                    {},
                    {"IntendedFor": [9]},
                    {},
                ],
            },
        ),
    ],
)
def test_combine_configs(
    input_configs: List[Dict[str, Any]],
    expected_config: Dict[str, Any],
):
    output_config = combine_config(input_configs)
    assert output_config == expected_config
