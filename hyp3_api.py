from os import environ

import boto3
import connexion

BATCH_CLIENT = boto3.client('batch')


def submit_job(body):
    job = BATCH_CLIENT.submit_job(
        jobName=body['granule'],
        jobQueue=environ['JOB_QUEUE'],
        jobDefinition=environ['JOB_DEFINITION'],
        parameters=body
    )
    job['parameters'] = body
    return job


connexion_app = connexion.App(__name__)
connexion_app.add_api('openapi.yml')


if __name__ == '__main__':
    connexion_app.run(port=8080)
