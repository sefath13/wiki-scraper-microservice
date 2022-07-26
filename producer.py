import pika
import uuid

class WikiScraperRpcClient(object):
# class WikiScraperRpcClient to make an instance

    def __init__(self):
        self.response = None
        self.corr_id = None

        # sets channel and queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)



    # function to make sure correlation ids match to get proper response
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        # makes a unique id
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='wiki_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n.encode())
        self.connection.process_data_events(time_limit=None)
        return self.response.decode()


wiki_rpc = WikiScraperRpcClient()
print("Enter a Wikipedia Search String. Some examples are: US Dollar, Euro, Japanese Yen, etc.")
my_input = input("Search: ")
print(f"[\u2192] Requesting summary for: {my_input}")
response = wiki_rpc.call(my_input)
print("[\u2605] Your Summary: %r" % response)
