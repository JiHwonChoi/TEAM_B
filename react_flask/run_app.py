from server.routes.route import app


if __name__ == "__main__":
    app.secret_key = '2019313442'
    app.run(port=5000, debug = True)
    