import pika
import wikipedia

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='wiki_queue')


def wiki_scraper(n):
    n = 'the ' + n
    return wikipedia.summary(n, sentences=2)


def on_request(ch, method, props, body):
    response = wiki_scraper(body.decode())

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id =props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='wiki_queue', on_message_callback=on_request)

print(" [x] Waiting for requests...")
channel.start_consuming()
