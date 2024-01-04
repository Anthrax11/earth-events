import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.exceptions import AirflowException

from src.pipeline.extract import read_from_api
from src.pipeline.transform import transform
from src.pipeline.cold_start import check_db_exists
from src.pipeline.init_db import init_db

default_args = {
    "owner": "airflow",
}

def branch_func(**kwargs):
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(key="db_exists", task_ids='check_if_database_exists')
    if xcom_value == "true":
        return 'read_from_api'
    elif xcom_value == "false":
        return 'init_db'
    else:
        raise AirflowException(f"Unexpected XCom value: {xcom_value!r}")


dag = DAG(
    dag_id="earth-events",
    default_args=default_args,
    start_date=datetime.datetime.now(),
    schedule="@daily",
)

database_exists = PythonOperator(task_id="check_if_database_exists", python_callable=check_db_exists, dag=dag)

branch_op = BranchPythonOperator(task_id="database_exists", python_callable=branch_func, dag=dag)

extract_task = PythonOperator(task_id="read_from_api", python_callable=read_from_api, dag=dag)

transform_task = PythonOperator(task_id="transform", python_callable=transform, dag=dag)

init_db_task = PythonOperator(task_id="init_db", python_callable=init_db, dag=dag)


database_exists >> branch_op >> [extract_task, init_db_task]
extract_task >> transform_task