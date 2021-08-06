# Data Pipelines with Apache Airflow

#### Project overview: 

Rockets are arguably one of the humanity's engineering marvels, and every launch attracts attention all around the globe. In this project we will demonstrates the steps a rocket enthusiast who like to collect rocket images for an upcoming rocket launches will take using apache airflow.

#### Exploring the data

We will use a free and open API (subject to rate limit) the Launch Library 2, an online repository of historical and future rocket launches from different sources. The launch library the data for the upcoming rocket launches together with URLs of where to find images of the respective rockets. (https://ll.thespacedevs.com/2.0.0/launch/upcoming)

see the snippet of the data the url returns.
![snippet](/images/url-snippet.png)

The image below shows the mental model.



https://github.com/naneu/Rocket-Images-Download-Data-Pipeline/blob/main/images/mental_image.jpg)





To accomplish our goal we will need to perform the following steps:

1. download the rocket launch data from the API.
2.  get the upcoming rocket pictures.
3. send a notification that the job is done.

#### Data pipelines

Data pipelines generally consists of several tasks or action that need to be executed to achieve a desired result. and from the use case above we have 3 different tasks to be performed for us to achieve our desired outcome.

This tasks need to be executed in a specific order for example we do not want to send notification before collecting the rocket pictures. Therefore, it is important we enforced this order when running this data process. 

with airflow, we can split a large job into individual tasks that together for a DAG, define dependencies so that our tasks run in a specific order and tasks can run in parallel and use different technologies.



#### How to run airflow in a python environment

With apache airflow installed and airflow user created, start by initializing the metastore ( a database that stores all airflow state), ensure that your rocket launch DAG is in the DAG directory and start the scheduler and webserver in different terminals.

1. airflow db init
2. airflow scheduler
3. airflow webserver.

After the set up, visit http://localhost:8080 and log in with the username you created to view airflow.



#### Airflow output

After triggering the DAG, it will start running and you will see the current state of the workflow. and since dependencies were set between tasks, the consecutive tasks will only start running once the upstream task has been completed. 

https://github.com/naneu/Rocket-Images-Download-Data-Pipeline/blob/main/images/dag-running.jpg


https://github.com/naneu/Rocket-Images-Download-Data-Pipeline/blob/main/images/dag-run-result.png)



once all tasks are completed the dag run status will change to success if all tasks executes as expected as shown above.



All tasks logs are collected in airflow, so  we can check the notify task logs to see our notification( this can be integrated to send an email)



https://github.com/naneu/Rocket-Images-Download-Data-Pipeline/blob/main/images/notify-logs.jpg)
