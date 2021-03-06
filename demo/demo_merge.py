# -*- coding: utf-8 -*-

from xdapy import Connection, Mapper, Entity

connection = Connection.profile("demo") # use standard profile
connection_2 = Connection.default() # use standard profile
# drop the old database structure
connection.create_tables()
connection_2.create_tables()

m = Mapper(connection)
m_2 = Mapper(connection_2)

# from objects import Experiment, ...

class Experiment(Entity):
    """Concrete class for experiments"""    
    declared_params = {
        'experimenter': 'string',
        'project': 'string'
    }

Experiment_nodate = Experiment

class Experiment(Entity):
    """Concrete class for experiments"""    
    declared_params = {
        'experimenter': 'string',
        'project': 'string',
        'date': 'date'
    }

class Trial(Entity):
    declared_params = {
        'date': 'datetime',
        'number_of_runs': 'integer'
    }
    # holds data

class Observer(Entity):
    """Concrete class for observers"""
    declared_params = {
        'name': 'string',
        'age': 'integer',
        'glasses': 'boolean'
    }


# available types:
#    'integer', 'float', 'string', 'date', 'time', 'datetime', 'boolean'

# Next: register the objects
m.register(Experiment_nodate)
m_2.register(Experiment)
m.register(Trial)
m.register(Observer)

# for this data we have the convention:
# each Trial has one Experiment it belongs to. (parent–child relationship)
# Observers don’t belong to anything but Trials can hold a connection to an Observer.


e1 = Experiment(project="My Project", experimenter=u"Dareios Marika Nainsí")
e2 = Experiment(project="My Project", experimenter=u"Malin Calliope Lilly")
e2.parent = e1
e3 = Experiment(project="My Project", experimenter=u"Ilinka Iodocus")
m.save(e1, e2, e3)

e3.data["a"].put("Some Data")
e3.data["b"].put("Even more data")


e4 = Experiment(project="My other Project", experimenter="Nichol Pauline")
m_2.save(e4)

e3.attach("O", e1)
m.save(e3, e2)

mapping = {Experiment_nodate: Experiment}

from sqlalchemy.orm import exc

def migrate_obj(obj, old_mapper, new_mapper, mapping):
    klass = obj.__class__
    mapto = klass
    if klass in mapping:
        mapto = mapping[klass]
    
    # check, if unique_id is already present
    try:
        new_obj = new_mapper.find_by_unique_id(obj.unique_id) # TODO Deal with closed sessions
    except exc.NoResultFound:
        new_obj = mapto(_unique_id = obj.unique_id)
    except exc.MultipleResultsFound:
        raise DataInconsistencyError("unique_id in mapper {0} is not unique".format(new_mapper))

    # copy params
    for k,v in obj.params.iteritems():
        new_obj.params[k] = v

    new_mapper.save(new_obj)

    # copy data
    new_obj.data.copy(obj.data)

def migrate(old_mapper, new_mapper, mapping):
    for obj in old_mapper.find_roots():
        migrate_obj(obj, old_mapper, new_mapper, mapping)

from xdapy.structures import Context
from sqlalchemy.orm.exc import NoResultFound
def migrate_connections(m1, m2):
    conn1 = m1.find(Context)
    for c1 in conn1:
        from_unique_id = c1.holder.unique_id
        to_unique_id = c1.attachment.unique_id
        name = c1.connection_type

        print from_unique_id, to_unique_id

        try:
            m2_from = m2.find_by_unique_id(from_unique_id)
            m2_to = m2.find_by_unique_id(to_unique_id)
            m2_from.attach(name, m2_to)
        except NoResultFound:
            pass

migrate(m, m_2, mapping)
migrate(m_2, m, mapping)

migrate_connections(m, m_2)

print m.find_roots()
print m_2.find_roots()


assert len(m.find_roots()) == len(m_2.find_roots())

