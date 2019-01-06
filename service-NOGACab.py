from __future__ import print_function

import subprocess
import boto3

from utils import load_yaml_config


def downloadFromS3(bucketname, key, filename):
    s3_client = boto3.client('s3')
    s3_client.download_file(bucketname, key, filename)


def image_analysis_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        imagepath = "/tmp/{}".format(key)
        downloadFromS3(bucket, key, imagepath)
        print("Downloaded image: {}".format(key))

        bucket = 'bucket-nogacab'
        key = 'darknet/yolov3.weights'
        weightpath = '/tmp/yolov3.weights'
        downloadFromS3(bucket, key, weightpath)
        print("Downloaded weight file.")

        print("Start detecting objects from image.")
        result = subprocess.run(['./darknet', 'detect', 'cfg/yolov3.cfg',
                                 weightpath, imagepath])

        if result.returncode != 0:
            print("Error while detecting objects:\n" + result.stderr)
            break

        print("Finished detecting objects from image.")
        print(result.stdout)
