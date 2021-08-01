from ._anvil_designer import UploadTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from HashRouting import routing

@routing.route("upload")
class Upload(UploadTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.handle_file(None)

  def handle_file(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.json_file = file
    if file and file.content_type == 'application/json':
      self.label_content.text = file.get_bytes().decode('utf-8')
      self.label_preview.visible = True
    else:
      self.label_preview.visible = False
      self.label_content.text = ''

  def continue_click(self, **event_args):
    """This method is called when the button is clicked"""
    passwrd = self.text_box_password.text
    if anvil.server.call('check_pass', passwrd):
      if self.json_file:
        is_saved = anvil.server.call('store_json', self.json_file)
        self.file_loader_main.clear()
        self.json_file = None
        if is_saved:
          Notification('File uploaded').show()
          routing.clear_cache()
        else:
          Notification('Something Went wrong').show()
      else:
        Notification('Please choose a file').show()
    else:
      Notification('Incorrect Password. Max 3 tries only.').show()

