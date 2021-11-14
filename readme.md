## Architecture will be separated on multiple sections
- Handling new users’ messages via implementation chat service with websockets or any kind of messengers (Telegram)
- Execute common NLP preprocessing
- For ML inference we will retrieve previous little context from in-memory storage.
- Response to users via notification to specific chat_id

## Key components for implementation
- Chat services workers - receive messages from users and send response to users, also keep websocket connections
- ML inference workers - generate response for user's replica and save message to storage
- Notification workers - send response message to specific running chat service worker)
- Rabbit - store queue data
- Cassandra - store chat messages data
- PostgreSQL - store common rarely changable data
- Redis - store in-memory last users' replicas and info about active websocket connections

[Architecture picture (Miro)](https://miro.com/app/board/o9J_ljDvhis=/)


## Architecture can be fault tolerant and scalable because:
- For each processing workers we can split our reading from queue horizontally
- If something goes wrong inside a specific worker broker will resend a given message to another worker. Because we set acknowledgements for messages.
- Database will be splitted by multiple nodes. SQL implementation will have master node and slave replications - for example, we can use PostgreSQL. For storing the amount of messages data I would recommend to apply NoSQL approach like Cassandra because it has great throughput and scalability right out of the box.
- We can also run multiple worker instances for specific characters if it has some popularity with users.  It will be managed by separation to different topics inside the queue.
- For logging information and retrieving different metrics we can apply SQL queries to ChatMessage table grouped by chat_id. Also, we can prepare trained datasets from Cassandra for improving our existing dialog models separated by characters.

## Critical parts:
- Memory usage for redis. Need to calculate storage for N last users' replicas.
- Long API or ML inference or other kind of rate limits to external API.
- If we have internal inference pipeline we need to manage GPU capability on devices.
- We need to store our chat message safely and in encrypted format.

## Consistent hash algorithm for ML inference routing
- Each ML inference worker by character should be registered on startup in redis with record `character_id` `worker_number`. Before registering we check current active worker by the same character_id and increment `worker_number`. This record should be set with TTL (Time to live) parameter. Worker should ping redis about its existance.
- On previous step we need to find appropriate worker for current `chat_id`, I think we would like to process each new messages of user in the same chat consistently. Then before the sending message to specific queue `inference:{character_id}_{unique_suffix}` we need to find active worker which store and process that `chat_id`. For example, if we have 3 active workers we can calculate `unique_suffix` via `hash(chat_id) %  workers_count`. But it `workers_count` be changed `unique_suffix` will be changed and new messages by `chat_id` will be address to only specific worker.
- If a worker has some problems it must resend message to other available workers with `unique_suffix` calculation and shutdown.


## Recommended tech stack:
- RabbitMQ / (Kafka / Nats) as message broker / queue
- PostgreSQL - for storage rarely updated data (tables User / Character)
- Cassandra -  for storage chat message history and users’ selection characters
- Redis - for storage actual info about addresses running char services and connected user websockets for notification
File storage for binary data (image / video / audio) - S3
- Python or any other kind of language if we want more speed. But here we apply a lot Input/Output communication and then I would recommend to use asyncio implementation for Python
- Docker for deployment process and Kubernetes for flexible scalability


## Required steps for local running
1. Create `.env` file and copy values from `.env.example`.
2. Add your telegram bot API token to `.env` file
3. Add your Hugging face API token to `.env` file
4. Build one python container (for docker layers cache usage):
```
docker-compose build telegram_bot
```
5. Build all python containers:
```
docker-compose build --parallel
```
6. Run all containers (I would suggest to run rabbitmq / cassandra / redis before running python containers, because they take long take to running):
```
docker-compose up -d rabbitmq cassandra redis
docker-compose up notifier telegram_bot nlp_inference nlp_common_preprocessing

# OR

docker-compose up -d
```


## For running tests locally
```
virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.test.txt
python3 -m pytest -s -x tests/utils
```
