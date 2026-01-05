FROM apache/airflow:3.1.0
 
USER root
 
# Install Java + utilities + CA certs (for HTTPS downloads)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk wget curl git ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
 
# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
 
# Add MySQL Connector/J 9.4.0 (for Spark JDBC)
RUN mkdir -p /opt/spark/jars && \
    wget --no-verbose --retry-connrefused --waitretry=2 --timeout=30 -t 3 \
    https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/9.4.0/mysql-connector-j-9.4.0.jar \
    -O /opt/spark/jars/mysql-connector-j-9.4.0.jar || \
    (echo "Failed to download MySQL Connector/J 9.4.0" && exit 1)
 
# Add JAR path to environment
ENV SPARK_CLASSPATH="/opt/spark/jars/mysql-connector-j-9.4.0.jar"
 
# Install Python dependencies for Airflow
USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Working directory for Airflow
WORKDIR /opt/airflow