
from xdapy import Connection, Mapper
from xdapy.io import JsonIO

connection = Connection.profile("test") # use standard profile
connection.create_tables()#overwrite=True)
m = Mapper(connection)

from xdapy.structures import EntityObject
#class Ex(EntityObject):
#    parameter_types = {'project': 'string', 'citation': 'string', 'experimenter': 'string'}

#m.register(Ex)

#m.create_and_save("Ex", project="A new project")

# We create a new JSON importer.
# add_new_types = True so all defined and declared objects are imported
#jio = JsonIO(m, add_new_types=True)
#jio.ignore_unknown_attributes = True

#with open("demo/detection-format.json") as f:
#    objs = jio.read_file(f)

#for cls in m.registered_objects:
#    print """class {name}(EntityObject):\n    parameter_types = {types!r}\n""".format(name=cls.__original_class_name__, types=cls.parameter_types)

#print len(objs), "objects"

#print jio.write_string(objs)

class Experiment(EntityObject):
    parameter_types = {u'project': u'string', u'citation': u'string', u'experimenter': u'string'}

class Hardware(EntityObject):
    parameter_types = {u'graphicscard': u'string', u'monitor': u'string', u'monitorsize': u'string', u'stimuluscontroller': u'string', u'maxluminance': u'float', u'responsedevice': u'string', u'minluminance': u'float', u'calibrationdevice': u'string', u'operatingsystem': u'string'}

class Session(EntityObject):
    parameter_types = {u'count': u'integer', u'bitdepth': u'integer', u'viewingdistance': u'float', u'observerexperience': u'string', u'framerate': u'float', u'calibrationdate': u'date', u'xpixelresolution': u'float', u'ypixelresolution': u'float', u'date': u'date', u'observerknowledge': u'string', u'bitdepthmodification': u'string'}

class Observer(EntityObject):
    parameter_types = {u'birthyear': u'integer', u'initials': u'string', u'handedness': u'string', u'name': u'string', u'glasses': u'boolean'}

class Condition(EntityObject):
    parameter_types = {u'count': u'integer', u'observerexperience': u'string', u'observerknowledge': u'string', u'firstinterval': u'string', u'secondinterval': u'string'}

class Block(EntityObject):
    parameter_types = {u'count': u'integer', u'signalstrength': u'float', u'feedback': u'boolean', u'iti': u'float', u'responseinterval': u'float', u'isi': u'float', u'valid': u'boolean', u'performance': u'float', u'stimuluspresentationtime': u'float', u'numberoftrials': u'integer'}

class Trial(EntityObject):
    parameter_types = {u'count': u'integer', u'feedback': u'boolean', u'iti': u'float', u'responseinterval': u'float', u'note': u'string', u'isi': u'float', u'learning': u'boolean', u'rotation': u'float', u'stimuluspresentationtime': u'float'}

class Stimulus(EntityObject):
    parameter_types = {u'signalphase': u'float', u'nominalduration': u'float', u'pedestalphaseoffset': u'float', u'signalspatialfrequency': u'float', u'meanluminance': u'float', u'ysize': u'float', u'signalcontrast': u'float', u'pedestalspatialfrequency': u'float', u'xsize': u'float', u'maxluminance': u'float', u'minluminance': u'float', u'identifier': u'string', u'pedestalcontrast': u'float', u'shapetemporalwindow': u'string'}

class Response(EntityObject):
    parameter_types = {u'category': u'integer', u'rt': u'float', u'button': u'string', u'intime': u'boolean', u'correct': u'boolean'}

m.register(Experiment)

Experiment = m.entity_by_name("Experiment")


