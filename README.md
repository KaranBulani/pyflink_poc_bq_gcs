# PyFlink: Data Transfer Between BigQuery and Google Cloud Storage

## Setup Instructions

### Infrastructure Requirements

1. **Environment:**  
    All operations are performed on a Google Cloud Platform (GCP) Virtual Machine (VM) with OS: Ubuntu 22.

2. **Location Consistency:**  
    Ensure that BigQuery datasets and Google Cloud Storage (GCS) buckets are located in the same region.

3. **Google Cloud API Access:**  
    Ensure that the VM has the required Google Cloud APIs enabled (such as BigQuery and Cloud Storage). These permissions are set during VM creation in the "Security" section and cannot be changed later.

4. **Permissions Verification:**  
    Confirm that the VM has the necessary permissions for both GCS and BigQuery by running the following commands:

    ```sh
    # List contents of the GCS bucket
    gsutil ls gs://pyflink-gke-poc-gcs-us/

    # View a file in the GCS bucket
    gsutil cat gs://pyflink-gke-poc-gcs-us/storage_output.csv

    # List BigQuery datasets
    bq ls pyflink-gke-poc:testUS

    # Query a BigQuery table
    bq query --nouse_legacy_sql 'SELECT * FROM `pyflink-gke-poc.testUS.dummy_string_types`'
    ```
The cleanest approach to collaborate in 1 folder.

1. **Create a shared directory**, e.g.:

   ```bash
   sudo mkdir /opt/shared-code
   ```

2. **Change the group ownership** to a common group both you and your friend are in (or create a new group):

   ```bash
   sudo groupadd devgroup           # create new group (if needed)
   sudo chown :devgroup /opt/shared-code
   ```

3. **Add both users to that group**:

   ```bash
   sudo usermod -aG devgroup ksbrocks_bulani
   sudo usermod -aG devgroup your_friend_username
   ```

   ✅ You’ll need to log out and log back in for group changes to take effect.

4. **Set permissions to allow group members to read/write**:

   ```bash
   sudo chmod 2775 /opt/shared-code
   ```

   * The `2` (setgid bit) ensures all new files/folders inside inherit the group.

5. **Put VM code here**
---

### Python Installation

Follow these steps to install Python 3.9 and essential tools on Ubuntu 22:

1. **Update package lists and install prerequisites:**
    ```sh
    sudo apt update
    sudo apt install -y software-properties-common ca-certificates
    ```

2. **Add the Deadsnakes PPA for Python 3.9:**
    ```sh
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    ```

3. **Install editors (optional but recommended):**
    ```sh
    sudo apt install -y nano vim
    ```

4. **Install Python 3.9 and required modules:**
    ```sh
    sudo apt install -y python3.9 python3.9-venv python3.9-distutils
    # 1. For python 2. For Virtual Env 3. needed by pip
    ```

5. **Install pip for Python 3.9:**
    ```sh
    curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.9
    ```

6. **Configure the default Python 3 version:**
    > **Note:**  
    > If you need to switch between multiple Python 3 versions (e.g., 3.9 and 3.10), use the following commands:
    > ```sh
    > sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2
    > sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
    > sudo update-alternatives --config python3
    > ```
    > It is recommended to keep Ubuntu’s default Python 3.10 at a higher priority to avoid affecting system operations.

7. **Verify installations:**
    ```sh
    python3.9 --version      # Should print Python 3.9.x
    python3 --version        # Prints the selected default Python 3 version
    pip3.9 --version         # pip tied to Python 3.9
    ```

