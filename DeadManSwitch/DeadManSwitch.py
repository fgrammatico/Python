#!/usr/bin/env python3

import os
from pathlib import Path
import time
import boto3
import re
import traceback
import secrets
import string
alphabet = string.ascii_letters + string.digits
bucketrnd = ''.join(secrets.choice(alphabet) for i in range(20))
DMSBUCKET = str('dms-mails-' + bucketrnd.lower())

HOME = str(Path.home())
fileCheck = Path(HOME +'/.aws/credentials')

def aws_cred():
    try:
        if fileCheck.exists ():
            file = open(HOME +'/.aws/credentials')
            allLines = file.readlines()
            accessKeyTemp = (allLines[1])
            accessKey = accessKeyTemp[18:38]
            secretTemp = (allLines[2])
            secret = secretTemp[22:62]
            file.close()
            answer1 = input ('\nWelcome to the Dead Man Switch generator for AWS.\nThese credentials were found:\n\n' + 'aws_access_key_id=' + accessKey + '\n' + 'aws_secret_access_key=' + secret + '\n' + '\nPlease enter Y/n to confirm this is correct: ').upper()
            if answer1 == 'Y':
                print('\nThank you for confirming, program resuming...')
                user_question()
            elif answer1 == 'N':
                print('\nThank you for confirming, please edit your AWS credentials file so the top user is the one you will select.')
                program_end()
            else:
                print('\nSorry, the answer is invalid, please use just Y or n.\n')
                aws_cred()
        else:
            print('\nI can\'t find any AWS credentials, please download AWS cli and configure the tool with an existing user.')
            answer2 = input ('\nWould you like to enter the acces key and secret manually now? ').upper()
            if answer2 == 'N':
                program_end()
            elif answer2 == 'Y':
                accessKeyTemp = input ('\nPlease enter your access key: ')
                secretTemp = input ('\nPlease enter your secret: ')
                accessKey = str(accessKeyTemp)
                secret = str(secretTemp)
                user_question()
            else:
                print('\nSorry, the answer is invalid, please use just Y or n.\n')
                aws_cred()

    except IOError:
        print('\nFile not accessible.\n')

def user_question():
    AWSUSER = input ('\nPlease enter the AWS user you want to monitor as it appears in your console manager: ')
    confirm = input ('\nIs this correct "' + str(AWSUSER) + '" ?(Y/n)')
    confirmUp = confirm.upper()
    if confirmUp == "Y":
        print('\nThank you for confirming, program resuming...')
        email_from()
    elif confirmUp == "N":
        user_question()
    else:
        print('\nInvalid answer, please enter Y or n only.')
        user_question()

def email_from():
    questionAddress = input ('\nPlease enter your "from" address that you will use to send your notifications: ')
    fromaddress = questionAddress.lower()
    fromaddressTemp = re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',fromaddress)
    confirmAdd = input ('\nIs this correct "' + str(fromaddress) + '" ?(Y/n)').upper()
    if confirmAdd == "Y":
        if fromaddressTemp:
            region_question()
        else:
            print('\nYour email does not evaluate to a correct pattern, please retry.')
            email_from()
    elif confirmAdd == "N":
        email_from()
    else:
        print('\nYour answer is incorrect, please retry.')
        email_from()

def region_question():
    REGION = input ('\nWhich AWS Availability Zone do you want to use to deploy your Dead Man Switch (ex. eu-central-1)? ')
    checkRegionPattern= re.search(r'\w{2}-\w{4,7}-\d{1}',REGION)
    if checkRegionPattern:
        days_func()
    else:
        print('\nYour region does not evaluate to a correct patter, please retry')
        region_question()

def days_func():
    N = int(input ('\nPlease define how many days back you want to check for your logins (min 10 to max 90): '))
    if isinstance(N, int) == True and N <= 90 and N >= 10:
        create_role()
    else:
        print('\nInvalid number!')
        days_func()

def create_role():
    try:
        client = boto3.client('iam')
        print('\nCreating AWS Role "dms-lambda"')
        response = client.create_role(
            RoleName='dms-lambda',
            AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":["lambda.amazonaws.com"]},"Action":["sts:AssumeRole"]}]}',
            Description='Dead Man Switch Role',
            MaxSessionDuration=3600,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'DMS'
                },
            ]
        )
        print('Attaching policies...')
        time.sleep(3) 
        response = client.put_role_policy(
            PolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:*","Resource":"*"},{"Effect":"Allow","Action":"cloudtrail:*","Resource":"*"},{"Effect":"Allow","Action":"SES:*","Resource":"*"}]}',
            PolicyName='dms-lambda',
            RoleName='dms-lambda',
        )
        print('\nRole successfully created')
        create_bucket()
    except Exception as error:
        errdescr = type(error).__name__ + '\n' + traceback.format_exc()
        print(errdescr)

def create_bucket():
    client = boto3.client('s3')
    print('\nCreating S3 bucket')
    response = client.create_bucket(
    ACL='private',
    Bucket=DMSBUCKET,
    CreateBucketConfiguration={
        'LocationConstraint': REGION
    },
    )
    response = client.put_bucket_encryption(
        Bucket=DMSBUCKET,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                },
            ]
        }
    )
    response = client.put_bucket_acl(
    ACL='private',
    Bucket=DMSBUCKET
    )
    print('\nS3 bucket created')
    mail_func()

def mail_func():
    toaddress = input ('Please enter your the address that you will use to send your notifications: ')
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('/Users/fabiogrammatico/github/Automation/cloudformation/Serverless/dead-man-switch/test.txt', bucketName, 'test.txt')
    program_end()

def program_end():
    final = input ('\nEnd of program\n\nPress any key\n')

aws_cred()

#to do:
#mail question and body
#send to s3
#delete local file
#create handler
#run sls


