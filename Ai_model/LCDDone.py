print ("DOne  ...............")
from RPLCD import CharLCD
import time
from RPLCD import CursorMode
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

lcd.cursor_pos = (1, 3) 
lcd.cursor_mode = CursorMode.line


lcd.clear()
lcd.write_string(u"DONE!!")
time.sleep(2000)
lcd.clear()
