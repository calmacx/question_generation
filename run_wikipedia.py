import os
import sys
import json
import wikipedia
import pymongo
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

db_ip = os.environ.get('PUBQUAIZ_DB_IP')
db_port = os.environ.get('PUBQUAIZ_DB_PORT')
db_user = os.environ.get('PUBQUAIZ_DB_ADMIN_USER')
db_pwd = os.environ.get('PUBQUAIZ_DB_ADMIN_PWD')

client = pymongo.MongoClient(f"mongodb://{db_user}:{db_pwd}@{db_ip}:{db_port}/")
db = client["PubQuAIZ"]
m_dataset_names = db['CollectionLookup'].distinct("dataset")
print ('Test db connection...',m_dataset_names)

from pipelines import pipeline
nlp = pipeline("question-generation",model="valhalla/t5-small-qg-prepend", qg_format="prepend")
#nlp = pipeline("e2e-qg")
#nlp = pipeline("multitask-qa-qg")


def insert_into_db(qa,topic):
    dataset = db[f"WikiNLP"]
    if topic[0]=='"' and topic[-1]=='"':
        topic = topic[1:-1]
    for x in qa:
        x['topic'] = topic
    dataset.insert_many(qa)

    #get all the ids we just created
    ids = list(dataset.find({'topic':topic},{'_id':True}))
    print (ids)
    #make a pandas dataframe with these ids
    df = pd.DataFrame(ids).rename({'_id':'question_id'},axis=1)
    #make sure they're mapped to the original db name
    df['dataset'] = 'WikiNLP'
    #put these into the collection lookup db
    records = df.to_dict(orient='records')
    db['CollectionLookup'].insert_many(records)
    
    
    
def get_questions(text):
    qa = nlp(text)
    print (json.dumps(qa,indent=4))
    return qa

    
def get_text(topic):
    print ("Getting topic: ",topic)
    qa = get_questions(wikipedia.summary(topic))
    insert_into_db(qa,topic)
    print ('done')
    
if __name__ == "__main__":
    for topic in sys.argv[1:]:
        get_text(topic)
