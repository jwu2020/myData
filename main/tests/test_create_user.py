from main.tests.testing_settings import MongoTestCase
from mongoengine import Document, StringField


class Person(Document):
    name = StringField()


class CreateUserTestCase(MongoTestCase):
    def test_thing(self):
        pers = Person(name='John')
        pers.save()

        fresh_pers = Person.objects().first()
        self.assertEqual(fresh_pers.name, 'John')
