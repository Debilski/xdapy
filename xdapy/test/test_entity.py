# -*- coding: utf-8 -*-

"""Entity basic tests."""

# alphabetical order by last name, please
from sqlalchemy.exc import IntegrityError

__authors__ = ['"Rike-Benjamin Schuppner" <rikebs@debilski.de>']

from xdapy import Connection, Mapper, Entity
from xdapy.structures import create_entity, BaseEntity
from xdapy.errors import EntityDefinitionError
import unittest


declared_params = {
                'project': 'string',
                'experimenter': 'string'
            }

declared_params_w_date = {
                'project': 'string',
                'experimenter': 'string',
                'project_start': 'date'
            }


class TestEntity(unittest.TestCase):
    def setUp(self):
        class Experiment(Entity):
            declared_params = declared_params

        class ExperimentalProject(Entity):
            declared_params = declared_params
        
        self.Experiment = Experiment
        self.ExperimentalProject = ExperimentalProject

    def test_BaseEntity_raises(self):
        self.assertRaises(TypeError, BaseEntity.__init__, "")
    
    def test_same_entity_has_same_hash(self):
        class Experiment(Entity):
            declared_params = declared_params
        self.assertEqual(self.Experiment.__name__, Experiment.__name__)

    def test_different_entity_has_different_hash(self):
        class Experiment(Entity):
            declared_params = declared_params_w_date
        self.assertNotEqual(self.Experiment.__name__, Experiment.__name__)

        self.assertNotEqual(self.Experiment.__name__, self.ExperimentalProject.__name__)

    def test_entities_must_not_contain_underscore(self):
        self.assertRaises(EntityDefinitionError, create_entity, "Some_Entity", {})

    def test_entity_must_not_contain_more_than_one_underscore(self):
        self.assertRaises(EntityDefinitionError, create_entity, "Some_other_Entity", {})

    def test_may_create_entity_with_correct_hash(self):
        Experiment = create_entity("Experiment_b95e622546d303f14f7ceaca2e8e316c", declared_params)
        self.assertEqual(self.Experiment.__name__, Experiment.__name__)
        self.assertNotEqual(self.Experiment, Experiment)

    def test_entity_without_declared_params(self):
        def no_declared_params():
            class NoParamsEntity(Entity):
                pass
            return NoParamsEntity

        self.assertRaises(AttributeError, no_declared_params)

    def test_entity_with_inknown_declared_params(self):
        def bad_declared_params():
            class BadParamsEntity(Entity):
                declared_params = {
                    "some_p": "unknown"
                }
            return BadParamsEntity

        self.assertRaises(ValueError, bad_declared_params)

    def test_set_type(self):
        class E0(Entity):
            declared_params = {
                "q": "integer"
            }

        class E1(Entity):
            declared_params = {
                "q": "integer",
                "q1": "integer"
            }

        e0 = E0(q=100)
        self.assertEqual(e0._type, E0.__name__)

        self.assertRaises(TypeError, setattr, e0, "_type", 100)

        e0._type = E0
        self.assertEqual(e0._type, E0.__name__)

        e0._type = E1
        self.assertEqual(e0._type, E1.__name__)

    def test_simple_type_change_does_not_work(self):
        # (though it would be nice if it did)
        class E0(Entity):
            declared_params = {
                "q": "integer"
            }

        class E1(Entity):
            declared_params = {
                "q": "integer",
                "q1": "integer"
            }

        e0 = E0(q=100)
        e0._type = E1

        e0.params["q"] = 0
        self.assertRaises(KeyError, e0.params.__setitem__, "q1", 0)


class TestSavedTypes(unittest.TestCase):
    def setUp(self):

        class MyTestEntity(Entity):
            declared_params = { "some_param": "string" }

        self.MyTestEntity = MyTestEntity

        self.connection = Connection.test()
        self.connection.create_tables()
        self.m = Mapper(self.connection)
        
        self.m.register(self.MyTestEntity)
        
    def tearDown(self):
        self.connection.drop_tables()
        # need to dispose manually to avoid too many connections error
        self.connection.engine.dispose()


    def test_entity_type_is_correct(self):
        ent = self.MyTestEntity(some_param = "a short string")
        self.assertEqual(ent.type, "MyTestEntity")
        self.assertEqual(ent._type, "MyTestEntity_0b97eed8bcd1ab0ceb7370dd2f9d8cb9")

        self.m.save(ent)
        self.assertEqual(ent.type, "MyTestEntity")
        self.assertEqual(ent._type, "MyTestEntity_0b97eed8bcd1ab0ceb7370dd2f9d8cb9")

        found = self.m.find(Entity).one()
        self.assertEqual(found.type, "MyTestEntity")
        self.assertEqual(found._type, "MyTestEntity_0b97eed8bcd1ab0ceb7370dd2f9d8cb9")

    def test_entity_type_is_class_name(self):
        ent = self.MyTestEntity(some_param = "a short string")
        self.assertEqual(ent._type, ent.__class__.__name__)

    def test_polymorphic_id_is_type(self):
        ent = self.MyTestEntity(some_param = "a short string")
        self.assertEqual(ent._type, ent.__mapper_args__["polymorphic_identity"])


class NameEntityAutoId(Entity):
    declared_params = {
        "first_name": "string",
        "last_name": "string",
        }

class NameEntity(Entity):
    declared_params = {
        "first_name": "string",
        "last_name": "string",
        }
    def gen_unique_id(self):
        return "%s %s" % (self.params["first_name"], self.params["last_name"])


class TestUniqueId(unittest.TestCase):
    def setUp(self):
        self.connection = Connection.test()
        self.connection.create_tables()
        self.m = Mapper(self.connection)
        self.m.register(NameEntityAutoId)
        self.m.register(NameEntity)

    def tearDown(self):
        self.connection.drop_tables()
        # need to dispose manually to avoid too many connections error
        self.connection.engine.dispose()

    def test_unique_id(self):
        user = NameEntity(first_name="David", last_name="Persaud")
        self.assertTrue(user._unique_id is None)
        self.m.save(user)
        self.assertEqual(user.unique_id, "David Persaud")

        # does not work twice

        user2 = NameEntity(first_name="David", last_name="Persaud")
        self.assertTrue(user2._unique_id is None)
        self.assertRaises(IntegrityError, self.m.save, user2)
        # setting it manually
        user2._unique_id = "David Persaud (II)"
        # now it works
        self.m.save(user2)
        self.assertEqual(user2.unique_id, "David Persaud (II)")

    def test_auto_gen_unique_id(self):
        user = NameEntityAutoId(first_name="David", last_name="Persaud")
        self.assertTrue(user._unique_id is None)
        self.m.save(user)
        # it is something completely different
        self.assertTrue(user._unique_id is not None)
        self.assertNotEqual(user.unique_id, "David Persaud")

        # does work twice
        
        user2 = NameEntityAutoId(first_name="David", last_name="Persaud")
        self.assertTrue(user2._unique_id is None)
        self.m.save(user2)
        # it is something completely different
        self.assertTrue(user2._unique_id is not None)
        self.assertNotEqual(user2.unique_id, "David Persaud")

        self.assertNotEqual(user._unique_id, user2._unique_id)



if __name__ == "__main__":
    unittest.main()
