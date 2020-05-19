import connexion


def submit_job():
    print('submit_job')


app = connexion.App(__name__)
app.add_api('openapi.yml')


if __name__ == '__main__':
    app.run(port=8080)
