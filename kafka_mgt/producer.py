"""Schedule Kafka producer and send to topic."""
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
    """Get data from TMDB and send to Kafka topic."""
    time = 'day'

    # Movies day
    data = tmdb.get_trending(time, 'movie')
    data['time_window'] = time
    
    producer.send('topic_test', data)

    # TV day
    tv = tmdb.get_trending(time, 'tv')
    tv['time_window'] = time

    producer.send('topic_test', tv)    

    # Fridays download week trending
    if date.today().weekday() == 4:
        time = 'week'

        # Movies
        data = tmdb.get_trending(time, 'movie')
        data['time_window'] = time
        
        producer.send('topic_test', data)

        # TV
        tv = tmdb.get_trending(time, 'tv')
        tv['time_window'] = time

        producer.send('topic_test', tv)


if __name__ == "__main__":
    schedule.every(1).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)

    while True:
        schedule.run_pending()
