from threading import Thread

from flask import Blueprint, jsonify, request
import requests

from common import require_secret
from config import config
import secrets

module = Blueprint(config['module_name'], __name__)

def perform_backup(send_notification):
    url = 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=%s' % secrets.PINBOARD_AUTH_TOKEN
    result = requests.get(url).json()

    uploader.quick_upload(result,
        file_prefix='pinboard', folder=secrets.BACKUP_FOLDER_ID)

    if send_notification:
        notifier.quick_send('Backed up %s Pinboard bookmarks.' % len(items))

@module.route('/backup')
@module.route('/backup/')
@require_secret
def backup_all_scrobbles():
    send_notification = request.args.get('notify') is not None
    t = Thread(target=perform_backup, args=[send_notification])
    t.start()

    return jsonify({
        'status': 'started'
    })