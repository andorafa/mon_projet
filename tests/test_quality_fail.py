def fail_quality():
    print("this is a test")  # code smell: lower case message
    print("this is a test")  # duplicated line

def fail_quality():
    pass  # function redefinition = bug
