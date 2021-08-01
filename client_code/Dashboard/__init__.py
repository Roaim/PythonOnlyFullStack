from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from HashRouting import routing
from ..List import List
from ..Upload import Upload
from ..History import History
from ..Delete import Delete

@routing.main_router
class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.links = []
    # self.set_tag(self.link_list, 'list')
    self.set_tag(self.link_list, '')
    self.set_tag(self.link_history, 'history')
    self.set_tag(self.link_upload, 'upload')
    self.set_tag(self.link_delete, 'delete')
    # routing.set_url_hash('list')
    # print("init",properties)
  
  def set_tag(self, link, *args):
    self.links.append(link)
    link.tag.url_hash = args[0]

  def handle_nav_click(self, **event_args):
    """This method is called when the link is clicked"""
    # print("hnc", event_args)
    routing.set_url_hash(event_args['sender'].tag.url_hash)
  
  def on_navigation(self, **event_args):
    """This method is called when the link is clicked"""
    # print("on",event_args)
    for link in self.links:
      if link.tag.url_hash == event_args.get('url_hash'):
        link.role = 'selected'
        self.label_title.text = link.text
      else:
        link.role = 'default'