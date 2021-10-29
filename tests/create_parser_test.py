import argparse

from compile_dcm2bids_config import _create_parser


def test_create_parser_with_default_args():
    parser = _create_parser()

    assert isinstance(parser, argparse.ArgumentParser)

    expected = "Combine multiple"
    assert parser.description is not None and parser.description.startswith(expected)


def test_create_parser_with_user_provided_parser():
    description = "__CUSTOM_DESCRIPTION__"
    custom_parser = argparse.ArgumentParser(description=description)

    parser = _create_parser(custom_parser)
    assert isinstance(parser, argparse.ArgumentParser)
    assert parser.description == description
