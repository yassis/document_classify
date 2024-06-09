
import pathlib
from fastapi import FastAPI

from api.config import getSettings
from api.schema import SingleTextQuery, MultipleTextQuery, PredictionResult

from model.classifyModel import ClassifyModel

settings = getSettings()


miniapp = FastAPI()


# globally-accessible objects:
docClassifier = None

@miniapp.on_event("startup")
def onStartup():
    global docClassifier
    #
    settings = getSettings()
    #
    # location of the model data files
    API_BASE_DIR = pathlib.Path(__file__).resolve().parent
    MODEL_DIR = API_BASE_DIR / settings.model_directory
    CLASSIFY_HD_PATH = MODEL_DIR / 'doc_classify_model.h5'
    CLASSIFY_TOKENIZER_PATH = MODEL_DIR / 'doc_tokenizer.json'
    CLASSIFY_METADATA_PATH = MODEL_DIR / 'doc_metadata.json'
    print(CLASSIFY_METADATA_PATH)
    # actual loading of the classifier model
    docClassifier = ClassifyModel(
        modelPath=CLASSIFY_HD_PATH,
        tokenizerPath=CLASSIFY_TOKENIZER_PATH,
        metadataPath=CLASSIFY_METADATA_PATH,
    )


@miniapp.get('/')
def basic_info():
    settings = getSettings()
    # prepare to return the non-secret settings...
    info = {
        k: v
        for k, v in settings.dict().items()
    }
    # done.
    return info


@miniapp.post('/classify_document')
def single_text_prediction(query: SingleTextQuery):
    result = docClassifier.predict([query.document_text])[0]
    result["message"] = "classification successfully"
    return PredictionResult(**result)


@miniapp.post('/classify_documents')
def multiple_text_predictions(query: MultipleTextQuery):
    results = docClassifier.predict(query.texts)
    return results
