import os

config = {
    'attachment_path': os.environ.get('FILE_BASE_PATH', 'temp'),
    'root_path': os.environ.get('FILE_ROOT_PATH', 'static')
}
