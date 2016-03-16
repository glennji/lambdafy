import lambdafy


@lambdafy('cloudwatch')
def run_dispatcher(queue_name, sns_topic, dynamo_hash_key, dynamo_range_key, max_in_flight=40):

    in_flight = dynamo.lookup(table, hash_key, range_key).get(field)
    left_in_queue = sqs.get_queue_size(queue_name)

    outstanding = min(max_in_flight - in_flight, left_in_queue)
    for i in xrange(0, outstanding):
        send_sns_message(queue_name.get_message())
