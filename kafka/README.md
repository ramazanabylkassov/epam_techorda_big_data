# Kafka Practice – Docker Setup and Topic Creation

## 1. Raising Kafka Using Docker

Kafka is deployed inside a Docker container to simplify setup and ensure a consistent practice environment. The container includes Kafka **2.4.0** and **ZooKeeper**, which is required for this Kafka version.

### 1.1 Create Docker Network

Kafka and other services (e.g., MySQL) communicate over a shared Docker network.

```bash
docker network create bigdata_network
```

### 1.2 Create Kafka Container

The Kafka container is created with exposed ports for:

- ZooKeeper (2181)
- Kafka Broker (9092)
- Kafka Connect REST API (8083)

```bash
docker create --name kafka \
  --network bigdata_network \
  -p 2181:2181 \
  -p 9092:9092 \
  -p 8083:8083 \
  -e ADVERTISED_HOST=192.168.16.1 \
  ofrir119/kafka:2.4.0
```

### 1.3 Start Kafka Container

```bash
docker start kafka
```

### 1.4 Access Kafka Container Shell

All Kafka scripts are executed inside the container.

```bash
docker exec -it kafka bash
```

Kafka is installed in:

```
/opt/kafka_2.12-2.4.0
```

ZooKeeper runs on the default port:

```
localhost:2181
```

---

## 2. Creating Kafka Topics

### 2.1 View Kafka Scripts in the Bin Directory

Kafka management scripts are located in the bin directory.

```bash
ls /opt/kafka_2.12-2.4.0/bin
```

Approximately 25 Kafka-related scripts are available, including:

- `kafka-topics.sh`
- `kafka-console-producer.sh`
- `kafka-console-consumer.sh`

### 2.2 Check the PATH Variable

```bash
echo $PATH
```

If the Kafka bin directory is not included in the PATH, scripts can be executed using their full path.

### 2.3 Check the KAFKA_HOME Environment Variable

```bash
echo $KAFKA_HOME
```

If not set, Kafka is still accessible directly from its installation directory.

### 2.4 Check Existing Kafka Topics

Before creating a new topic, existing topics are listed:

```bash
cd /opt/kafka_2.12-2.4.0/bin
./kafka-topics.sh --zookeeper localhost:2181 --list
```

If no user-defined topics exist, the output may be empty or show only internal topics.

### 2.5 Create a New Kafka Topic

A new topic named `kafka-tst-01` is created with:

- 1 partition
- 1 replication factor (single broker)

```bash
./kafka-topics.sh \
  --zookeeper localhost:2181 \
  --create \
  --topic kafka-tst-01 \
  --partitions 1 \
  --replication-factor 1
```

### 2.6 Verify Topic Creation

```bash
./kafka-topics.sh --zookeeper localhost:2181 --list
```

The output confirms that the topic `kafka-tst-01` was successfully created.

(Optional) Describe the topic:

```bash
./kafka-topics.sh \
  --zookeeper localhost:2181 \
  --describe \
  --topic kafka-tst-01
```

---

## 3. Summary

- Kafka was successfully deployed using Docker.
- Kafka management scripts were accessed from the Kafka bin directory.
- Existing topics were checked before creation.
- A new Kafka topic `kafka-tst-01` was created and verified successfully.

---

## 4. Writing and Reading Kafka Topics

This task demonstrates reading and writing messages to a Kafka topic using Kafka console producer and consumer scripts. All commands were executed inside the Kafka Docker container.

- **Kafka broker endpoint:** `localhost:9092`
- **Kafka topic:** `kafka-tst-01`

### 4.1 Start a Kafka Consumer (Session 1)

To read data from a Kafka topic and write it to standard output, the `kafka-console-consumer.sh` script was used.

```bash
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic kafka-tst-01
```

The consumer waits for incoming messages and remains active until manually stopped.

### 4.2 Start a Kafka Producer (Session 2)

In a second terminal session, a Kafka producer was started using the `kafka-console-producer.sh` script.

```bash
./kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic kafka-tst-01
```

The producer prompts for input using the `>` symbol.

The following message was produced:

```
Hello world! This is Kafka!
```

The message was successfully received by the consumer.

### 4.3 Produce Additional Messages

Additional messages were produced:

```
Event 1
Event 2
Event 3
```

All messages were immediately consumed and displayed by the consumer.

### 4.4 Multiple Producers

A second producer was started in a third terminal session, writing to the same Kafka topic.

