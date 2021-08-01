from ._anvil_designer import ItemTemplateAttachmentTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from HashRouting import routing

class ItemTemplateAttachment(ItemTemplateAttachmentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    if routing.get_url_hash() == '':
      self.button_delete.visible = True
  
  def sec_str(self, sec):
    return f"{int(sec/60)}:{sec%60}"

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.raise_event('x-delete')
    routing.remove_from_cache('history')


