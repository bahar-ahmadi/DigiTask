FROM hub.indraproject.ir/baseimages/bi-python-dbdrivers:1.0
MAINTAINER <baharahmadi7798@gmail.com>

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

COPY . .

ENTRYPOINT ["python3"]
CMD [ "API.py" ]
