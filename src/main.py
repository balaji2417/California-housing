from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data

app = FastAPI()


class HousingData(BaseModel):
    """
    Pydantic BaseModel representing California housing metrics.

    Attributes:
        MedInc (float): Median income in block group.
        HouseAge (float): Median house age in block group.
        AveRooms (float): Average number of rooms per household.
        AveBedrms (float): Average number of bedrooms per household.
        Population (float): Block group population.
        AveOccup (float): Average number of household members.
        Latitude (float): Block group latitude.
        Longitude (float): Block group longitude.
    """
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


class HousingResponse(BaseModel):
    prediction: float


"""Modern web apps use a technique named routing. This helps the user remember the URLs."""


@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    """Concurrent (multiple tasks can run simultaneously)"""
    return {"status": "healthy"}


@app.post("/predict", response_model=HousingResponse)
async def predict_housing(housing_features: HousingData):
    """
    Predict the median house value based on provided features.
    Args:
        housing_features (HousingData): Object containing the 8 housing metrics.
    Returns:
        HousingResponse: Object containing the predicted median house value.
    Raises:
        HTTPException: Returns a 500 status code if prediction fails.
    """
    try:
        # Extract all 8 features in the correct order expected by the model
        features = [[
            housing_features.MedInc,
            housing_features.HouseAge,
            housing_features.AveRooms,
            housing_features.AveBedrms,
            housing_features.Population,
            housing_features.AveOccup,
            housing_features.Latitude,
            housing_features.Longitude
        ]]

        prediction = predict_data(features)
        return HousingResponse(prediction=float(prediction[0]))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))