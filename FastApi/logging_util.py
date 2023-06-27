import time
from dotenv import load_dotenv
import os
import string
import boto3


class logging_function():
    def __init__(self):
        #loading env variables
        load_dotenv()
        # Define the AWS access key and secret
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.logGroupName=os.environ.get('LOG_GROUP_NAME')
        self.logStreamName=os.environ.get('LOG_STREAM_NAME')
        
    # Create an S3 client using the access key and secret
    def init_resources(self):
        cloudwatch = boto3.client('logs', 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name='us-east-1')
        return cloudwatch

    def get_log_stream_name(self):
        return self.logStreamName
    
    def create_AWS_logs(self,msg):
        logStreamName= self.get_log_stream_name()
        cloudwatch = self.init_resources()
        cloudwatch.put_log_events(
                    logGroupName=self.logGroupName,
                    logStreamName=logStreamName,
                    logEvents=[
                            {
                                'timestamp': int(time.time() * 1000),
                                'message': msg
                            },
                        ]
                )
    
    def read_cloudwatch_logs(self,code,username,filter_range,api_name):
        logStreamName= self.get_log_stream_name()
        cloudwatch = self.init_resources()
        response=cloudwatch.get_log_events(
            logGroupName=self.logGroupName,
            logStreamName=logStreamName
        )
        return self.filter_logs(cloudwatch,code,username,filter_range,api_name)
    
    def filter_logs(self,cloudwatch,code,username,filter_range,api_name):
        # write a CloudWatch Logs Insights query
        #print(code)
        backend= 'backend'
        if username == 'admin': 
            if api_name == None:
                query = f"fields @timestamp, @message, @logStream | filter @message like /{code}/ and @message like /{backend}/ | sort @timestamp desc"
            else:
                query = f"fields @timestamp, @message, @logStream | filter @message like /{code}/ and @message like /{api_name}/ and @message like /{backend}/ | sort @timestamp desc"
            
        else: 
            if api_name == None:
                query = f"fields @timestamp, @message, @logStream | filter @message like /{code}/ and @message like /{username}/ and @message like /{backend}/ | sort @timestamp desc"
            else:
                query = f"fields @timestamp, @message, @logStream | filter @message like /{code}/ and @message like /{username}/ and @message like /{api_name}/ and @message like /{backend}/ | sort @timestamp desc"
        if filter_range == 'last_hour':
            time_passed=3600
        elif filter_range == 'last_day':
            time_passed=86400
        elif filter_range == 'last_week':
            time_passed=604800
        elif filter_range == 'last_month':
           time_passed=2629746 
        else:
            time_passed=3600
        # execute the query and retrieve results
        query_response = cloudwatch.start_query(
            logGroupName=self.logGroupName,
            startTime=int((time.time() - time_passed) * 1000), # start time (in milliseconds) for the query (in this example, last hour)
            endTime=int(time.time() * 1000), # end time (in milliseconds) for the query (in this example, now)
            queryString=query
        )
        # retrieve query ID and status
        query_id = query_response['queryId']
        query_status = None
        # wait for query to complete
        while query_status == None or query_status == 'Running':
            print('Waiting for query to complete ...')
            time.sleep(1)
            query_status = cloudwatch.get_query_results(
                queryId=query_id
            )['status']
        # retrieve query results
        query_results = cloudwatch.get_query_results(
            queryId=query_id
        )
        return query_results['results']
        # return query_results