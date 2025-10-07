import app
from boddle import boddle

def test_webapp_index():
    with boddle(params={'name':'Derek'}):
        assert app.index() == 'What would you like to do?', 'invalid name'

#main routine
test_webapp_index()

