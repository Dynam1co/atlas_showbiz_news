"""Consume Kafka producer. Store in Database and send to Blogger."""
from kafka import KafkaConsumer
from json import loads
import get_third_party_data as mgt
import twitter_mgt as twMgt
import time
from blogger_post import BlogPost

# Define kafka consumer that contacts with localhost and is suscribed to the topic topic_test
consumer = KafkaConsumer(
    'blogger_item_topic',
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
        # If not exists blog post item create it
        if not mgt.get_item_published_in_blogger(item['tmdb_id']):
            stored_blog_item = mgt.create_blogger_item(item)
            
            # Create post in blogger
            my_post = mgt.create_blogger_post_item(stored_blog_item)

            # Update post url and blog id in blog item table
            mgt.update_blogger_post_item(my_post, str(stored_blog_item['id']))
