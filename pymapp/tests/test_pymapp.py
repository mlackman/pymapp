import unittest
import pymapp

class TestMapping(unittest.TestCase):

  def test_simple_attribute(self):

    class MyObject(object):

      def __init__(self):
        self.id = 5

      def __eq__(self, o):
        return self.id == o.id


    class MyObjectMapper(pymapp.Mapper):
      __target_class__ = MyObject
      id = pymapp.Attribute('id')

    mapper = MyObjectMapper()
    self.assertEquals(mapper.to_hash(MyObject()), dict(id=5))
    self.assertEquals(mapper.from_hash(dict(id=5)), MyObject())

  def test_list_attributes(self):
    class MyObject(object):
      def __init__(self):
        self._list = [1,2,3,4]

      def __eq__(self, o):
        return self._list == o._list

    class MyObjectMapper(pymapp.Mapper):
      __target_class__ = MyObject
      mylist = pymapp.Attribute('_list')

    mapper = MyObjectMapper()
    self.assertEquals(mapper.to_hash(MyObject()), dict(mylist=[1,2,3,4]))
    self.assertEquals(mapper.from_hash(dict(mylist=[1,2,3,4])), MyObject())

  def test_compound_object(self):
    class Composite(object):
      def __init__(self):
        self.variable = 5
      def __eq__(self, o):
        return self.variable ==  o.variable
    class MyObject(object):
      def __init__(self):
        self.id = 5
        self.comp = Composite()
      def __eq__(self, o):
        return self.id == o.id and self.comp == o.comp

    class CompositeMapper(pymapp.Mapper):
      __target_class__ = Composite
      variable = pymapp.Attribute('variable')

    class MyObjectMapper(pymapp.Mapper):
      __target_class__ = MyObject
      comp = pymapp.Relation('comp', CompositeMapper())
      id   = pymapp.Attribute('id')

    mapper = MyObjectMapper()
    self.assertEquals(mapper.to_hash(MyObject()), dict(comp=dict(variable=5), id=5))
    self.assertEquals(mapper.from_hash(dict(comp=dict(variable=5), id=5)), MyObject())

  def test_list_of_compound_objects(self):
    class Composite(object):
      def __init__(self):
        self.variable = 5
      def __eq__(self, o):
        return self.variable ==  o.variable
    class MyObject(object):
      def __init__(self):
        self.id = 5
        self.composites = [Composite(), Composite()]

      def __eq__(self, o):
        return self.id == o.id and self.composites == o.composites

    class CompositeMapper(pymapp.Mapper):
      __target_class__ = Composite
      variable = pymapp.Attribute('variable')

    class MyObjectMapper(pymapp.Mapper):
      __target_class__ = MyObject
      composites = pymapp.ListRelation('composites', CompositeMapper())
      id        = pymapp.Attribute('id')

    mapper = MyObjectMapper()
    self.assertEquals(mapper.to_hash(MyObject()), dict(composites=[dict(variable=5), dict(variable=5)], id=5))
    self.assertEquals(mapper.from_hash(dict(composites=[dict(variable=5), dict(variable=5)], id=5)), MyObject())