```bash
./kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic kafka-tst-01
```

Messages produced by both producers were successfully consumed, confirming that multiple producers can write to the same Kafka topic.

### 4.5 Multiple Consumers

A second consumer was started in a fourth terminal session.

```bash
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic kafka-tst-01
```

When new messages were produced, both consumers received the events. Since no consumer group was specified, each consumer received all messages independently.

### 4.6 Consumer Reading from the Beginning

A new consumer was created to read all events from the beginning of the topic using the `--from-beginning` flag.

```bash
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic kafka-tst-01 \
  --from-beginning
```

All previously produced messages were successfully read.

### 4.7 Delete the Kafka Topic

After stopping all producers and consumers, the Kafka topic was deleted.

```bash
./kafka-topics.sh \
  --zookeeper localhost:2181 \
  --delete \
  --topic kafka-tst-01
```

Kafka returned the following confirmation:

```
Topic kafka-tst-01 is marked for deletion.
```

### 4.8 Verify Topic Deletion

```bash
./kafka-topics.sh --zookeeper localhost:2181 --list
```

The topic was no longer listed, confirming successful deletion.

### 4.9 Summary

- Kafka producers successfully wrote messages to the topic
- Kafka consumers successfully read messages from the topic
- Multiple producers and consumers were supported
- Consumers without a consumer group received all messages
- A consumer was able to read messages from the beginning of the topic
- The Kafka topic was successfully deleted

### Questions and Answers

- Multiple producers can write to the same Kafka topic.
- Multiple consumers can read from the same topic.
- Without a consumer group, all consumers receive all messages.
- Round-robin distribution occurs only when consumers belong to the same consumer group.

---

## 5. Using Kafka Connect to Read from a Source File

This task demonstrates the use of **Kafka Connect (Standalone mode)** to read data from a local file and publish it to a Kafka topic using a FileStream source connector. All commands were executed inside the Kafka Docker container.

### 5.1 Create Required Directories

The following directories were created for Kafka Connect configuration, source files, and sink files:

```bash
mkdir -p /kafka/{confFiles,srcFiles,sinkFiles}
```

Directory creation was verified using:

```bash
ls -l /kafka/
```

The output confirmed the presence of `confFiles`, `srcFiles`, and `sinkFiles`.

### 5.2 Create Kafka Connect Source Configuration File

A Kafka Connect source configuration file was created using the vi editor.

**File location:**

```
/kafka/confFiles/connect-file-source.properties
```

**File contents:**

```properties
#--------------------------------------------------
# Content of connect-file-source.properties
#--------------------------------------------------

name=kafka-file-source-task
connector.class=org.apache.kafka.connect.file.FileStreamSourceConnector
tasks.max=1
file=/kafka/srcFiles/sourceFile.log
topic=kafka-file-topic
```

The file was saved and closed using `ESC :wq`.

### 5.3 Insert Records into the Source File

Several records were appended to the source file to simulate incoming events:

```bash
echo 'Event 1 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/sourceFile.log
sleep 1
echo 'Event 2 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/sourceFile.log
sleep 1
echo 'Event 3 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/sourceFile.log
```

The contents of the file were verified using:

```bash
cat /kafka/srcFiles/sourceFile.log
```

### 5.4 Run Kafka Connect in Standalone Mode

Kafka Connect was started in standalone mode using the Kafka Connect configuration and the file source connector configuration.

```bash
./connect-standalone.sh \
  /opt/kafka_2.12-2.4.0/config/connect-standalone.properties \
  /kafka/confFiles/connect-file-source.properties
```

The process produced multiple INFO and WARNING messages, which were expected. The process remained running without errors.

### 5.5 Create a Consumer to Read from the Topic

A Kafka consumer was created to read all messages from the beginning of the topic used by the source connector.

```bash
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic kafka-file-topic \
  --from-beginning
```

All previously written file records were successfully displayed on the consumer's standard output.

### 5.6 Append Additional Records to the Source File

More records were added to the source file:

```bash
echo 'Event 1 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/sourceFile.log
sleep 1
echo 'Event 2 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/sourceFile.log
sleep 1
echo 'Event 3 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/sourceFile.log
```

The consumer immediately received and displayed the new events, confirming real-time file monitoring by Kafka Connect.

### 5.7 Verify Kafka Topics

Kafka topics were listed to ensure the topic created by Kafka Connect exists:

