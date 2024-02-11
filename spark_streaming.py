from pyspark.sql import SparkSession
from pyspark import SparkContext,SparkConf
from pyspark.sql.functions import StructType,StringType
from conf import  ACCESS_KEY,SECRET_KEY
spark = SparkSession\
    .builder\
    .config('fs.s3a.access.key', ACCESS_KEY)\
    .config('fs.s3a.secret.key', SECRET_KEY)\
    .appName("cluster")\
    .getOrCreate()

def main():
    """
    :return:
    """
