#!/usr/bin/python
from flask import Flask, request, redirect, send_file
import random
import requests
import json
import os

__doc__ = '''
    just a app provide dynamic background for google page
'''

app = Flask(__name__)

PIC_DIR = 'pic'
PICS_FILE = 'picture_addresses.json'

with open(PICS_FILE, 'r+') as f:
    picture_addresses = json.loads(f.read())['data']

picture_addresses += [PIC_DIR + '/' + filename for filename in os.listdir(PIC_DIR)]
new_picture = []


def savePic():
    with open(PICS_FILE, 'w+') as f:
        f.write(json.dumps({'data': picture_addresses}))

@app.route('/background')
def background():
    index = random.randint(0, len(picture_addresses))
    url = picture_addresses[index]
    if url.startswith('http'):
        return redirect(url)
    else:
        return send_file(url, mimetype='image/' + url.split('.')[-1])


@app.route('/background/add')
def background_add():
    url = request.form.get('url')
    try:
        background = requests.get(url)
        picture_addresses.append(url)
        new_picture.append(url)
        if len(new_picture) == 20:
            savePic()
            new_picture.clear()

        return 'success' + str(type(background))
    except:
        return 'failed'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9410)
