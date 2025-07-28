from pyflink.table import EnvironmentSettings, TableEnvironment
import os

def gcs_test():

    # Initialize the Table Environment
    env_settings = EnvironmentSettings.in_batch_mode()
    t_env = TableEnvironment.create(env_settings)
    t_env.get_config().set("pipeline.jars", "file:///opt/shared-code/flink-1.17.2/opt/flink-gs-fs-hadoop-1.17.2.jar;file:///opt/shared-code/flink-1.17.2/lib/flink-csv-1.17.2.jar;file:///opt/shared-code/flink-1.17.2/lib/flink-json-1.17.2.jar;file:///opt/shared-code/pyflink_setup_2/target/flink.gcp.bq.gcs.minimal-0.0.1.jar")

    # -------------------------------------------------------------------
    # Define CSV sinks on GCS for each approach
    print("STEP 1")
    t_env.execute_sql("""
    CREATE TABLE gcs_source_storage (
      col1 STRING,
      col2 STRING,
      col3 STRING,
      col4 STRING,
      col5 STRING,
      col6 STRING,
      col7 STRING,
      col8 STRING,
      col9 STRING,
      col10 STRING
    ) WITH (
      'connector' = 'filesystem',
      'path'      = 'gs://pyflink-gke-poc-gcs-us/storage_input.csv',
      'format'    = 'csv'
    )
    """)
    print("STEP 2")
    t_env.execute_sql("SELECT * FROM gcs_source_storage").print()

    t_env.execute_sql("""
    CREATE TABLE gcs_output_storage (
      col1 STRING,
      col2 STRING,
      col3 STRING,
      col4 STRING,
      col5 STRING,
      col6 STRING,
      col7 STRING,
      col8 STRING,
      col9 STRING,
      col10 STRING
    ) WITH (
      'connector' = 'filesystem',
      'path'      = 'gs://pyflink-gke-poc-gcs-us/output_dir/',
      'format'    = 'csv',
      'sink.parallelism' = '1'
    )
    """)
    print("STEP 3")
    result = t_env.execute_sql("INSERT INTO gcs_output_storage SELECT * FROM gcs_source_storage")
    result.wait()  # <-- Waits for job completion


if __name__ == '__main__':
    gcs_test()
