from functools import wraps
import json


def _unwrap_message(trigger, input):
    t = trigger.upper()
    if t == "SNS":
        return input['Records'][0]['Sns']['Message']
    # elif t is "KINESIS"
    else:
        return input


def lambdafy(*setting_args, **setting_kwargs):
    no_args = False
    if len(setting_args) == 1 \
            and not setting_kwargs \
            and callable(setting_args[0]):
        # We were called without args
        func = setting_args[0]
        no_args = True

    def outer(func):
        @wraps(func)
        def aws_lambda_fn(input, context):
            if no_args:
                message = input
            else:
                message = _unwrap_message(setting_args[0], input)
            try:
                message_obj = json.loads(message)
                if isinstance(message_obj, dict):
                    return func(**message_obj)
                elif isinstance(message_obj, list):
                    return func(*message_obj)
                else:
                    return func(message_obj)
            except (ValueError, TypeError):
                # Return as string
                return func(message)
        return aws_lambda_fn

    if no_args:
        return outer(func)
    else:
        return outer
