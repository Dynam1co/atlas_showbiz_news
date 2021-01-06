"""Schedule Kafka producer and send to topic."""
from json import dumps
from kafka import KafkaProducer
import schedule
import time
import get_third_party_data as tmdb

# Create producer that connects of our local instance of kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def job():
    """Get data from TMDB and send to Kafka topic."""
    data = tmdb.get_trending('day', 'movie')
    producer.send('topic_test', data)


schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)