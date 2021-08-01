from ._anvil_designer import HistoryTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from HashRouting import routing

@routing.route("history")
class History(HistoryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.refresh_history()
    
  def refresh_history(self, **arg):
    self.repeating_panel_1.items = anvil.server.call('histories')
#     self.refresh_data_bindings()
    

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if len(self.repeating_panel_1.items) > 0:
      is_cleared = anvil.server.call('clear_history')
      if is_cleared:
        self.refresh_history()
      else:
        Notification('You are not authorized to clear all').show()
