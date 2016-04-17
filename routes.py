from threading import Thread

from flask import Blueprint, jsonify, request

from backup import perform_backup
from common import require_secret
from config import config
import secrets

module = Blueprint(config['module_name'], __name__)

@module.route('/backup')
@module.route('/backup/')
@require_secret
def backup_all():
    send_notification = request.args.get('notify') is not None
    t = Thread(target=perform_backup, args=[send_notification, uploader, notifier])
    t.start()

    return jsonify({
        'status': 'started'
    })