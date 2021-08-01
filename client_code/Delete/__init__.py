from ._anvil_designer import DeleteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from HashRouting import routing

@routing.route('delete')
class Delete(DeleteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.repeating_panel_1.set_event_handler('x-delete', self.delete_item)
    self.refresh_list()
    
  def refresh_list(self):
    self.repeating_panel_1.items = anvil.server.call('sessions')
  
  
  def delete_item(self, session, **args):
    if anvil.server.call('delete_session', session):
      self.refresh_list()
      routing.clear_cache()
    else:
      Notification('Failed to delete. Maybe you are unauthorized to delete.').show()