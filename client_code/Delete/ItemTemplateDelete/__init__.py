from ._anvil_designer import ItemTemplateDeleteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplateDelete(ItemTemplateDeleteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    if alert(f"Confirm deletion of {self.item['session']}",title='Delete Entire Season',buttons=[('Yes', True)]):
      self.parent.raise_event('x-delete', session=self.item)

