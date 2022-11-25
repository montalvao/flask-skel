$env:FLASK_DEBUG = 'true'

flask --app skel.app run

Remove-Item Env:\FLASK_DEBUG
