from unittest import TestCase
import fetch
from jac.record.MyRecord import MyRecord

__author__ = 'ajo'


class TestFetch(TestCase):


  def test_fetch(self):
    instance = fetch.Bcpao()
    mr = MyRecord(dict(legal='hi', legals='hi2'))
    instance.fetch(mr)
