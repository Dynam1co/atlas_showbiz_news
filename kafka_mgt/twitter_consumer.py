"""Consume Kafka producer. Store in Database and send to Twitter."""
from kafka import KafkaConsumer
from json import loads
from misc import get_third_party_data as mgt
from misc import twitter_mgt as twMgt
import time

if __name__ == "__main__":    
    # Define kafka consumer that contacts with localhost and is suscribed to the topic topic_test
    consumer = KafkaConsumer(
        'twitter_topic',
        bootstrap_servers=['localhost:9092'],
        # auto_offset_reset='earliest',  # Oldest message
        auto_offset_reset='latest',  # Most recent message
        enable_auto_commit=True,
        group_id='my-group-id',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    for event in consumer:
        event_data = event.value    

        for item in event_data:
            twMgt.post_tweet(item)
            mgt.update_twitter_published(item['id'], True)
            
            print(f"Tweet sent: {item['title']}")
            time.sleep(10)
