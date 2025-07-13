from datetime import datetime
import peewee as pw
from json import dumps, loads


db = pw.SqliteDatabase('history\history.db')

class JSONField(pw.TextField):
  def db_value(self, value):
    return dumps(value)

  def python_value(self, value):
    if value is not None:
      return loads(value)

class History(pw.Model):
  created_at = pw.DateTimeField(default=datetime.now())
  user_id = pw.BigIntegerField()
  command = pw.TextField()
  hotels = JSONField()

  class Meta():
    database = db


db.connect()
db.create_tables([History])