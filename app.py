import connexion


def submit_job(body):
    return {
        'jobId': 'myJobId',
        'jobName': body['granule'],
        'parameters': body,
    }


app = connexion.App(__name__)
app.add_api('openapi.yml')


if __name__ == '__main__':
    app.run(port=8080)
