import anvil.server
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

home_form = None

def get_form():
  if home_form is None:
    raise Exception('You must set the Home Form First.')
  return home_form

def go_bot():
  from ..BotFormComponent import BotFormComponent
  form = get_form()
  form.load_cmpt(BotFormComponent())
pass

def go_bruteforce():
  from ..BruteForceFormComponent import BruteForceFormComponent
  form = get_form()
  form.load_cmpt(BruteForceFormComponent())

def go_Dictionary():
  from ..addDictionaryComponent import addDictionaryComponent
  form = get_form()
  form.load_cmpt(addDictionaryComponent())

def go_DetailedGuide():
  from ..DetailedGuideComponent import DetailedGuideComponent
  form = get_form()
  form.load_cmpt(DetailedGuideComponent())
  

