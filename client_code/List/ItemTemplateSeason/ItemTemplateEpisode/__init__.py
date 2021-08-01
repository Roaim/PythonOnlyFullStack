from ._anvil_designer import ItemTemplateEpisodeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from HashRouting import routing

class ItemTemplateEpisode(ItemTemplateEpisodeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.repeating_panel_attachment.set_event_handler('x-delete', self.delete_item)

  def delete_item(self, **args):
    self.parent.raise_event('x-delete', episode=self.item)
  
  def convert_timestamp(self, ts):
    if routing.get_url_hash() == 'history':
      return self.item['updated']
    return datetime.fromtimestamp(int(ts)).strftime('%a %d %b, %Y %I:%M:%S %p')

