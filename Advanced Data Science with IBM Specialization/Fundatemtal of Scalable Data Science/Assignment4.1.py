
# coding: utf-8

# # Assignment 4
# 
# Welcome to Assignment 4. This will be the most fun. Now we will prepare data for plotting.
# 
# Just make sure you hit the play button on each cell from top to down. There are three functions you have to implement. Please also make sure than on each change on a function you hit the play button again on the corresponding cell to make it available to the rest of this notebook. Please also make sure to only implement the function bodies and DON'T add any additional code outside functions since this might confuse the autograder.
# 
# So the function below is used to make it easy for you to create a data frame from a cloudant data frame using the so called "DataSource" which is some sort of a plugin which allows ApacheSpark to use different data sources.
# 

# Sampling is one of the most important things when it comes to visualization because often the data set gets so huge that you simply
# 
# - can't copy all data to a local Spark driver (Watson Studio is using a "local" Spark driver)
# - can't throw all data at the plotting library
# 
# Please implement a function which returns a 10% sample of a given data frame:

# In[2]:


def getSample(df,spark):
    return df.sample(False, 0.1, seed=None)


# Now we want to create a histogram and boxplot. Please ignore the sampling for now and return a python list containing all temperature values from the data set

# In[27]:


def getListForHistogramAndBoxPlot(df,spark):
    result = spark.sql("select temperature from washing where temperature is not null")
    result_array = result.rdd.map(lambda row : row.temperature).collect()
    return result_array


# Finally we want to create a run chart. Please return two lists (encapsulated in a python tuple object) containing temperature and timestamp (ts) ordered by timestamp. Please refer to the following link to learn more about tuples in python: https://www.tutorialspoint.com/python/python_tuples.htm

# In[38]:


#should return a tuple containing the two lists for timestamp and temperature
#please make sure you take only 10% of the data by sampling
#please also ensure that you sample in a way that the timestamp samples and temperature samples correspond (=> call sample on an object still containing both dimensions)
def getListsForRunChart(df,spark):
    result = spark.sql("select voltage,ts from washing where voltage is not null order by ts asc")
    result_rdd = result.rdd.sample(False,0.1).map(lambda row : (row.ts,row.voltage))
    result_array_ts = result_rdd.map(lambda ts_voltage: ts_voltage[0]).collect()
    result_array_voltage = result_rdd.map(lambda ts_voltage: ts_voltage[1]).collect()
    return (result_array_ts, result_array_voltage)


# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED
# #axx
# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED

# Now it is time to connect to the object store and read a PARQUET file and create a dataframe out of it. We've created that data for you already. Using SparkSQL you can handle it like a database.

# In[4]:


import ibmos2spark

# @hidden_cell
credentials = {
    'endpoint': 'https://s3-api.us-geo.objectstorage.service.networklayer.com',
    'api_key': 'PUJMZf9PLqN4y-6NUtVlEuq6zFoWhfuecFVMYLBrkxrT',
    'service_id': 'iam-ServiceId-9cd8e66e-3bb4-495a-807a-588692cca4d0',
    'iam_service_endpoint': 'https://iam.bluemix.net/oidc/token'}

configuration_name = 'os_b0f1407510994fd1b793b85137baafb8_configs'
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name, 'bluemix_cos')

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
# Since JSON data can be semi-structured and contain additional metadata, it is possible that you might face issues with the DataFrame layout.
# Please read the documentation of 'SparkSession.read()' to learn more about the possibilities to adjust the data loading.
# PySpark documentation: http://spark.apache.org/docs/2.0.2/api/python/pyspark.sql.html#pyspark.sql.DataFrameReader.json

df = spark.read.parquet(cos.url('washing.parquet', 'courseradsnew-donotdelete-pr-1hffrnl2pprwut'))
df.show()


# In[3]:


get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt


# In[29]:


plt.hist(getListForHistogramAndBoxPlot(df,spark))
plt.show()


# In[33]:


plt.boxplot(getListForHistogramAndBoxPlot(df,spark))
plt.show()


# In[39]:


lists = getListsForRunChart(df,spark)


# In[41]:


plt.plot(lists[0],lists[1])
plt.xlabel("time")
plt.ylabel("temperature")
plt.show()


# Congratulations, you are done! Please download the notebook as python file, name it assignment4.1.py and submit it to the grader.
