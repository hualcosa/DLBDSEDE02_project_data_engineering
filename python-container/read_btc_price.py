import websocket
import json
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import time

def on_open(ws):
    print('the socket is opened!')

    # subscribing to channel that sends BTC price in USD
    subscribe_message = {
        'type': 'subscribe',
        'channels': [
            {
                'name': 'ticker',
                'product_ids':['BTC-USD']
            }
        ]
    }

    ws.send(json.dumps(subscribe_message))

def on_message(ws, message):
    try:
        # desserializing received message
        message = json.loads(message)
        # formatting message
        stream_message = {
            'sequence_id': message['sequence'],
            'product_id': message['product_id'],
            'price': message['price'],
            'time': message['time']
        }
        
        # Setting kafka consumer
        conf = {'bootstrap.servers': 'localhost:9092'}
        producer = Producer(conf)

        # Sending message to Kafka Topic
        producer.produce(
            topic='btc-usd-price',
            key='BTC',
            value=json.dumps(stream_message),
            callback=delivery_status
        )
        producer.flush()

        # Control the rate in which the producer send messages to the topic (Approx. 2 msgs/second)
        time.sleep(0.5) # 

    except Exception as e:
        print(e)

def delivery_status(err, msg):
    """Reports the delivery status of the message to Kafka."""
    if err is not None:
        print('Message delivery failed:', err)
    else:
        print('Message delivered to', msg.topic(), '[Partition: {}]'.format(msg.partition()))

def create_topic(topic_name):
    '''
    create a kafka topic if it doesn't exist
    '''
    admin_client = AdminClient({'bootstrap.servers': 'localhost:9092'})

    if topic_name in admin_client.list_topics().topics:
        print(f'Topic {topic_name} already exists')
    else:
        new_topic = NewTopic(topic_name, num_partitions=4, replication_factor=2)
        admin_client.create_topics([new_topic])

if __name__ == '__main__':
    # create a topic
    create_topic('btc-usd-price')
    # send data to the topic
    socket = 'wss://ws-feed.exchange.coinbase.com'
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
    ws.run_forever()