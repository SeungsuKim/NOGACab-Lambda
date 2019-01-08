#from __future__ import print_function

import subprocess
import os
import boto3

from utils import load_yaml_config


def get_session():
    certificate = load_yaml_config("certificate.yml")
    session = boto3.Session(
        aws_access_key_id = certificate.AWS_ACCESS_ID,
        aws_secret_access_key = certificate.AWS_SECRET_KEY,
        region_name = certificate.REGION_NAME
    )
    return session


def get_client(session, service):
    return session.client(service)


def downloadFromS3(bucketname, key, filename):
    s3_client = get_client(get_session(), 's3')
    s3_client.download_file(bucketname, key, filename)


def image_analysis_handler(event, context):
    os.environ['PATH'] = os.environ['PATH'] + '/' + os.environ[
        'LAMBDA_TASK_ROOT']

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        imagepath = "/tmp/" + key.split('/')[-1]
        print("Start downloading image.")
        print("Bucket: {}".format(bucket))
        print("Key: {}".format(key))
        print("Image path: {}".format(imagepath))
        downloadFromS3(bucket, key, imagepath)
        print("Downloaded image: {}".format(imagepath))

        print("Start downloading weight file.")
        bucket = 'bucket-nogacab'
        key = 'darknet/yolov3.weights'
        weightpath = '/tmp/yolov3.weights'
        downloadFromS3(bucket, key, weightpath)
        print("Downloaded weight file.")

        print("Start detecting objects from image.")
        result = subprocess.run(['./darknet', 'detect', './cfg/yolov3.cfg',
                                 weightpath, imagepath])
        if result.returncode != 0:
            print("Error while detecting objects:\n" + str(result.stderr))
            break
        
        print("Finished detecting objects from image.")
        print(str(result.stdout))
        print(str(result.stderr))

        result_file = open("/tmp/result.txt", "r")
        print("Content of result.txt: ")
        print(result_file.read())

