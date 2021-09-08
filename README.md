# URL Shortening Service Backend

This project is a submodule (backend) of the [URL Shortening Service repository](https://github.com/huishun98/url-shortening-service).

The live version can be found [here](https://url-shorterning-service.herokuapp.com/).

## Run locally
1. Set up virtual environment and install requirements
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Set up local MongoDB (at port 27017) and [frontend](https://github.com/huishun98/url-shortening-service-frontend)
3. Add the following environment variables
    - FRONTEND_URL_ONE (obtained by running [frontend](https://github.com/huishun98/url-shortening-service-frontend))
    - FRONTEND_URL_TWO (obtained by running [frontend](https://github.com/huishun98/url-shortening-service-frontend))
    - MONGO_INITDB_ROOT_USERNAME
    - MONGO_INITDB_ROOT_PASSWORD
4. Run the application: `python3 app.py`

## Notes for deployment on cloud
1. Add the following environment variables:
    - FRONTEND_URL_ONE
    - DATABASE_URL