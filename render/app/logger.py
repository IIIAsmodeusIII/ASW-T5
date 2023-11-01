import pika
import json
import logging

logging.getLogger("pika").setLevel(logging.ERROR)

class Log:
    def log(self, id, action, payload):
        self.connect()
        self.publish(id, action, payload)
        self.connection.close()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='render_logs'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='players',
                                      exchange_type='topic')

    def publish(self, id, action, payload):
        routing_key = f"player.{action}.{id}"
        message = json.dumps(payload)

        self.channel.basic_publish(exchange='players', routing_key=routing_key, body=message)

class Receive:
    def __init__(self):
        logging.info("Waiting for logs...")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='render_logs'))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='players',exchange_type='topic')
        self.channel.queue_declare('player_for_player_queue', exclusive=True)
        self.channel.queue_bind(exchange='players', queue="player_for_player_queue", routing_key="player.delete.*")
        self.channel.basic_consume(queue='player_for_player_queue',on_message_callback=self.callback)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        logging.info(f"Ended connection with: {body['name']} 👋")
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    Receive()