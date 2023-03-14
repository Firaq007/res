from fastapi import FastAPI,File, UploadFile
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
import openai
import aspose.words as aw
import requests
import os
import json


app = FastAPI()


k="Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/"
openai.api_key = "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"


@app.post("/files/")
async def create_file(file: UploadFile = File(...)):
    file_location = os.path.join(r"uploads",file.filename)
    with open(file_location, "wb+") as destination:
        for chunk in file.file:
            destination.write(chunk)
    doc = aw.Document(file_location)  
    doc.save("doc-to-text.txt") 
    read_file="doc-to-text.txt"
    with open(read_file, "r",encoding="utf8") as f:
        content = f.read()[80:-1]
        Content=str(content)
        K=Content.replace(k, '')
        prompt="Fill the following fields  #1 candidate name: #2 phone number:,#3 email id:, #4: Previous Job & Company Name,#5 Graduation College: , from the following resume and please leave the field blank if it doesn't exist "+K
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1024)
        brainstorming_output = response['choices'][0]['text']
        print(brainstorming_output)
        return {"Parsed Resume": response}
    





