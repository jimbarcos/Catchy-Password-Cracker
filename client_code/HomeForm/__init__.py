from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .. import navigation

class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    navigation.home_form = self
    navigation.go_bruteforce()
    self.link_1.role = 'selected'

  def load_cmpt (self, cmpnt):
    self.content_panel.clear()
    self.content_panel.add_component(cmpnt)

  def link_bot_click(self, **event_args):
    if (self.link_bot.text == 'Ask Catchy'):
      navigation.go_bot()
      self.link_bot.text = 'Go Back'
    else:
      navigation.go_bruteforce()
      self.link_bot.text = 'Ask Catchy'
    pass

  def link_2_click(self, **event_args):
    navigation.go_Dictionary()
    self.link_1.role = None
    self.link_3.role = None
    self.link_2.role = 'selected'
    self.change_txt()
    pass

  def link_1_click(self, **event_args):
    navigation.go_bruteforce()
    self.link_3.role = None
    self.link_2.role = None
    self.link_1.role = 'selected'
    self.change_txt()
    pass

  def link_3_click(self, **event_args):
    navigation.go_DetailedGuide()
    self.link_1.role = None
    self.link_2.role = None
    self.link_3.role = 'selected'
    self.change_txt()
    pass

  def change_txt(self):
    self.link_bot.text = 'Ask Catchy'
