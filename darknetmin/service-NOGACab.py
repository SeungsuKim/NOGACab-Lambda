from __future__ import print_function

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
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        imagepath = "/tmp/" + key.split('/')[-1]
        print("Fuck off")
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

        print("Start copying cfg file.")
        result = subprocess.run(['cp', './cfg/yolov3.cfg', '/tmp/volov3.cfg'])
        if result.returncode != 0:
            print("Error while copying cfg file:\n" + result.stderr)
            break
        print("Copied the cfg file.")

        print("Start copying darknet file.")
        result = subprocess.run(['cp', '/var/task/darknet', '/tmp/darknet'])
        if result.returncode != 0:
            print("Error while copying darknet file.")
            break
        print("Copied the darknet file")

        print("Start making darknet executable.")
        result = subprocess.run(['chmod', '755', '/tmp/darknet'])
        if result.returncode != 0:
            print("Error while making darknet executable.")
            break
        print("Made darknet executable.")

        print("Start detecting objects from image.")
        result = subprocess.run(['/tmp/darknet', 'detect', '/tmp/yolov3.cfg',
                                 weightpath, imagepath], shell=True)
        if result.returncode != 0:
            print("Error while detecting objects:\n" + result.stderr)
            break

        print("Finished detecting objects from image.")
        print(result.stdout)
