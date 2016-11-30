# tpcds-datagen-as-hive-query
Generate TPCDS data using hive query

##How to use with Hive CLI
1. Clone this repo.

    ```shell
    git clone https://github.com/dharmeshkakadia/tpcds-datagen-as-hive-query/ && cd tpcds-datagen-as-hive-query
    ```
2. Run TPCDSDataGen.hql with settings.hql file and set the required config variables.
    ```shell
    hive -i settings.hql -f TPCDSDataGen.hql -hiveconf SCALE=10 -hiveconf PARTS=10 -hiveconf LOCATION=/HiveTPCDS/ -hiveconf TPCHBIN=resources 
    ```
    Here, `SCALE` is a scale factor for TPCDS, 
    `PARTS` is a number of task to use for datagen (parrellelization), 
    `LOCATION` is the directory where the data will be stored on HDFS, 
    `TPCHBIN` is where the resources are found. You can specify specific settings in settings.hql file.

3. Now you can create tables on the generated data.
    ```shell
    hive -i settings.hql -f ddl/createAllExternalTables.hql -hiveconf LOCATION=/HiveTPCDS/ -hiveconf DBNAME=tpcds
    ```
    Generate ORC tables and analyze
    ```shell
    hive -i settings.hql -f ddl/createAllORCTables.hql -hiveconf ORCDBNAME=tpcds_orc -hiveconf SOURCE=tpcds
    hive -i settings.hql -f ddl/analyze.hql -hiveconf ORCDBNAME=tpcds_orc 
    ```

4. Run the queries !
    ```shell
    hive -database tpcds_orc -i settings.hql -f queries/query12.sql 
    ```

##How to use with Beeline CLI
1. Clone this repo.

    ```shell
    git clone https://github.com/dharmeshkakadia/tpcds-datagen-as-hive-query/ && cd tpcds-datagen-as-hive-query
    ```

2. Upload the resources to DFS.
    ```shell
    hdfs dfs -copyFromLocal resources /tmp
    ```    
    
3. Run TPCDSDataGen.hql with settings.hql file and set the required config variables.
    ```shell
    beeline -u "jdbc:hive2://`hostname -f`:10001/;transportMode=http" -n "" -p "" -i settings.hql -f TPCDSDataGen.hql -hiveconf SCALE=10 -hiveconf PARTS=10 -hiveconf LOCATION=/HiveTPCDS/ -hiveconf TPCHBIN=`grep -A 1 "fs.defaultFS" /etc/hadoop/conf/core-site.xml | grep -o "wasb[^<]*"`/tmp/resources  
    ```
    Here, `SCALE` is a scale factor for TPCDS, 
    `PARTS` is a number of task to use for datagen (parrellelization), 
    `LOCATION` is the directory where the data will be stored on HDFS, 
    `TPCHBIN` is where the resources are found. You can specify specific settings in settings.hql file.

4. Now you can create tables on the generated data.
    ```shell
    beeline -u "jdbc:hive2://`hostname -f`:10001/;transportMode=http" -n "" -p "" -i settings.hql -f ddl/createAllExternalTables.hql -hiveconf LOCATION=/HiveTPCDS/ -hiveconf DBNAME=tpcds
    ```
    Generate ORC tables and analyze
    ```shell
    beeline -u "jdbc:hive2://`hostname -f`:10001/;transportMode=http" -n "" -p "" -i settings.hql -f ddl/createAllORCTables.hql -hiveconf ORCDBNAME=tpcds_orc -hiveconf SOURCE=tpcds
    beeline -u "jdbc:hive2://`hostname -f`:10001/;transportMode=http" -n "" -p "" -i settings.hql -f ddl/analyze.hql -hiveconf ORCDBNAME=tpcds_orc 
    ```

5. Run the queries !
    ```shell
    beeline -u "jdbc:hive2://`hostname -f`:10001/;transportMode=http" -n "" -p "" -database tpcds_orc -i settings.hql -f queries/query12.sql 
    ```
