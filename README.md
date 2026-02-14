# California Housing Prediction API

## Overview

In this Lab, we will learn how to expose a Machine Learning Regression model as an API using [FastAPI](https://fastapi.tiangolo.com/) and [uvicorn](https://www.uvicorn.org/).

1.  **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
2.  **uvicorn**: An ASGI web server implementation for Python.

The workflow involves the following steps:
1.  Training a **Random Forest Regressor** on the **California Housing Dataset**.
2.  Serving the trained model as an API using FastAPI and uvicorn.

---

## Setting up the lab

1.  Create a virtual environment (e.g. `housing_env`).
2.  Activate the environment and install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

Project structure


mlops_labs
└── housing_lab
    ├── model/
    │   └── california_model.pkl  <-- Created after running train.py
    ├── src/
    │   ├── data.py      # Loads and splits California Housing data
    │   ├── main.py      # FastAPI application
    │   ├── predict.py   # Loads model and makes predictions
    │   └── train.py     # Trains Random Forest and saves .pkl
    ├── README.md
    └── requirements.txt

Running the Lab
1. Train the Model

The first step is to train the Random Forest Regressor. This will create the california_model.pkl file in the model/ directory.

Move into the src/ folder:

Bash
cd src
Run the training script:

Bash
python train.py
Output: Model saved successfully.

2. Start the API Server

To serve the trained model as an API, run the following command from the src/ directory:

Bash
uvicorn main:app --reload
main: Refers to the file main.py.

app: Refers to the app = FastAPI() object inside that file.

--reload: Restarts the server automatically when you make code changes.

3. Test the API

Once the server is running, you can access the interactive documentation at:

http://127.0.0.1:8000/docs

You can test the API directly from the docs page (Click "Try it out"), or use Postman or cURL.

Example Request (JSON):

JSON
{
  "MedInc": 8.3252,
  "HouseAge": 41.0,
  "AveRooms": 6.9841,
  "AveBedrms": 1.0238,
  "Population": 322.0,
  "AveOccup": 2.5556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
Example Response:

JSON
{
  "prediction": 4.526
}
FastAPI Syntax & Logic
Data Models (Pydantic)

FastAPI uses Pydantic to validate data types automatically.

1. HousingData (Input)

Defines the 8 features required by the model. If a user sends text instead of a number, FastAPI will return a generic error.

Python
class HousingData(BaseModel):
    MedInc: float      # Median income in block group
    HouseAge: float    # Median house age in block group
    AveRooms: float    # Average number of rooms per household
    AveBedrms: float   # Average number of bedrooms per household
    Population: float  # Block group population
    AveOccup: float    # Average number of household members
    Latitude: float    # Block group latitude
    Longitude: float   # Block group longitude
2. HousingResponse (Output)

Defines the structure of the prediction returned to the user.

Python
class HousingResponse(BaseModel):
    prediction: float
Route Handlers

We use @app.post because we are sending data TO the server to get a prediction.

Python
@app.post("/predict", response_model=HousingResponse)
async def predict_housing(housing_features: HousingData):
    # Logic calls predict.py and returns result
FastAPI Features Used
Request Body Reading: FastAPI automatically reads the JSON body from the request because we defined housing_features: HousingData in the function arguments.

Data Validation: Pydantic ensures MedInc is a float. If you send "Hello" as the income, the API returns a 422 Unprocessable Entity error automatically.

Automatic Documentation: By using Pydantic models, FastAPI automatically generates the Swagger UI at /docs, showing exactly what fields are required.

Error Handling: We use HTTPException to catch errors (like if the model file is missing) and return a clean 500 Internal Server Error to the user.