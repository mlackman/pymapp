
class Attribute(object):

  def __init__(self, target_attribute_name):
    self.target_attribute_name = target_attribute_name

  def set(self, target_object, value):
    target_object.__dict__[self.target_attribute_name] = value

  def get(self, target_object):
    return getattr(target_object, self.target_attribute_name)

  def satisfies(self, obj):
    assert hasattr(obj, self.target_attribute_name), \
      "MAPPING NOT SATISFIED: %s does not have attribute %s" % (str(obj.__class__), self.target_attribute_name)

class Relation(Attribute):
  "RelationSetter sets specisic class to target object attribute"""

  def __init__(self, object_target_attribute_name, mapper):
    super().__init__(object_target_attribute_name)
    self.mapper = mapper

  def get(self, target_object):
    value = super().get(target_object)
    return self.mapper.to_hash(value)

  def set(self, target_object, value):
    target_object.__dict__[self.target_attribute_name] = self.mapper.from_hash(value)

class ListRelation(Attribute):
  """Sets list of relation object to target object"""

  def __init__(self, object_target_attribute_name, mapper):
    super().__init__(object_target_attribute_name)
    self.mapper = mapper

  def get(self, target_object):
    values = super().get(target_object)
    return [self.mapper.to_hash(value) for value in values]

  def set(self, target_object, values):
    print(values)
    target_object.__dict__[self.target_attribute_name] = [self.mapper.from_hash(value) for value in values]
