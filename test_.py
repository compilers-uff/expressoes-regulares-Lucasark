import pytest
import er as er

def test_er():
    assert er.match("a", "a") == "OK"
    assert er.match("+(a,b)", "a") == "OK"
    assert er.match("+(a,b)", "ab") == "Not OK"  
    assert er.match("*(+(a,b))", "a") == "OK"
    assert er.match("*(+(a,b))", "aaa") == "OK"
    assert er.match("*(+(a,b))", "ab") == "OK"
    assert er.match("*(+(a,b))", "aba") == "OK"
    assert er.match("*(+(a,b))", "abababa") == "OK"
    assert er.match("*(+(.(a,b),.(c,d)))", "ab") == "OK"
    assert er.match("*(+(.(a,b),.(c,d)))", "cd") == "OK"
    assert er.match("*(+(.(a,b),.(c,d)))", "ac") == "Not OK"
    assert er.match("*(+(.(a,b),.(c,d)))", "db") == "Not OK"
    
    #Others