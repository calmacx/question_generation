FROM python:3.8
RUN pip install transformers==3.0.0
RUN pip install nltk
RUN pip install nlp==0.2.0
RUN python -m nltk.downloader punkt
RUN pip install torch --no-cache-dir

WORKDIR /nlp/
COPY ./ /nlp/
#RUN mv /nlp/data/cache /root/.cache

RUN python run_custom.py input.txt
CMD ["python","run_custom.py"]