8. **Creating a Python Virtual Environment and Installing PyFlink**

    Follow these steps to set up a dedicated Python virtual environment and install PyFlink:

    1. **Create a virtual environment:**
        ```sh
        python3.9 -m venv flink_env
        ```
    2. **Activate the virtual environment:**
        ```sh
        source flink_env/bin/activate
        ```
    3. **Install PyFlink (version 1.17.2 mentioned [here](https://github.com/GoogleCloudDataproc/flink-bigquery-connector?tab=readme-ov-file#maven-central) ):**
        ```sh
        pip install apache-flink==1.17.2
        ```
        This ensures that PyFlink and its dependencies are installed in an isolated, user-owned environment.

        A. **Flink setup tarball : needed in production setup**
        ```sh
        wget https://downloads.apache.org/flink/flink-1.17.2/flink-1.17.2-bin-scala_2.12.tgz
        tar -xvzf flink-1.17.2-bin-scala_2.12.tgz
        cd flink-1.17.2
        ```

    4. **Deactivate the virtual environment when finished:**
        ```sh
        deactivate
        ```

    **Please Note:** Any Python commands provided below assume that the virtual environment is active.

---

### Java Installation

To install Java (OpenJDK 11) and configure your environment on Ubuntu 22, follow these steps:

1. **Install OpenJDK 11:**
    ```sh
    sudo apt install -y openjdk-11-jdk
    ```

2. **Set JAVA_HOME and update your PATH:**
    ```sh
    echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
    echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
    ```

3. **Verify the JAVA_HOME environment variable:**
    ```sh
    echo $JAVA_HOME
    ```
    The output should be:
    ```
    /usr/lib/jvm/java-11-openjdk-amd64
    ```

    > **Note:**  
    > Setting `JAVA_HOME` and updating your `PATH` ensures that Java is available for all terminal sessions and required by many tools and frameworks.

To confirm that Python (PyFlink) is using the correct Java version, run:

```sh
python -c "from pyflink.java_gateway import get_gateway; print(get_gateway().jvm.java.lang.System.getProperty('java.version'))"
# Expected output: 11.0.x
```

---

## Testing PyFlink Installation

1. **Create a test script:**  
    Create a file named `flink_test.py` with the following content:

    ```python
    from pyflink.datastream import StreamExecutionEnvironment

    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # Set parallelism to 1 for clear output
    env.from_collection([1, 2, 3]).print()
    env.execute("test")
    ```

2. **Run the test script:**
    ```sh
    python flink_test.py
    ```

    If your installation is correct, you should see the output of the collection `[1, 2, 3]` printed to the console.

---

### Maven Installation

To install Apache Maven (version 3.8.8) on Ubuntu 22, follow these steps:

1. **Download and Extract Maven:**
    ```sh
    wget https://downloads.apache.org/maven/maven-3/3.8.8/binaries/apache-maven-3.8.8-bin.tar.gz
    tar -xvzf apache-maven-3.8.8-bin.tar.gz
    sudo mv apache-maven-3.8.8 /opt/maven
    ```

2. **Configure Environment Variables:**
    Add the following lines to your `~/.bashrc` (or `~/.zshrc` if using Zsh) to set up Maven environment variables:
    ```sh
    export MAVEN_HOME=/opt/maven
    export M3_HOME=/opt/maven
    export PATH=/opt/maven/bin:$PATH #/bin path should be correct
    echo 'export PATH=/opt/maven/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
    ```

3. **Verify Maven Installation:**
    Confirm that Maven is installed and accessible by running:
    ```sh
    mvn -v
    ```
    You should see output indicating Maven 3.8.8 and the Java version in use.

    > **Note:**  
    > These steps are based on the prerequisites outlined in the [Flink BigQuery Connector documentation](https://github.com/GoogleCloudDataproc/flink-bigquery-connector?tab=readme-ov-file#prerequisites).  
    > For archive versions of Maven, check here: https://archive.apache.org/dist/maven/maven-3/

---

### Building the Connector JAR with Maven

Follow these steps to build the required JAR file using Maven:

1. **Download the `pom.xml` file:**  
    Obtain the `pom.xml` provided in this repository and place it in your project directory.

2. **Validate the Maven Project:**  
    Run the following command to validate the `pom.xml` configuration:
    ```sh
    mvn validate
    ```
    Ensure that the validation completes successfully before proceeding.

3. **Build the Project:**  
    Execute the Maven build process to generate the JAR file:
    ```sh
    mvn clean install
    ```
    Upon successful completion, a new JAR file will be created in the `target/` directory.

4. **Reference the JAR in Your Python Code:**  
    Use the path to the generated JAR file (located in the `target/` directory) when configuring your Python code to utilize the connector.

    > **Note:**  
    > Ensure that all Maven dependencies are resolved and that the build completes without errors before using the JAR.
