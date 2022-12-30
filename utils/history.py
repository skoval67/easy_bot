from database.core import db, History


def write_history(command, hotels):
  History(command=command, hotels = hotels).save()
