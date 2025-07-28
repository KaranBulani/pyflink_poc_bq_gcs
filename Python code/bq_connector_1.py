from pyflink.table import EnvironmentSettings, TableEnvironment


def bq_connector():
    
    # Initialize the Table Environment
    env_settings = EnvironmentSettings.in_batch_mode()
    t_env = TableEnvironment.create(env_settings)

    t_env.get_config().set("pipeline.jars", "file:///opt/shared-code/pyflink_setup_2/target/flink.gcp.bq.gcs.minimal-0.0.1.jar;file:///opt/shared-code/flink-1.17.2/opt/flink-gs-fs-hadoop-1.17.2.jar;file:///opt/shared-code/flink-1.17.2/lib/flink-csv-1.17.2.jar;file:///opt/shared-code/flink-1.17.2/lib/flink-json-1.17.2.jar")

    # -------------------------------------------------------------------
    # Define BigQuery source using the Storage API connector
    t_env.execute_sql("""
    CREATE TABLE bq_source (
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
      'connector' = 'bigquery',
      'project'   = 'pyflink-gke-poc',
      'dataset'   = 'testUS',
      'table'     = 'dummy_string_types'
    )
    """)
    print("bq_storage created")
    
    t_env.execute_sql("SELECT * FROM bq_source").print()

if __name__ == '__main__':
    bq_connector()
