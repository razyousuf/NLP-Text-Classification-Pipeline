#from hate.pipeline.trainer import TrainingPipeline
#obj = TrainingPipeline()
#obj.run_pipeline()

from fastapi import FastAPI, Query
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from starlette.responses import RedirectResponse

import sys
from hate.constants import *
from hate.logger import logging
from hate.exception import CustomException

from hate.pipeline.predictor import PredictionPipeline
from hate.pipeline.trainer import TrainingPipeline

from fastapi.responses import JSONResponse


app = FastAPI()

# authentication for the FastAPI app
@app.get("/", tags=["authentication"])
async def index():
    """
    Redirects to the prediction page.
    """
    return RedirectResponse(url="/docs")

# Training the model
@app.get("/train")
async def training():
    """
    Trains the model.
    """
    try:
        logging.info("Entering train method of the FastAPI app..")
        obj = TrainingPipeline()
        obj.run_pipeline()
        return JSONResponse(content={"message": "Training completed successfully."})
    
    except Exception as e:
        return Response(f"An error occurred during training: {str(e)}")

    
# Predicting the class of the input text
@app.get("/predict")
async def predict(text: str = Query(...)):
    try:
        obj = PredictionPipeline()
        result = obj.run_pipeline(text)
        return {"prediction": result}
    except Exception as e:
        raise CustomException(e, sys) from e

# Run the FastAPI app   
# if __name__ == "__main__":
#     uvicorn.run("app:app", host=APP_HOST, port=APP_PORT)