# file name : index.py
# pwd : /IAFC_coffee/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
# 추가할 모듈이 있다면 추가

sendData = 1

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/main', methods=['GET'])
def index():
    # /main/index.html은 사실 /IAFC_coffee/app/templates/main/index.html을 가리킨다.
    global sendData
    sendData += 1

    return render_template('/main/index.html', sendDataHtml=sendData)