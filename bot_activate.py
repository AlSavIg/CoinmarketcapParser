from bot import activate_bot


def set_config():
    import os
    os.system("pip install -r .\\requirements.txt")


if __name__ == '__main__':
    set_config()
    activate_bot()