```bash
./kafka-topics.sh --zookeeper localhost:2181 --list
```

The topic `kafka-file-topic` was present in the list.

### 5.8 Stop Processes

Both the Kafka Connect process and the Kafka consumer were stopped using `Ctrl + C`.

The Kafka topic was not deleted, as required by the task instructions.

### 5.9 Summary

- Kafka Connect Standalone mode was used successfully
- A FileStreamSource connector read data from a local file
- File records were published to a Kafka topic
- A Kafka consumer read all events from the beginning of the topic
- Newly appended file records were consumed in real time
- The Kafka topic remained available after stopping the processes

---

## 6. Using Kafka Connect to Write to a Destination File

This task demonstrates the use of **Kafka Connect (Standalone mode)** to read data from a source file, publish it to a Kafka topic, and write the same data to a destination (sink) file using FileStream source and sink connectors. All commands were executed inside the Kafka Docker container.

### 6.1 Update Kafka Connect Source Configuration

The existing source configuration file was overwritten to define a new source file and a new Kafka topic.

**File location:**

```
/kafka/confFiles/connect-file-source.properties
```

**File contents:**

```properties
#--------------------------------------------------
# Content of connect-file-source.properties
#--------------------------------------------------

name=kafka-file-source-task-2
connector.class=org.apache.kafka.connect.file.FileStreamSourceConnector
tasks.max=1
file=/kafka/srcFiles/newSourceFile.log
topic=kafka-file-sink-topic
```

The file was saved and closed using `ESC :wq`.

### 6.2 Create Kafka Connect Sink Configuration

A sink configuration file was created to write Kafka topic data to a local file.

**File location:**

```
/kafka/confFiles/connect-file-sink.properties
```

**File contents:**

```properties
#--------------------------------------------------
# Content of connect-file-sink.properties
#--------------------------------------------------

name=kafka-file-sink-task
connector.class=org.apache.kafka.connect.file.FileStreamSinkConnector
tasks.max=1
file=/kafka/sinkFiles/targetFile.log
topics=kafka-file-sink-topic
```

### 6.3 Write Data to the New Source File

Initial events were written to the new source file:

```bash
echo 'Event 1 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/newSourceFile.log
sleep 1
echo 'Event 2 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/newSourceFile.log
sleep 1
echo 'Event 3 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/newSourceFile.log
```

The file contents were verified using:

```bash
cat /kafka/srcFiles/newSourceFile.log
```

### 6.4 Create the Target (Sink) File

The destination file for the sink connector was created manually:

```bash
touch /kafka/sinkFiles/targetFile.log
```

### 6.5 Run Kafka Connect in Standalone Mode (Source + Sink)

Kafka Connect was started with both the source and sink configurations:

```bash
./connect-standalone.sh \
  /opt/kafka_2.12-2.4.0/config/connect-standalone.properties \
  /kafka/confFiles/connect-file-source.properties \
  /kafka/confFiles/connect-file-sink.properties
```

The process produced multiple INFO and WARNING messages, which were expected. Kafka Connect remained running without errors.

### 6.6 Verify Data in the Destination File

The destination file was checked to ensure that data was written successfully:

```bash
cat /kafka/sinkFiles/targetFile.log
```

The events from the source file were present in the target file.

### 6.7 Create a Consumer to Read from the Topic

A Kafka consumer was created to read all messages from the topic used by Kafka Connect, starting from the beginning:

```bash
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic kafka-file-sink-topic \
  --from-beginning
```

All events were successfully displayed on the screen.

### 6.8 Verify Kafka Topics

Kafka topics were listed to confirm the existence of the topic used in this task:

```bash
./kafka-topics.sh --zookeeper localhost:2181 --list
```

The topic `kafka-file-sink-topic` appeared in the list.

### 6.9 Insert Additional Records into the Source File

More records were appended to the source file:

```bash
echo 'Event 1 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/newSourceFile.log
sleep 1
echo 'Event 2 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/newSourceFile.log
sleep 1
echo 'Event 3 | ' $(hostname) ' | ' $(date) >> /kafka/srcFiles/newSourceFile.log
```

All new records were immediately written to the destination file and consumed from the Kafka topic.

### 6.10 Generate Events for 30 Seconds

A script was executed to continuously generate events for 30 seconds:

```bash
for v in {1..30}; do
  echo Event-$v '-' `date` >> /kafka/srcFiles/newSourceFile.log && sleep 1
done
```

