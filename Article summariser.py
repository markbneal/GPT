# How to use GPT-4 to summarize documents for your audience

# https://generative-ai-newsroom.com/how-to-use-gpt-4-to-summarize-documents-for-your-audience-18ecfe2ad6a4

# https://colab.research.google.com/drive/1EckuVSCJCPgIiz7fzQh4gRJRrC9j5Mss

!pip install openai
!pip install tiktoken
!pip install pdfplumber
!pip install requests
!pip install arxiv

# Added to pip install
!pip install pandas
!pip install scikit-learn
!pip install scipy 
!pip install matplotlib
!pip install numpy
!pip install sklearn
!pip install IPython
!pip install python-decouple

import pandas as pd
from sklearn.metrics import mean_squared_error
import openai
import json
import time
from openai.error import RateLimitError
import tiktoken
import requests
import pdfplumber
import io
from IPython.display import Markdown
import arxiv
from pathlib import Path
import os
from decouple import config

# TODO - Copy your Open AI Secret Key here
#not good practice in text
openai.api_key = "sk-myapikey"
openai.api_key

#better to use environment variables, but not clear how to access posit connect to do this?
# maybe this? 
# https://docs.posit.co/connect/user/accessing/#api-keys-from-code
#os.getenv(GPTAPI)
# export GPT_API=sk-test # in terminal?
# os.environ['GPT_API'] = 'sk-test' # in script, not permanently stored on workbench
openai.api_key = os.getenv("GPT_API")
print(os.getenv("GPT_API"))

# or this works on workbench (.env file has format GPTAPI=sk-myapikey, new line at end)
# https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5
openai.api_key = config('GPTAPI')


# or backup (File is key only, no new line after)
# openai.api_key = Path('GPTAPI.txt').read_text()


def getPDFText(url):
  # download the file
  response = requests.get(url)

  document_text = ""

  # load the PDF file using pdfplumber
  with pdfplumber.open(io.BytesIO(response.content)) as pdf:
      # iterate over all the pages in the PDF file
      for page in pdf.pages:
          # extract the text from the page
          text = page.extract_text()

          document_text = document_text + " " + text

  return document_text

def getAbstract(paper_id):
  # Search for the paper with the given ID
  search = arxiv.Search(id_list=[paper_id])
  paper = next(search.results())

  # Extract the abstract text
  abstract_text = paper.summary
  return abstract_text

def summarize(document_prompt, user_prompt, system_prompt, model, temp=.7, tokens=750):
  response = openai.ChatCompletion.create(
          model=model,
          messages=[{"role": "system", "content": system_prompt},
                    {"role": "user", "content": document_prompt},
                    {"role": "user", "content": user_prompt}],
          temperature=temp, 
          max_tokens=tokens,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
  output_summary = response["choices"][0]["message"]["content"]
  return output_summary
# End
1

#Testing Paper 1

# Example
document_text = getPDFText("https://arxiv.org/pdf/2304.00228.pdf")
abstract_text = getAbstract("2304.00228")

# Mine
document_text = getPDFText("https://github.com/markbneal/GPT/raw/730481c6e46ac234c942547f4c38775b0753991a/1-s2.0-S1751731118002471-main.pdf")

system_prompt = "You are a research assistant. Return your results in Markdown format." 
document_prompt = "You will accurately answer questions about the following research paper: " + document_text
model = "gpt-3.5-turbo"
extracted_info = []

user_prompt = "What research question is the paper trying to answer? Explain what the researchers did to\
 study that question, including the specific methods used and analyses performed. Explain thoroughly and be sure to include specific details."
t = summarize(document_prompt, user_prompt, system_prompt, model)
display(Markdown(t))
extracted_info.append(t)
# Error - Too many tokens in my doc


user_prompt = "What are the key findings reported in the paper that are important for journalists such as reporters and editors?\
How might journalists such as reporters and editors benefit from these findings? Why might there still be limits to those benefits? \
 Explain thoroughly and be sure to include specific details."
t = summarize(document_prompt, user_prompt, system_prompt, model)
display(Markdown(t))
extracted_info.append(t)

user_prompt = "Critique the findings of the paper, focusing on their validity and utility for journalists such as reporters and editors.\
Are there reasons not to trust any of the findings? Explain thoroughly and be sure to include specific details."
t = summarize(document_prompt, user_prompt, system_prompt, model)
display(Markdown(t))
extracted_info.append(t)

system_prompt = "You are a news reporter writing an article for an online blog. Return your results in Markdown format." 
document_prompt = "Here is a research paper abstract: " + abstract_text
user_prompt = "Here are some important observations about that research paper: " + extracted_info[0] + " " + extracted_info[1] + " " + extracted_info[2] + "\n\n "\
+  "Write a 600 word article about the paper using only the paper text and the important observations about \
the paper above and focusing on the benefits and limitations of the findings for journalists. \
Reduce scientific jargon and technical terminology in the writing."
t = summarize(document_prompt, user_prompt, system_prompt, model, temp=0.1, tokens = 1200)
display(Markdown(t))


# Testing Paper 2 (not included, see source)

# Plagiarism Check
!pip install -U pip setuptools wheel
!pip install -U spacy

input_text = ""
output_text = ""

out_doc = nlp(output_text)
in_doc = nlp(input_text)
out_doc_sents = [s for s in out_doc.sents]
in_doc_sents = [s for s in in_doc.sents]

for s1 in out_doc_sents:
  for s2 in in_doc_sents:
    t1 = [token.text for token in s1]
    t2 = [token.text for token in s2]
    o = set(t1).intersection(t2)
    score = len(o) / min(len(t1), len(t2))
    if score > .8:
      print ("---HIT---")
      print (s1)
      print (s2)
      print ("Score: {:.4f}\n".format(score))
