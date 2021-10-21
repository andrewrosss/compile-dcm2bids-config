from typing import Any
from typing import Dict
from typing import List

import pytest
from compile_dcm2bids_config import combine_config
from compile_dcm2bids_config import DescriptionIdError
from compile_dcm2bids_config import load_config_file
from compile_dcm2bids_config import serialize_config
from compile_dcm2bids_config import TopLevelParameterError
from compile_dcm2bids_config import update_intended_for
from compile_dcm2bids_config import yaml_dumper_factory
from compile_dcm2bids_config import YamlDumpError
from compile_dcm2bids_config import YamlLoadError
from compile_dcm2bids_config import YamlParserNotFoundError


class TestCombineConfigs:
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
                [
                    {
                        "descriptions": [
                            {},
                            {"IntendedFor": "a"},
                            {},
                            {"IntendedFor": "b"},
                        ],
                    },
                ],
                {"descriptions": [{}, {"IntendedFor": "a"}, {}, {"IntendedFor": "b"}]},
            ),
            # multiple configs, descriptions with integer IntendedFor
            (
                [
                    {},  # config w/out descriptions key
                    {"descriptions": [{}, {"IntendedFor": 0}, {}, {"IntendedFor": 2}]},
                    {},  # config w/out descriptions key
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
                    {
                        "descriptions": [
                            {},
                            {"IntendedFor": "a"},
                            {},
                            {"IntendedFor": "b"},
                        ],
                    },
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
                [
                    {
                        "descriptions": [
                            {},
                            {"IntendedFor": [0]},
                            {},
                            {"IntendedFor": [2]},
                        ],
                    },
                ],
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
                {
                    "descriptions": [
                        {},
                        {"IntendedFor": ["a"]},
                        {},
                        {"IntendedFor": ["b"]},
                    ],
                },
            ),
            # one config, descriptions with mixed-type (int | int[]) IntendedFor
            (
                [{"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": 2}]}],
                {"descriptions": [{}, {"IntendedFor": [0]}, {}, {"IntendedFor": 2}]},
            ),
            # one config, descriptions with mixed-type (str | str[]) IntendedFor
            (
                [
                    {
                        "descriptions": [
                            {},
                            {"IntendedFor": ["a"]},
                            {},
                            {"IntendedFor": "b"},
                        ],
                    },
                ],
                {
                    "descriptions": [
                        {},
                        {"IntendedFor": ["a"]},
                        {},
                        {"IntendedFor": "b"},
                    ],
                },
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
                    {
                        "descriptions": [
                            {},
                            {"IntendedFor": [0]},
                            {},
                            {"IntendedFor": [2]},
                        ],
                    },
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
    def test_intended_for_correction(
        self,
        input_configs: List[Dict[str, Any]],
        expected_config: Dict[str, Any],
    ):
        output_config = combine_config(input_configs)
        assert output_config == expected_config

    @pytest.mark.parametrize(
        ("description",),
        [
            ({"IntendedFor": set()},),
            ({"IntendedFor": [set(), dict()]},),
            ({"IntendedFor": YamlParserNotFoundError("test")},),
        ],
    )
    def test_update_intended_for_raises_with_bad_IntendedFor_types(self, description):
        with pytest.raises(ValueError):
            update_intended_for(description, 0)

    @pytest.mark.parametrize(
        ("configs", "expected"),
        [
            (
                [
                    {"a": 1, "descriptions": [{}, {}]},
                    {"descriptions": [{}]},
                ],
                {"a": 1, "descriptions": [{}, {}, {}]},
            ),
            (
                [
                    {"a": 1, "descriptions": [{}]},
                    {"b": 2, "descriptions": [{}]},
                ],
                {"a": 1, "b": 2, "descriptions": [{}, {}]},
            ),
            (
                [
                    {"a": 1, "descriptions": [{}]},
                    {"a": 1, "descriptions": [{}]},
                ],
                {"a": 1, "descriptions": [{}, {}]},
            ),
            (
                [
                    {"a": 1, "descriptions": [{}]},
                    {"a": 2, "descriptions": [{}]},
                ],
                TopLevelParameterError,
            ),
        ],
    )
    def test_top_level_params_are_combined(self, configs, expected):
        if isinstance(expected, dict):
            assert combine_config(configs) == expected
        else:
            with pytest.raises(expected):
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
                    {
                        "descriptions": [
                            {"id": "some-id"},
                            {},
                            {"id": "some-id"},
                            {},
                            {},
                        ],
                    },
                    {"descriptions": [{}, {}, {}]},
                ]
            ),
        ],
    )
    def test_combining_with_duplicate_ids(self, configs):
        with pytest.raises(DescriptionIdError):
            combine_config(configs)


class TestWithMissingYamlPackage:
    def test_yaml_dumper_factory_raises(self, yaml_not_found):
        with pytest.raises(YamlParserNotFoundError):
            yaml_dumper_factory()

    def test_load_config_file_raises(self, yaml_not_found, datadir):
        config_file = datadir / "config3.yaml"
        with pytest.raises(YamlLoadError):
            load_config_file(config_file)

    def test_serialize_config_raises(self, yaml_not_found):
        with pytest.raises(YamlDumpError):
            serialize_config({}, to_yaml=True)
