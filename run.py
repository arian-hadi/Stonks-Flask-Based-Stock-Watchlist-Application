from app import create_app
import logging


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    logging.basicConfig(level=logging.DEBUG)
    