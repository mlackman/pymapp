import collections
import inspect
import json


class Mapper(object):

  def __init__(self):
    if not hasattr(self, '__target_class__'):
      raise Exception("Define __target_class__")
    self.__mappings__ = collections.defaultdict(lambda: None)
    ignored_attributes = ['to_hash', 'from_hash']
    for attr in dir(self):
      if attr not in ignored_attributes and not attr.startswith('__') and not attr.endswith('__'):
        self.__mappings__[attr] = getattr(self, attr)

  def to_hash(self, obj):
    result = dict()
    for store_key, attribute in self.__mappings__.items():
      value = attribute.get(obj)
      result[store_key] = value
    return result

  def from_hash(self, hash):
    obj = self.__target_class__.__new__(self.__target_class__)
    for store_key, attribute in self.__mappings__.items():
      data = hash[store_key]
      attribute.set(obj, data)
    return obj

