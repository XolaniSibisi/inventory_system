import os


def recursor(dirpath):
    # print(dirpath)
    delfiles = []
    deldirs = []
    with os.scandir(dirpath) as l1:
        for e1 in l1:
            if not e1.is_file():
                with os.scandir(e1.path) as l2:
                    for e2 in l2:
                        if e2.name == 'migrations':
                            with os.scandir(e2.path) as l3:
                                for e3 in l3:
                                    if not e3.name == '__init__.py':
                                        print(e3.path)
                                        if e3.is_file():
                                            delfiles.append(e3.path)
                                        else:
                                            deldirs.append(e3.path)
                                            with os.scandir(e3.path) as l4:
                                                for e4 in l4:
                                                    delfiles.append(e4)
    yn = input('are you sure to delete all the files above?(y/n)')
    if yn == 'y':
        for dp in delfiles:
            os.remove(dp)
        for dp in deldirs:
            os.rmdir(dp)



recursor(os.path.dirname(os.path.realpath(__file__)))