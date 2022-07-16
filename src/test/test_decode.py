import os
import sys
sys.path.append("./src/logic")
from dotenv import load_dotenv
from decode import Decode

load_dotenv()

def test_answer():
    file_name = os.getenv('BARCODE_PATH')
    Decode(file_name).run()

test_answer()

# def test_answer():
#    file_name = os.getenv['BARCODE_PATH']
#    assert Decode(file_name).run()