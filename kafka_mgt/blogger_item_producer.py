"""Schedule Blogger Item Kafka producer and send to topic."""
from json import dumps
from kafka import KafkaProducer
import schedule
from misc import get_third_party_data as tmdb
from datetime import date

# Create producer that connects of our local instance of kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


def job():
    """Get data from Fast API and send to Kafka topic."""
    date_to_get = date.today()
    period_type = 'day'

    data = tmdb.get_item_data(date=date_to_get, period=period_type)

    producer.send('blogger_item_topic', data)    


if __name__ == "__main__":
    # schedule.every().hour.do(job)
    # schedule.every(1).minutes.do(job)
    schedule.every(15).seconds.do(job)

    while True:
        schedule.run_pending()