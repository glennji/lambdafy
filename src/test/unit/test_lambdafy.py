import pytest
from moto import mock_sns, mock_sqs

import json
import boto
from lambdafy import lambdafy


def _generate_sns_message(msg):
    # TODO: Use moto
    return {
        "Records": [
            {
                "Sns": {
                    "Message": msg
                }
            }
        ]
    }


@pytest.fixture
def simple_sns_message():
    return _generate_sns_message("World")


@pytest.fixture
def simple_dict_sns_message():
    message = {
        "id": "some_id",
        "name": "My Favourite Name"
    }
    return _generate_sns_message(json.dumps(message))


@pytest.fixture
def simple_list_sns_message():
    message = ["a", "b", "c"]
    return _generate_sns_message(json.dumps(message))


@pytest.fixture
def lambda_context():
    return None


def test_lambdafy(simple_sns_message, lambda_context):
    def test(input):
        print "Hello, {}".format(input)

    lambdafied_fn = lambdafy("SNS")(test)
    lambdafied_fn(simple_sns_message, lambda_context)


def test_lambdafy_decorator(simple_sns_message, lambda_context):
    @lambdafy('sns')
    def test(input):
        print "Wrap it up, {}".format(input)

    test(simple_sns_message, lambda_context)


def test_lambdafy_decorator_no_params(simple_sns_message, lambda_context):
    @lambdafy
    def test(input):
        print "Wrap it up, {}".format(input)

    test(simple_sns_message, lambda_context)


def test_lambdafy_json_message_params(simple_dict_sns_message, lambda_context):
    @lambdafy('sns')
    def test_with_params(id, name):
        print "Hello {}({})".format(name, id)

    test_with_params(simple_dict_sns_message, lambda_context)


def test_lambdafy_json_message_named_params(simple_dict_sns_message, lambda_context):
    @lambdafy('sns')
    def test_with_named_params(name=None, id=None):
        print "Hello {}({})".format(name, id)

    test_with_named_params(simple_dict_sns_message, lambda_context)


def test_lambdafy_json_message_list_params(simple_list_sns_message, lambda_context):
    @lambdafy('sns')
    def test_with_named_params(first, second, third):
        print "Hello {}, {}, {}".format(first, second, third)

    test_with_named_params(simple_list_sns_message, lambda_context)
