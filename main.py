from flask import Flask
from application import init_app

app: Flask = init_app() # type: ignore

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=False)