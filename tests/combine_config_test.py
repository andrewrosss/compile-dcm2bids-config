from typing import Any
from typing import Dict
from typing import List

import pytest
from compile_dcm2bids_config import combine_config
from compile_dcm2bids_config import DescriptionIdError


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
            {"descriptions": [{}, {"IntendedFor": 0}, {}, {"IntendedFor": 2}]},
        ),
        # one config, descriptin with string IntendedFor
        (
            [{"descriptions": [{}, {"IntendedFor": "a"}, {}, {"IntendedFor": "b"}]}],
            {"descriptions": [{}, {"IntendedFor": "a"}, {}, {"IntendedFor": "b"}]},
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
                    {"IntendedFor": 0},
                    {},
                    {"IntendedFor": 2},
                    {},
                    {},
                    {"IntendedFor": 5},
                    {},
                ],
            },
        ),
        # multiple configs, descriptions with string IntendedFor
        (
            [
                {"descriptions": [{}, {"IntendedFor": "a"}, {}, {"IntendedFor": "b"}]},
                {"descriptions": [{}, {}, {"IntendedFor": "c"}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {"IntendedFor": "a"},
                    {},
                    {"IntendedFor": "b"},
                    {},
                    {},
                    {"IntendedFor": "c"},
                    {},
                ],
            },
        ),
        # one config, descriptions with length-one integer list as IntendedFor
        (
            [{"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": [2]}]}],
            {"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": [2]}]},
        ),
        # one config, descriptions with length-one string list as IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {"IntendedFor": ["a"]},
                        {},
                        {"IntendedFor": ["b"]},
                    ],
                },
            ],
            {"descriptions": [{}, {"IntendedFor": ["a"]}, {}, {"IntendedFor": ["b"]}]},
        ),
        # one config, descriptions with mixed-type (int | int[]) IntendedFor
        (
            [{"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": 2}]}],
            {"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": 2}]},
        ),
        # one config, descriptions with mixed-type (str | str[]) IntendedFor
        (
            [{"descriptions": [{}, {"IntendedFor": ["a"]}, {}, {"IntendedFor": "b"}]}],
            {"descriptions": [{}, {"IntendedFor": ["a"]}, {}, {"IntendedFor": "b"}]},
        ),
        # one config, descriptions with list (int[]) as IntendedFor
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
        # one config, descriptions with list (str[]) as IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {},
                        {"IntendedFor": ["a", "b"]},
                        {},
                        {"IntendedFor": ["c"]},
                    ],
                },
            ],
            {
                "descriptions": [
                    {},
                    {},
                    {"IntendedFor": ["a", "b"]},
                    {},
                    {"IntendedFor": ["c"]},
                ],
            },
        ),
        # multiple configs, descriptions with length-one list (int[]) IntendedFor
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
        # multiple configs, descriptions with length-one list (str[]) IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {"IntendedFor": ["a"]},
                        {},
                        {"IntendedFor": ["b"]},
                    ],
                },
                {"descriptions": [{}, {}, {"IntendedFor": ["c"]}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {"IntendedFor": ["a"]},
                    {},
                    {"IntendedFor": ["b"]},
                    {},
                    {},
                    {"IntendedFor": ["c"]},
                    {},
                ],
            },
        ),
        # multiple configs, descriptions with list (int[]) IntendedFor
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
        # multiple configs, descriptions with list (str[]) IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {},
                        {"IntendedFor": ["a", "b"]},
                        {},
                        {"IntendedFor": ["c"]},
                    ],
                },
                {"descriptions": [{}, {}, {}, {"IntendedFor": ["d", "e"]}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {},
                    {"IntendedFor": ["a", "b"]},
                    {},
                    {"IntendedFor": ["c"]},
                    {},
                    {},
                    {},
                    {"IntendedFor": ["d", "e"]},
                    {},
                ],
            },
        ),
        # multiple configs, descriptions with mixed-type (int | int[]) IntendedFor
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
                    {"IntendedFor": 3},
                    {},
                    {},
                    {},
                    {"IntendedFor": 9},
                    {},
                ],
            },
        ),
        # multiple configs, descriptions with mixed-type (str | str[]) IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {},
                        {"IntendedFor": ["a", "b"]},
                        {},
                        {"IntendedFor": "c"},
                    ],
                },
                {"descriptions": [{}, {}, {}, {"IntendedFor": "d"}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {},
                    {"IntendedFor": ["a", "b"]},
                    {},
                    {"IntendedFor": "c"},
                    {},
                    {},
                    {},
                    {"IntendedFor": "d"},
                    {},
                ],
            },
        ),
        # multiple configs, descriptions with mixed-type
        # (int | str | (int | str)[]) IntendedFor
        (
            [
                {
                    "descriptions": [
                        {},
                        {},
                        {"IntendedFor": [3, "b"]},
                        {},
                        {"IntendedFor": 1},
                    ],
                },
                {"descriptions": [{}, {}, {}, {"IntendedFor": 2}, {}]},
            ],
            {
                "descriptions": [
                    {},
                    {},
                    {"IntendedFor": [3, "b"]},
                    {},
                    {"IntendedFor": 1},
                    {},
                    {},
                    {},
                    {"IntendedFor": 7},
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


@pytest.mark.parametrize(
    ("configs"),
    [
        # ID collision, different configs
        (
            [
                {"descriptions": [{"id": "some-id"}, {}, {}, {}, {}]},
                {"descriptions": [{}, {"id": "some-id"}]},
            ]
        ),
        (
            [
                {"descriptions": [{"id": "some-id"}, {}, {}, {}, {}]},
                {"descriptions": [{}, {"id": "some-id"}, {}]},
                {"descriptions": [{}, {}, {}, {"id": "some-id"}]},
            ]
        ),
        # ID collision, same configs
        (
            [
                {"descriptions": [{"id": "some-id"}, {}, {"id": "some-id"}, {}, {}]},
                {"descriptions": [{}, {}, {}]},
            ]
        ),
    ],
)
def test_combine_configs_with_duplicate_ids_default_behaviour(configs):
    with pytest.raises(DescriptionIdError):
        combine_config(configs)


@pytest.mark.parametrize(
    ("configs"),
    [
        # ID collision, different configs
        (
            [
                {"descriptions": [{"id": "some-id"}, {}, {}, {}, {}]},
                {"descriptions": [{}, {"id": "some-id"}]},
            ]
        ),
        (
            [
                {"descriptions": [{"id": "some-id"}, {}, {}, {}, {}]},
                {"descriptions": [{}, {"id": "some-id"}, {}]},
                {"descriptions": [{}, {}, {}, {"id": "some-id"}]},
            ]
        ),
        # ID collision, same configs
        (
            [
                {"descriptions": [{"id": "some-id"}, {}, {"id": "some-id"}, {}, {}]},
                {"descriptions": [{}, {}, {}]},
            ]
        ),
    ],
)
def test_combine_configs_with_duplicate_ids_and_behaviour_is_raise(configs):
    with pytest.raises(DescriptionIdError):
        combine_config(configs)
