from ._anvil_designer import BotFormComponentTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server



class BotFormComponent(BotFormComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btnRespond_click(self, **event_args):
    if not self.txtQuestion.text:
      Notification("Invalid Input: Please enter your question.").show()
      return
    
    question = self.txtQuestion.text
    input = f'The question is {question}.'
    Notification("Question Received: Please wait for my response :)").show()
    description = anvil.server.call('generate_description', input)
    self.txtOutput.content = description
  pass

  def txtQuestion_pressed_enter(self, **event_args):
    self.btnRespond_click()
    pass
