import sys
sys.path.append("./src/logic")
from decode import Decode


def run(file_name):
    Decode(file_name).run()

image_path = '' # your image path
run(image_path)