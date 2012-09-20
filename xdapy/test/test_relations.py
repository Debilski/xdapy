# -*- coding: utf-8 -*-

import unittest

from xdapy import Connection, Mapper, Entity

class Experiment(Entity):
    declared_params = {
        "project": "string"
    }

class Observer(Entity):
    declared_params = {
        "name": "string",
        "birthday": "date"
    }

class Session(Entity):
    declared_params = {
        "date": "date"
        }


class Trial(Entity):
    declared_params = {
        "duration": "integer",
        "number": "integer",
        "valid": "boolean"
    }

class TestRelations(unittest.TestCase):
    def test_all(self):
        exp_monorail = Experiment(project="The Monorail Project")
        exp_neptune = Experiment(project="Neptune Colonisation Project")

        obs_1 = Observer(name="n1")
        obs_2 = Observer(name="n2")
        obs_3 = Observer(name="n3")

        sess1 = Session()
        sess1.parent = exp_monorail
        sess2 = Session()
        sess2.parent = exp_monorail
        sess3 = Session()
        sess3.parent = exp_neptune

        trial1_1 = Trial()
        trial1_1.parent = sess1

        trial1_2 = Trial()
        trial1_2.parent = sess1

        trial2_1 = Trial()
        trial2_1.parent = sess2

        trial2_2 = Trial()
        trial2_2.parent = sess2

        trial3_1 = Trial()
        trial3_1.parent = sess3

        trial3_2 = Trial()
        trial3_2.parent = sess3

        db = Connection.test()
        db.create_tables()
        m = Mapper(db)
        m.register(Observer, Experiment, Trial)
        m.save(exp_monorail, exp_neptune)


        eeee = Experiment()
        oooo = Observer()
        eeee.attach("Obs", oooo)


        exp_monorail.attach("Observer", obs_1)
        exp_monorail.attach("Observer", obs_2)
        exp_neptune.attach("Observer", obs_1)


        # test print
        print exp_monorail.info()
        self.assertEqual(exp_monorail.info(),
            ("Experiment(id=1, project=u'The Monorail Project')\n"
             "[]"
             "\nhas 2 children and 6 siblings"))

        print ""
        print exp_neptune.info()
        self.assertEqual(exp_neptune.info(),
            ("Experiment(id=8, project=u'Neptune Colonisation Project')\n"
             "[]\n"
             "has 1 children and 3 siblings"))
        print ""
        print obs_1.info()
        print ""
        print trial1_1.info()

        # test print
        print exp_monorail.tree()
        print ""
        print exp_neptune.tree()
        print ""
        print obs_1.tree()

        self.assertEqual(obs_1.tree(),
            ("x- Observer(id=12, name=u'n1')\n"
             "  +- belongs to Experiment(id=1, project=u'The Monorail Project')\n"
             "  +- belongs to Experiment(id=8, project=u'Neptune Colonisation Project')\n"))

        print ""
        print trial1_1.tree()

        #exp_neptune.attach("C", obs_1)

        from xdapy.structures import Context

        print m.find_all(Context)
        #m.delete(obs_1)
        #print m.find_all(Context)

        m.delete(*m.find_all(Context))


        print m.find_all(Context)
        print m.find_all(Experiment)


        contx = m.find_first(Context)
        #m.registerConnection(Experiment, Observer, "Observer")

        exp_monorail.attach("Observer", obs_1)

        from xdapy.io import XmlIO
        xmlio = XmlIO(m, Entity.__subclasses__())
        print xmlio.write()

        db.drop_tables()
