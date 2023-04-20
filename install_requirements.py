def set_config():
    import os
    os.system(f'pip install -r "{os.path.dirname(os.path.abspath(__file__))}/requirements.txt')


if __name__ == '__main__':
    set_config()
