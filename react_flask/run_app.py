from server.routes.route import app


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5000, debug = True)
    