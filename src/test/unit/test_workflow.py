import pytest
import workflow
from workflow import stage

def test_workflow():

    @stage('stage_one')
    def do_something(id):
        print "something"

    workflow.submit("stage_one", "asdf")