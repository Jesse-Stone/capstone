from routes import app

app.config['SECRET_KEY'] = '123456'


if __name__ == '__main__':
    app.run(debug=True)