from ._anvil_designer import BruteForceFormComponentTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import time
import itertools
from .. import navigation
from ..HomeForm import HomeForm

class BruteForceFormComponent(BruteForceFormComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.StopCode = False
    # Any code you write here will run before the form opens.

  # For the Catchy Title Animation
  def timer_tick(self, **event_args):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=<>?/.,;:[]{}|`~'
    message = 'Catchy'
    
    for i in range(len(message) + 1):
      for j in range(len(alphabet)):
        if i == len(message):
          break
        prefix = alphabet[j]
        current_str = message[:i] + prefix
        self.label_title.text = current_str
        time.sleep(0.0001)
        self.label_title.text = 'Catchy'
        self.timer.interval = 0.00
    return

  # Validating and knowing the search space of the characters to be processed
  def validateRange (self):
    characters = ''
    if self.lowercaseCB.checked:
      characters += 'abcdefghijklmnopqrstuvwxyz'
    if self.uppercaseCB.checked:
      characters += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if self.numbercaseCB.checked:
      characters += '1234567890'
    if self.specialcaseCB.checked:
      characters += r"""!@#$%^&*()-_=+[]\{}|;:'",.<>/?`~"""

    if characters == '' or self.passwordTxt.text.strip() == '':
      return None
    else:
      self.cardDisplay.visible = True
      self.ElapsedTimeTxt.visible = True
      self.TotalCombinationsTxt.visible = True
      return characters

  def delayValidation(self):
    try:
      delay = float(self.delayTxt.text)
    except ValueError:
      Notification("Invalid Input: Please enter a valid time delay.").show()
      return True
      
    input = self.passwordTxt.text.strip()
    
    if not input or input is None or input == '' or input =='\0':
      Notification("Invalid Input: Please enter a character.").show()
      return True
    if delay == 0.00:
      if not confirm('WARNING: A time delay of zero might cause your device to lag, do you want to proceed?'):
        self.stopCode = True
        return True
    if delay is None:
      Notification("Invalid Input: Please enter a time delay.").show()
      return True
    if delay < 0:
      Notification("Invalid Input: Time Delay must be a positive value.").show()
      return True
      
  # Action when the Generate Bruteforce Attack is clicked
  def btnBruteforce_click(self, **event_args):
    validateChar = self.validateRange()
    
    if validateChar is None:
      Notification("Invalid Range: \n\nPlease pick at least one Brute Force Range and enter a character").show()
      return
    
    badStart = self.delayValidation()
    rangeCheck = self.checkRange()

    if not badStart and rangeCheck:
      self.stringLabel.text = 'Mode: Bruteforce Attack'
      self.stringLabel.foreground = '#FFFFB3'
      self.timer_Bruteforce.interval = 0.0000000000000001 # starts the process of bruteforcing
      self.containerConfiguration()
      self.cardEvaluation.visible = True
      self.evaluatePass()

    rangeCheck = False
        
    pass

  def containerConfiguration(self):
    self.StopCode = False
    self.stopBtn.visible = True
    self.passAttemptTxt.foreground = '#F5F5F5' #white
    self.btnBruteforce.visible = False
    self.btnDictionary.visible = False
    self.cardCombinations.visible = True
    self.stringLabel.visible = True
    self.delayTxt.enabled = False
    self.passAttemptTxt.enabled = False
    self.lowercaseCB.enabled = False
    self.uppercaseCB.enabled = False
    self.numbercaseCB.enabled = False
    self.specialcaseCB.enabled = False
    
    pass

  def checkRange(self):
    lowerCase = list('abcdefghijklmnopqrstuvwxyz')
    upperCase = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    number = list('1234567890')
    specialChar = list('!@#$%^&*()_+-=<>?/.,;:[]{}|`~')

    validatedRange = self.passwordTxt.text + "\0"
    errorRange = False

    for char in validatedRange:
      if char in lowerCase and not self.lowercaseCB.checked:
        errorRange = True
        Notification('Entered text has characters within the Lower Case Alphabet range type\n\nPlease tick the correct range.').show()
        break
      if char in upperCase and not self.uppercaseCB.checked:
        errorRange = True
        Notification('Entered text has characters within the Upper Case Alphabet range type\n\nPlease tick the correct range.').show()
        break
      if char in number and not self.numbercaseCB.checked:
        errorRange = True
        Notification('Entered text has characters within the Number range type\n\nPlease tick the correct range.').show()
        break
      if char in specialChar and not self.specialcaseCB.checked:
        errorRange = True
        Notification('Entered text has characters within the Special Characters range type\n\nPlease tick the correct range.').show()
        break

    return not errorRange
    pass
      

  def product(self, iterables, repeat):
    pools = [tuple(pool) for pool in iterables] * repeat
    result = [[]]

    for pool in pools:
      result = [x + [y] for x in result for y in pool]
    return result

  
  # The process of Bruteforcing
  def timer_Bruteforce_tick(self, **event_args):
    characters = self.validateRange()
      
    try:
      password = self.passwordTxt.text.strip() + '\0'
    except Exception:
      Notification("Invalid Action: Stopping the Process").show()
      self.stopCode = True
      return

    try:
      delay = self.delayTxt.text
    except ValueError:
      delay = 0.01
    
    counter = 0
    maxLength = len(password) - 1
    method = ''

    if self.rbItertools.selected:
      method = itertools.product(characters, repeat=maxLength)
    else:
      #method = self.product([characters], maxLength)
      if len(password) > 0:
        if confirm('CONFIRMATION: Product Method is only practical for very small search spaces. This may cause an out of memory status on your end?\n\nYes = Continue\nNo = Use itertools'):
          method = self.product([characters], maxLength)
        else:
          method = itertools.product(characters, repeat=maxLength)
          self.rbItertools.selected = True


    if method != '':
      clockStart = time.time()
      # Bruteforce Algorithm
      for combination in method:
        if self.StopCode: #if stopcode is true then stop
          return
        if delay > 0.00:
          time.sleep(delay)
        current_time = time.time()
        counter += 1
        current_str = ''.join(combination) + '\0'
  
        self.passAttemptTxt.text = f'{current_str}'
        self.ElapsedTimeTxt.text = f'Elapsed time: {current_time - clockStart:.4f} seconds'
        self.TotalCombinationsTxt.text = f'Total combinations Run: {counter}'
  
        if current_str == password:
          end_time = time.time()
          elapsed_time = end_time - clockStart
          self.passAttemptTxt.text = f'{current_str}'
          self.ElapsedTimeTxt.text = f'Elapsed time: {elapsed_time:.4f} seconds'
          self.TotalCombinationsTxt.text = f'Total combinations Run: {counter}'
          self.passAttemptTxt.foreground = '#90EE90' #light green
          self.configReset()
          alert(title = "Password found!")
          return
    return

  # When current string is equal, ready for the next default configuration
  def configReset(self):
    self.StopCode = True
    self.stopBtn.visible = False
    self.btnBruteforce.visible = True
    self.btnDictionary.visible = True
    self.timer_Bruteforce.interval = 0.00
    self.delayTxt.enabled = True
    self.passAttemptTxt.enabled = True
    self.lowercaseCB.enabled = True
    self.uppercaseCB.enabled = True
    self.numbercaseCB.enabled = True
    self.specialcaseCB.enabled =True
    pass

  # to automatically enter the bruteforce attack when user entered the enter key in the textbox
  def passwordTxt_pressed_enter(self, **event_args):
    self.btnDictionary_click()
    pass

  # Force stopping the process
  def stopBtn_click(self, **event_args):
    self.StopCode = True
    self.stopBtn.visible = False
    self.btnBruteforce.visible = True
    self.btnDictionary.visible = True
    self.configReset()
    return

  # Time delay component checker
  def delayTxt_change(self, **event_args):
    try:
      if self.delayTxt.text is None:
        self.delayTxt.text = 0.01

      else:
        if self.delayTxt.text is not None:
          delay = float(self.delayTxt.text)
          if delay < 0.01:
            self.warningLabel.visible = True
            Notification("Warning: Low Time Delay can cause lagging")
          else:
            self.warningLabel.visible = False
    except ValueError:
      self.warningLabel.visible = True
      Notification("Invalid input: Please enter a valid number")
       
    pass


  def btnDictionary_click(self, **event_args):
    self.timer_Dictionary.interval = 0.00000000000000001
   
    pass

  def retrievedDictionary(self):
    retrieveList = app_tables.tbldictionarylist.search(tables.order_by('dictionaryPasswords', ascending= True))
    storeList = [row['dictionaryPasswords'] for row in retrieveList]

    return storeList



  def evaluatePass(self):
    searchSpace = len(self.validateRange())
    characters = len(self.passwordTxt.text)
    calculations =  searchSpace ** characters
    displayCalculations = str(calculations)
   
    self.rtCombinations.content = '• In bruteforcing this, it would take a maximum combination/attempts of: {:,}'.format(int(displayCalculations))

    safe = 0

    if characters >= 16:
      safe = 4
    elif characters  >= 10:
      safe = 3
    elif characters  >= 6:
      safe = 2
    elif characters  >= 1:
      safe = 1
    
    if safe == 4:
      self.greenBox.background = '#c5fd81'
      self.yelloBox.background = '#FFEB99'
      self.orangeBox.background = '#FF8C66'
      self.label_1.text = 'Password Evaluation: Strong'
    elif safe == 3:
      self.greenBox.background = ''
      self.yelloBox.background = '#FFEB99'
      self.orangeBox.background = '#FF8C66'
      self.label_1.text = 'Password Evaluation: Fair'
    elif safe == 2:
      self.greenBox.background = ''
      self.yelloBox.background = ''
      self.orangeBox.background = '#FF8C66'
      self.label_1.text = 'Password Evaluation: Weak'
    elif safe == 1:
      self.greenBox.background = ''
      self.yelloBox.background = ''
      self.orangeBox.background = ''
      self.label_1.text = 'Password Evaluation: Very Weak'

  def passwordTxt_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    password = self.passwordTxt.text
    
    if ' ' in password:
      password = password.replace(' ', '')
      self.passwordTxt.text = password

  def timer_Dictionary_tick(self, **event_args):
    searchSpace = self.validateRange()
    stopProcess = False

    if searchSpace == '' or searchSpace is None or len(searchSpace) <= 0:
      self.timer_Dictionary.interval = 0.00
      Notification("Invalid Input: \n\nPlease enter a character and tick at least 1 bruteforce range.").show()
      return
    else:
      scanList = self.passwordTxt.text.strip()
      if scanList is None or scanList == '' or scanList == '\0' or not scanList:
        Notification("Invalid Input: Please enter a character.").show()
        self.timer_Dictionary.interval = 0.00
        self.cardDisplay.visible = False
        return
      else:
        delay = self.delayValidation()
  
        if not delay:
          self.containerConfiguration()
          
          self.cardDisplay.visible = True
          self.ElapsedTimeTxt.visible = True
          self.TotalCombinationsTxt.visible = True
          self.stringLabel.text = 'Mode: Dictionary Attack'
          self.stringLabel.foreground = '#FFFFB3'
          
          dictionaryList = self.retrievedDictionary()
          self.cardEvaluation.visible = True
          self.evaluatePass()
          
          try:
            delay = float(self.delayTxt.text)
          except ValueError:
            delay = 0.01
      
          found_passwords = []
          matchFound = False
          counter = 0
          clockStart = time.time()
          
          for password in dictionaryList:
            if self.StopCode:
              stopProcess = True
              break
            counter += 1
            time.sleep(delay)
            currentPassword = password.strip()
            self.passAttemptTxt.text = currentPassword.strip()
            current_time = time.time()
            self.ElapsedTimeTxt.text = f'Elapsed time: {current_time - clockStart:.4f} seconds'
            self.TotalCombinationsTxt.text = f'Total combinations Run: {counter}'
  
            if currentPassword == scanList:
              found_passwords.append(currentPassword)
              self.passAttemptTxt.foreground = '#90EE90'
              self.ElapsedTimeTxt.text = f'Elapsed time: {current_time - clockStart:.4f} seconds'
              self.TotalCombinationsTxt.text = f'Total combinations Run: {counter}'
              matchFound = True
              self.configReset()
              self.greenBox.background = ''
              self.yelloBox.background = ''
              self.orangeBox.background = ''
              self.label_1.text = 'Password Evaluation: Very Weak (Leaked in Dictionary)'
              alert(title = "Weak Password",
                content = "Password found in Dictionary list: {}".format(currentPassword) + '\n\nPlease create a strong and unique password.')
              break

          if not stopProcess:
            if not matchFound:
              self.passAttemptTxt.foreground = '#FF6666'
              if confirm('No Passwords Matched in the Dictionary. The password is safe from the current Dictionary List.\n\nWould you like to try the Bruteforce Attack?'):
                self.btnBruteforce_click()
              else:
                self.configReset()
                
      self.timer_Dictionary.interval = 0.00
      self.stopCode = True
    pass


        

      
      
    
    

    
    