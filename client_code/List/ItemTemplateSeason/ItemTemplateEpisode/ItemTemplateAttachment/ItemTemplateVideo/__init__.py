from ._anvil_designer import ItemTemplateVideoTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class ItemTemplateVideo(ItemTemplateVideoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
  
  
  def convert_bytes(self, size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

    return size
  
  def resolution_str(self, res, w, h):
    return f"{res} [ {w} x {h} ]"