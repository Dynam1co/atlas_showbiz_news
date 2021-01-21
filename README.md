# Atlas - Showbiz News

With this project I intend to cover various topics and use different current tools.

## Starting 🚀

The basic idea is to get third-party data using Python and Kafka, process that data, store it in DDBB using microservices, and publish Tweets and post in Blogger by reading that data. Everything automatically.

## Used Tools 🛠️
- Docker: for manage Kafka consumers and producers.
- Neovim: as IDE for Python
- Postgre: to store data
- AWS (Rds): to host the database

## Libraries ☔️

- kafka-python: Python client for the Apache Kafka [Git Hub](https://github.com/dpkp/kafka-python).
- FastAPI: Web framework for builgin APIs with Python [Web](https://fastapi.tiangolo.com/)
- Alembic: Manage database migrations. [Documentation](https://alembic.sqlalchemy.org/en/latest/)
- uuid: Generate unique ids. [Documentation](https://docs.python.org/3/library/uuid.html)
- tweepy: Twitter API communication. [Web](https://www.tweepy.org/) 

## References 📖

- Create Docker container with Kafka and Zookeeper: [Towardsdatascience](https://towardsdatascience.com/kafka-docker-python-408baf0e1088).

## License 📄

This project is under GNU license - look at the file [LICENSE.md](LICENSE.md) for more details.

## Use 🧩

Description of the main scripts.

Read third party API:

- [consumer.py](kafka_mgt/consumer.py)
- [producer.py](kafka_mgt/producer.py)



Publish into Twitter:

- [twitter_producer.py](kafka_mgt/twitter_producer.py)
- [twitter_consumer.py](kafka_mgt/twitter_consumer.py)



Publish into Blogger:

- [blogger_item_consumer.py](kafka_mgt/blogger_item_consumer.py)
- [blogger_item_producer.py](kafka_mgt/blogger_item_producer.py)



Blogger token management:

- [blogger_oauth.py](misc/blogger_oauth.py)



Blogger post class:

- [blogger_post.py](misc/blogger_post.py)



Script with common functions:

- [get_third_party_data.py](misc/get_third_party_data.py)



## Acknowledgments 🎁

- Tell others about this project 📢
- Give thanks publicly 🤓
- Follow me on [Twitter](https://twitter.com/AsensiFj) 🐦
