from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import navigation
from .. import addDictionaryComponent


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.displayData()

    # Any code you write here will run before the form opens.

  def displayData(self):
    self.lblPasswords.text = self.item['dictionaryPasswords']

    #repeating_panel_items = app_tables.tbldictionarylist.search(tables.order_by('dictionaryPasswords', ascending=True)
    #auto_increment_numbers = []


  def btnDelete_click(self, **event_args):
    self.outlined_1.visible = True
    Notification('Please type the secret key in the textbox, and pressed ENTER').show()

    
    pass

  def outlined_1_pressed_enter(self, **event_args):
    secretKey = 'PiCatchyu'

    self.outlined_1.visible = False
    if self.outlined_1.text == secretKey:
      self.item.delete()
      self.remove_from_parent()
      navigation.go_Dictionary()
    else:
      Notification('Wrong Secret Key').show()
      
    pass

  def outlined_1_change(self, **event_args):
    password = self.outlined_1.text
    if ' ' in password:
      password = password.replace(' ', '')
      self.outlined_1.text = password
    pass
