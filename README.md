# Meduzzen_int_be_ua

1. Create and activate virtual environment 
py -3 -m venv venv
.\scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run server
uvicorn main:app --reload

4. Create image Docker
docker build -t conteiner_meduz .

5. Start the Docker Container
docker run -p 8000:8000 --name meduzz-app conteiner_meduz
#open URL http://localhost:8000 or http://127.0.0.1:8000