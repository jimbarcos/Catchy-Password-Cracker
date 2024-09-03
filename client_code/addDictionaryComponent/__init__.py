from ._anvil_designer import addDictionaryComponentTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .. import navigation
from .. import cacheDictionary
#from .ItemTemplate1 import ItemTemplate1



class addDictionaryComponent(addDictionaryComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.cacheDicionary = cacheDictionary.cacheList()
    self.cacheCount = cacheDictionary.cacheCount()
    self.repeating_panel_1.items = app_tables.tbldictionarylist.search(tables.order_by('dictionaryPasswords', ascending=True))
    self.label_1_copy.text = 'Dictionary List Count: {:,}'.format(int(self.count_rows()))


  def btnEdit_click(self, **event_args):
    secretKey = 'PiCatchyU'

    if secretKey == self.txtEdit.text:
      self.outlined_card_2.visible = False
      self.outlined_card_2_copy.visible = True
    else:
      Notification('Wrong Secret Key, please try again').show()
    pass

  def txtEdit_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.btnEdit_click()
    pass

  def txtSubmit_pressed_enter(self, **event_args):
    self.btnSubmit_click()
    pass

  def btnSubmit_click(self, **event_args):
    addedPass = self.txtSubmit.text
    addedPass = addedPass.strip()
    redundant = False
    if addedPass is None or addedPass == '' or addedPass == '\0':
      Notification('Please enter a character').show()
    else:
      dictionaryList = self.retrievedDictionary()
      for password in dictionaryList:
        if self.txtSubmit.text == password.strip():
          alert('Phrase already existed in the Database, terminating the insertion to the Dictionary List')
          redundant = True
          break
      
      if not redundant:
        app_tables.tbldictionarylist.add_row(dictionaryPasswords=addedPass)
        Notification('Successfully Saved').show()
        self.repeating_panel_1.items = app_tables.tbldictionarylist.search(tables.order_by('dictionaryPasswords', ascending=True))
        self.label_1_copy.text = 'Dictionary List Count: {:,}'.format(int(self.count_rows()))
        self.txtSubmit.text =''
    pass

  def txtEdit_change(self, **event_args):
    password = self.txtEdit.text
    if ' ' in password:
      password = password.replace(' ', '')
      self.txtEdit.text = password
    pass

  def txtSubmit_change(self, **event_args):
    password = self.txtSubmit.text
    if ' ' in password:
      password = password.replace(' ', '')
      self.txtSubmit.text = password
    pass

  def retrievedDictionary(self):
    retrieveList = app_tables.tbldictionarylist.search(tables.order_by('dictionaryPasswords', ascending=True))
    storeList = [row['dictionaryPasswords'] for row in retrieveList]

    return storeList

  def count_rows(self):
    tables = app_tables.tbldictionarylist.search()
    return str(len(tables))