While the script was running, the destination file was monitored:

```bash
cat /kafka/sinkFiles/targetFile.log
```

Events were appended in real time.

### 6.11 Final State

At the end of the task:

- Kafka Connect (source and sink) remained running
- The Kafka consumer remained active
- The Kafka topic was not deleted

### 6.12 Summary

- Kafka Connect was configured with both FileStream source and sink connectors
- Data flowed from a source file to a Kafka topic and then to a destination file
- A Kafka consumer successfully read all topic messages from the beginning
- New events were processed and written in real time
- All required processes were left running as instructed

---

## 7. Kafka Administration

This task focuses on Kafka administration and monitoring activities. It builds upon the previous Kafka Connect file source and sink tasks and assumes that Kafka Connect, consumers, and producers are still active. All commands were executed inside the Kafka Docker container.

### 7.1 List Kafka Consumer Groups

Kafka consumer groups were listed using the following command:

```bash
./kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list
```

The output displayed multiple consumer groups, including groups created by:

- Kafka Connect sink connector
- Console consumers

This confirmed that Kafka tracks consumers through consumer groups.

### 7.2 Inspect Consumer Groups and Offsets

One of the consumer groups was inspected to view its offsets and lag information:

```bash
./kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group connect-kafka-file-sink-task
```

The output showed:

- Topic name
- Partition number
- Current committed offset
- Log end offset
- Lag

This confirmed how Kafka tracks message consumption progress per consumer group.

### 7.3 Run Consumers with Different Consumer Groups

A new consumer was started with a different consumer group name:

```bash
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic kafka-file-sink-topic \
  --group test-admin-group \
  --from-beginning
```

The consumer successfully read all messages from the beginning of the topic. A new consumer group appeared in the list of consumer groups, confirming that each consumer group maintains independent offsets.

### 7.4 Install curl Utility

The curl tool was installed in the environment to interact with the Kafka Connect REST API:

```bash
apk add curl
```

### 7.5 Use Kafka Connect REST API

Kafka Connect REST API (port 8083) was used to retrieve administrative information. All outputs were formatted using Python's json.tool for readability.

**List Running Connectors:**

```bash
curl localhost:8083/connectors | python -m json.tool
```

**View Active Tasks for a Connector:**

```bash
curl localhost:8083/connectors/kafka-file-sink-task/tasks | python -m json.tool
```

**View Connector Status:**

```bash
curl localhost:8083/connectors/kafka-file-sink-task/status | python -m json.tool
```

**Retrieve Connector Configuration:**

```bash
curl localhost:8083/connectors/kafka-file-sink-task/config | python -m json.tool
```

These queries confirmed that both source and sink connectors were running and properly configured.

### 7.6 Reset Consumer Offsets to the Earliest Position

The consumer group associated with the file sink connector was reset to the earliest offset.

Kafka Connect was stopped before resetting offsets, as offsets cannot be changed while the consumer is active.

```bash
./kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group connect-kafka-file-sink-task \
  --topic kafka-file-sink-topic \
  --reset-offsets --to-earliest \
  --execute
```

Kafka Connect was then restarted, and all records were reprocessed from the beginning.

### 7.7 Restart Without Offset Reset

Kafka Connect was stopped and restarted again without resetting offsets. No new records were consumed, confirming that Kafka resumed consumption from the last committed offset.

### 7.8 Verify Sink File Row Count

The number of records written to the sink file was verified using:

```bash
cat /kafka/sinkFiles/targetFile.log | wc -l
```

The row count increased only after the offset reset and remained unchanged when Kafka Connect was restarted without resetting offsets.

### 7.9 Summary

- Kafka consumer groups were listed and inspected successfully
- Consumer offsets and lag information were analyzed
- Independent offsets were confirmed using different consumer groups
- Kafka Connect REST API was used to monitor connectors and tasks
- Consumer offsets were reset to the earliest position
- Data was reprocessed after offset reset
- No reprocessing occurred without offset changes
- Sink file row counts confirmed correct offset handling

---

## 8. Using Kafka Connect to Read from a Database (MySQL)

This task demonstrates the use of **Kafka Connect JDBC Source Connector** to ingest data from a MySQL database into Kafka topics. The task assumes Kafka and Kafka Connect are already running inside Docker, and a MySQL container is available on the same Docker network.

All commands were executed using Docker containers.

### 8.1 Start and Verify MySQL Container

