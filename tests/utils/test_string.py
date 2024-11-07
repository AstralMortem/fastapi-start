import pytest
from fastapi_start.utils.string import snake2camel, camel2snake


@pytest.mark.parametrize("input_str, start_lower, expected", [
    ("simple_test", False, "SimpleTest"),
    ("another_example_here", False, "AnotherExampleHere"),
    ("with_numbers_123", False, "WithNumbers123"),
    ("_leading_underscore", False, "LeadingUnderscore"),
    ("double__underscore", False, "DoubleUnderscore"),
    ("one_more_test_case", True, "oneMoreTestCase"),
    ("alreadyCamelCase", False, "Alreadycamelcase"), # unexpected input test
    ("snake_with_number_1_and_letters", True, "snakeWithNumber1AndLetters"),
])
def test_snake2camel(input_str, start_lower, expected):
    assert snake2camel(input_str, start_lower) == expected


@pytest.mark.parametrize("input_str, expected", [
    ("SimpleTest", "simple_test"),
    ("AnotherExampleHere", "another_example_here"),
    ("WithNumbers123", "with_numbers_123"),
    ("LeadingUnderscore", "leading_underscore"),
    ("DoubleUnderscore", "double_underscore"),
    ("alreadyCamelCase", "already_camel_case"),
    ("camelWithNumber1AndLetters", "camel_with_number_1_and_letters"),
    ("smallCamel", "small_camel"),
])
def test_camel2snake(input_str, expected):
    assert camel2snake(input_str) == expected
