# -*- coding: utf-8 -*-

"""Contains decorator classes

"""

__docformat__ = "restructuredtext"

__authors__ = ['"Hannah Dold" <hannah.dold@mailbox.tu-berlin.de>',
               '"Rike-Benjamin Schuppner" <rikebs@debilski.de>']

def autoappend(a_list):
    """ Decorator which automatically appends the decorated class or method to a_list.

    Usage::

        classes = []

        @autoappend(classes)
        class A(object):
            pass

        @autoappend(classes)
        class B(object):
            pass

        assert classes == [A, B]

    """
    def wrapper(obj):
        a_list.append(obj)
        return obj
    return wrapper

if __name__ == '__main__':
    pass
