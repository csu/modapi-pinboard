import requests

def perform_backup(send_notification, uploader, notifier):
    url = 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=%s' % secrets.PINBOARD_AUTH_TOKEN
    result = requests.get(url).json()

    uploader.quick_upload(result,
        file_prefix='pinboard', folder=secrets.BACKUP_FOLDER_ID)

    if send_notification:
        notifier.quick_send('Backed up %s Pinboard bookmarks.' % len(items))