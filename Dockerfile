FROM python:3.8
RUN pip install transformers==3.0.0
RUN pip install nltk
RUN pip install nlp==0.2.0
RUN python -m nltk.downloader punkt
RUN pip install torch --no-cache-dir
RUN pip install pymongo
RUN pip install python-dotenv
RUN pip install wikipedia
RUN pip install pandas

WORKDIR /nlp/
COPY ./ /nlp/
#RUN mv /nlp/data/cache /root/.cache

RUN python run_wikipedia.py "Cactus" 
CMD ["python","run_custom.py"]