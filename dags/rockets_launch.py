import json
import pathlib
import requests
import requests.exceptions as req_exec
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args ={
    'start_date': datetime(2021,7, 10)
}

def _get_pictures():
    #ensure directory exists
    pathlib.Path('/tmp/images').mkdir(parents=True, exist_ok=True)
    #download all pictures in launches.json
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image" ] for launch in launches["results"]]

        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/") [-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {image_url} to {target_file}")
            except req_exec.MissingSchema:
                print(f"{image_url} appears to be invalid URL.")
            except req_exec.ConnectionError:
                print(f"Could not connect to {image_url}")


with DAG('download_rocket_launches',schedule_interval=None,default_args=default_args) as dag:

    download_launches=BashOperator(
        task_id='download_launches',
        bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming/'",
        
    )

    get_pictures=PythonOperator(
        task_id='get_pictures',
        python_callable=_get_pictures
    )

    notify=BashOperator(
        task_id='notify',
        bash_command = 'echo "There are now $(ls /tmp/images/ | wc -l) images."'
    )

  
    download_launches >> get_pictures >> notify

