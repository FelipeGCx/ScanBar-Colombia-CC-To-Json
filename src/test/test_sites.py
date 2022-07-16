import sys
sys.path.append("./src/logic")

from sites import search_site

def test_answer():
    assert search_site('12','001') == {
        'departament' : 'CESAR',
        'municipality' : 'VALLEDUPAR'
    }