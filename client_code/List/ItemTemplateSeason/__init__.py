from ._anvil_designer import ItemTemplateSeasonTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class ItemTemplateSeason(ItemTemplateSeasonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.repeating_panel_episode.set_event_handler('x-delete', self.delete_item)
  
  
  def delete_item(self, episode, **args):
    is_delete = anvil.server.call('delete_episode', self.item['session'] ,self.repeating_panel_episode.items, episode)
    if is_delete:
      self.refresh_episodes()
    else:
      Notification('You are not authorized to delete').show()

  def button_session_click(self, **event_args):
    """This method is called when the button is clicked"""
    is_visible = self.repeating_panel_episode.visible
    self.repeating_panel_episode.visible = not is_visible
    icon = self.button_session.icon
    if icon == 'fa:caret-up':
      self.button_session.icon = 'fa:caret-down'
    else:
      self.button_session.icon = 'fa:caret-up'
    if not is_visible and self.repeating_panel_episode.items is None:
      self.refresh_episodes()
      
  
  def refresh_episodes(self, **args):
    episodes =  anvil.server.call('episodes', self.item['session'])
    self.repeating_panel_episode.items = episodes

