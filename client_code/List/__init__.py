from ._anvil_designer import ListTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from HashRouting import routing

@routing.route("")
class List(ListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
#     self.repeating_panel_session.set_event_handler('x-refresh', self.refresh_items)
    self.refresh_items()
  
  def refresh_items(self, **args):
    self.repeating_panel_session.items = anvil.server.call('sessions')