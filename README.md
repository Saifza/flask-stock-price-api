Flask Stock Price Prediction API
This project is a Flask-based API for predicting stock prices using a machine learning model trained with features such as Open, High, Low, and GDP Growth.

## Features
# Machine Learning Model: Uses regression models to predict stock prices.
# REST API: Exposes an endpoint to receive input features and return predictions.
# Dockerized Deployment: Can be easily deployed using Docker.


## Installation
1. Clone the repository:
git clone https://github.com/Saifza/flask-stock-price-api.git  
cd flask-stock-price-api

2. Install dependencies:
pip install -r requirements.txt

3. Run the Flask application:
python app.py

## API Usage
Endpoint:
POST /predict

## Request Body (JSON):
{
  "features": [150, 600, 70, 800]
}

Where features correspond to:

1. Open price
2. High price
3. Low price
4. GDP Growth

## Response (JSON):
{
  "predicted_price": 175.23
}

## Docker Deployment

To run the application in a Docker container:
1. Build the Docker image:
docker build -t stock-predictor .

2. Run the container:

docker run -p 5000:5000 stock-predictor

The API will be accessible at http://localhost:5000/predict.

## Contributing
Feel free to fork the repo and submit pull requests!

## License
MIT License
