from weasyprint import HTML, CSS
import json
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request

templates = Jinja2Templates(directory="../templates")

#テンプレートとなるhtmlファイルを読み込む
html_filename = "template/template.html"

#出力するPDFファイル名 
output_filename = 'output.pdf'



def convert_pdf(request: Request):
    #json_open = open('../data/test.json', 'r')
    #json_load = json.load(json_open)
    
    payload = {"name": "shintaro", "total": 1234}
    return templates.TemplateResponse("template.html", {"request": request, "payload": payload})
    html = HTML(filename=html_filename)
    html.write_pdf(output_filename)
    
    
if __name__ == '__main__':
    convert_pdf("re")