The MySQL container was started as described in the installation guide:

```bash
docker start mysql
```

The container status was verified using:

```bash
docker stats
```

The `mysql` container appeared in the output, confirming it was running.

### 8.2 Connect to the MySQL Container

A terminal session was opened to connect to the MySQL container:

```bash
docker exec -it mysql /bin/bash
```

MySQL client connection:

```bash
mysql -uroot -proot
```

### 8.3 Create Database and Tables

Inside the MySQL container, the following script was executed:

```sql
drop database if exists srcdb;
create database srcdb;
use srcdb;

create table src_events(
  event_id int primary key,
  event_timestamp timestamp not null
);

insert into src_events values(1, sysdate());
select sleep(1);
insert into src_events values(2, sysdate());
select sleep(1);
insert into src_events values(3, sysdate());

create table web_logins(
  login_time timestamp,
  login_count int
);

insert into web_logins values(sysdate(), 0);

exit;
```

### 8.4 Verify Table Creation and Data

The table contents were verified:

```bash
mysql -uroot -proot srcdb -e 'select * from src_events'
```

The output confirmed that three rows were successfully inserted into the `src_events` table.

The terminal connected to the MySQL container was then minimized.

### 8.5 Verify Kafka Practice Directories

Inside the Kafka container, the Kafka practice directories were verified:

```bash
ls -l /kafka/
```

The following directories were present:

- `confFiles`
- `srcFiles`
- `sinkFiles`

### 8.6 Create JDBC Source Connector Configuration

A new Kafka Connect JDBC source configuration file was created:

**File location:**

```
/kafka/confFiles/connect-jdbc-source.properties
```

**File contents:**

```properties
#--------------------------------------------------
# Content of connect-jdbc-source.properties
#--------------------------------------------------

name=Kafka-jdbc-source-task-1
connector.class=io.confluent.connect.jdbc.JdbcSourceConnector

connection.url=jdbc:mysql://host.docker.internal:3306/srcdb?user=root&password=root&allowPublicKeyRetrieval=true

table.whitelist=src_events
tasks.max=1
poll.interval.ms=2000
mode=incrementing
incrementing.column.name=event_id
topic.prefix=mysql-src-
```

This configuration specifies:

- Source table: `src_events`
- Incremental ingestion based on `event_id`
- Topic prefix: `mysql-src-`

### 8.7 Run Kafka Connect Standalone (JDBC Source)

Kafka Connect was started in standalone mode using the JDBC source configuration:

```bash
./connect-standalone.sh \
  /opt/kafka_2.12-2.4.0/config/connect-standalone.properties \
  /kafka/confFiles/connect-jdbc-source.properties
```

The process produced INFO and WARNING messages, which were expected. Kafka Connect remained running without crashing.

### 8.8 Create Kafka Consumer

A Kafka consumer was created to read all records from the beginning of the topic:

```bash
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic mysql-src-src_events \
  --from-beginning
```

The consumer displayed the three records corresponding to the rows in the `src_events` table.

### 8.9 Insert Additional Records into MySQL

New rows were inserted into the `src_events` table:

```bash
mysql -uroot -proot srcdb -e \
  'insert into src_events select max(event_id)+1, sysdate() from src_events'
```

Verification:

```bash
mysql -uroot -proot srcdb -e 'select * from src_events'
```

The table showed the newly inserted row.

### 8.10 Verify New Records Are Ingested by Kafka

The Kafka consumer automatically received and displayed the new record, confirming that Kafka Connect successfully ingested new rows using incrementing mode.

### 8.11 Verify Kafka Topics

Kafka topics were listed:

```bash
./kafka-topics.sh --zookeeper localhost:2181 --list
```

The topic `mysql-src-src_events` appeared in the list, confirming successful topic creation.

### 8.12 Stop Processes and Drop Topic

The following processes were stopped:

- Kafka Connect (`Ctrl + C`)
- Kafka consumer (`Ctrl + C`)

The Kafka topic was deleted:

```bash
./kafka-topics.sh \
  --zookeeper localhost:2181 \
  --delete \
  --topic mysql-src-src_events
```

### 8.13 Summary

- MySQL container was started and verified
- Database `srcdb` and tables were created successfully
- Kafka Connect JDBC Source Connector was configured and executed
- Data was ingested from MySQL into Kafka
- Incrementing mode correctly detected new rows
- Kafka consumer read all records from the beginning
- Kafka topic creation and deletion were verified