# Wikipedia Scraper Microservice

A microservice that allows you to request a 2-sentence summary for any Wikipedia article. 

**Utilizes _RabbitMQ_ as the Communication Pipeline**

Code Adapted From: https://www.rabbitmq.com/tutorials/tutorial-six-python.html (7/25/2022)

## How to Request Data:
1. First, make sure you have the 'pika' package downloaded in the root directory of your project, if you haven't done so already.
```
pip install pika
```
2. Also be sure to have [RabbitMQ](https://www.rabbitmq.com/download.html) downloaded to create proper connection channels. 
3. Have the following code in your program: 
```
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')
channel = connection.channel()

result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue
```
4. The type of call that is being done here is called **Remote Procedure Call (RPC)**, where a client sends a request message and a server replies with a response message, all done through a 'callback' queue. 
5. An important distinction with this call would be the 'Correlation ID' which makes sure the response matches with the request. 
6. Import the 'Universally Unique Identifier' package so we can generate unique IDs. 
```
import uuid
```
7. Have the following code to request data, preferably in a function to properly abstract out the code:
```
corr_id = str(uuid.uuid4())
channel.basic_publish(
            exchange='',
            routing_key='wiki_queue',
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=corr_id),
            body=n.encode())
connection.process_data_events(time_limit=None)
return response.decode()
```
## How to Receive Data: 
7. The next segment of code would be a separate function to check the response receive has the same correlation id and to have the response tied to the response so the program can receive the data properly.
8. Have the following code to receive data:
```          
response = None
def on_response(ch, method, props, body):
    if corr_id == props.correlation_id:
          response = body
channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response,
            auto_ack=True)
```
### **Please Note:** All this code is adapted from RabbitMQ tutorials that can be accessed [here](https://www.rabbitmq.com/tutorials/tutorial-six-python.html).

## UML Diagram
![Wiki Scraper Microservice - Activity diagram](https://user-images.githubusercontent.com/74398530/180913303-ad524579-1909-4b88-a0a3-115d44f94e08.png)

