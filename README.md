# usage example (django + requests)

```
import os

import requests
from django.conf import settings
from django.template import loader


import logging

from requests import Response

logger = logging.getLogger("pdf")


def get_template_file(tex_file_name: str):
    template = loader.get_template('subfolder1/tex/' + tex_file_name)
    return template


def generate_pdf_from_tex(tex_file_name: str, context: dict) -> Response:
    template = get_template_file(tex_file_name)
    rendered = template.render(context)
    template_path = os.path.dirname(template.origin.name)
    attachment_render_files = get_relevant_files(template_path)
    pdf = pdf_service_request(rendered, attachment_render_files)
    return pdf


def get_relevant_files(folder_path: str) -> list:
    files = []
    # for now append all files in the tex folder for now (simple ... not fast)
    for element in os.listdir(folder_path):
        file = os.path.normpath(os.path.join(folder_path, element))
        if os.path.isfile(file):
            files.append(file)
    return files


def pdf_service_request(main_tex: str, files: list) -> Response:

    files_send = {
        'main.tex': ('main.tex', main_tex, 'text/plain'),
        }

    for file in files:
        name = os.path.basename(file)
        files_send[name] = (name, open(file, 'rb'))

    pdf = requests.post(settings.PDF_SERVICE_URL,
                        files=files_send,
                            headers={'Authorization': 'Bearer ' + settings.PDF_SERVICE_KEY})
    if pdf.status_code == requests.codes.ok:
        return pdf
    else:
        logger.fatal(main_tex)
        logger.fatal(pdf.content.decode('utf-8'))
        raise Exception("Error requesting pdf with status: " + str(pdf.status_code))
``` 
