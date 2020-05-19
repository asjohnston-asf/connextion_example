import connexion


def submit_job(body):
    return {
        'jobId': 'myJobId',
        'jobName': 'myJobName',
        'parameters': {
            'granule': body['granule'],
        },
    }


app = connexion.App(__name__)
app.add_api('openapi.yml')


if __name__ == '__main__':
    app.run(port=8080)
