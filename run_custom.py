import sys
import json
from pipelines import pipeline
nlp = pipeline("question-generation",model="valhalla/t5-small-qg-prepend", qg_format="prepend")
#nlp = pipeline("e2e-qg")
#nlp = pipeline("multitask-qa-qg")


def get_questions(text):
    #with open(fname) as f:
    #   string = f.read()
    print( nlp(text))
    #oname = fname+"_qa.json"
    #with open(oname, 'w') as outfile:
    #    json.dump(questions, outfile)


if __name__ == "__main__":
    #fname = None
    #if len(sys.argv) < 2 :
    #    fname = 'input.txt'
    #else:
    text = " ".join(sys.argv[1:])
    get_questions(text)
