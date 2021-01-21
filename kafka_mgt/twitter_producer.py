"""Schedule Twitter Kafka producer and send to topic."""
from json import dumps
from kafka import KafkaProducer
from misc import get_third_party_data as tmdb
from datetime import date
import schedule

# Create producer that connects of our local instance of kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


def job():
    """Get data from Fast API and send to Kafka topic."""
    date_to_get = date.today()
    period_type = 'day'

    data = tmdb.get_stored_data(date=date_to_get, period=period_type, tw_published=False)

    producer.send('twitter_topic', data)    


if __name__ == "__main__":    
    # schedule.every(1).minutes.do(job)
    # schedule.every().hour.do(job)
    schedule.every().day.at("12:30").do(job)
    schedule.every().day.at("17:30").do(job)

    while True:
        schedule.run_pending()
