import os

def clean(paths):
    for path in paths:
        file_list = list(os.walk(path))[0][2]
        for f in file_list:
            os.remove(path+f)

if __name__ == "__main__":
    clean(['./freq/', './partition/'])