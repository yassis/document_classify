""" config.py """

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # first argument of 'Field' is the default
    api_name: str = Field('API Name', env='API_NAME')
    # ellipsis here means field is required
    model_version: str = Field(..., env='MODEL_VERSION')
    model_directory: str = Field(..., env='MODEL_DIRECTORY')
    #
    secret_fields: {}

    # this trick is redundant once we enforce a restricted Pydantic schema
    # on the route response, but ...
    # (see https://fastapi.tiangolo.com/tutorial/response-model/#add-an-output-model)


    # mock-model setting (usually False!)
    # This field will not be returned by the "/" endpoint thanks to the route
    # enforcing the response to be of type APIInfo.

    class Config:
        env_file = '.env'


@lru_cache()
def getSettings():
    return Settings()