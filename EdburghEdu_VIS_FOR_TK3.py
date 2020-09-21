'''p3_Array_VIS_FOR_TK.py
Version of Aug. 29, 2018. Works with the formulation of
Missionaries and Cannibals that uses a State class for
representing states.

'''

#from show_state_array import initialize_tk, state_array, state_display, STATE_WINDOW, test

from tkinter import font
import math

myFont=None


WIDTH = 700
HEIGHT = 200
TITLE = 'Edburg Education'

gridW = 21 #number of grids in one row
gridH = 9

STATE_WINDOW = None
STATE_ARRAY = None

def initialize_vis(st_win, state_arr, initial_state):
  global STATE_WINDOW, STATE_ARRAY
  STATE_WINDOW = st_win
  STATE_ARRAY = state_arr
  STATE_WINDOW.winfo_toplevel().title(TITLE)
  render_state(initial_state)
  
def render_state(s):

    # Note that font creation is only allowed after the Tk root has been
    # defined.  So we check here if the font creation is still needed,
    # and we do it (the first time this method is called).
    global myFont
    if not myFont:
      myFont = font.Font(family="Helvetica", size=12, weight="bold")
    print("In render_state, state is "+str(s))
    # Create the default array of colors
    Grey = (50,50,50)
    B =   (255,247,123) #yello
    Mi =  (184,219,175) #green
    Ma =  (201,240,227) #cyan
    Er =  (160,192,219) #blue
    Tq =  (176,189,245) #periwinkle
    Ps =  (161,157,204) #lavender
    Ii =  (216,205,250) #purple
    Disp = (200,100,80) #red
    Avg = (150,220,150)
    Q = (100,100,100)
    Cr =  (156,6,6)     #dark red
    
    row = [Grey]*gridW
    the_color_array = [row]
    for i in range(gridH):
      the_color_array.append(row[:])
    # Now create the default array of string labels.
    row = ['' for i in range(gridW)]
    the_string_array = [row]
    for i in range(gridH):
      the_string_array.append(row[:])

    #custom functions
    def write(text,line,bg=None):
      start = (gridW-len(text))//2
      for i in range(len(text)):
        the_string_array[line-1][start+i]=text[i]
        if bg !=None:
          the_color_array[line-1][start+i]=bg

    # Adjust colors and strings to match the state.

    bars_list = [['B',B,s.budget//50],
                 ['Mi',Mi,s.avg_grade_mi//5],
                 ['Ma',Ma,s.avg_grade_ma//5],
                 ['Er',Er,s.enroll_rate//5],
                 ['Tq',Tq,s.teacher_qual//5],
                 ['Ps',Ps,s.parent_satis//5],
                 ['Ii',Ii,s.infra_integ//5]
                 ]

    avg = (s.avg_grade_mi + s.avg_grade_ma*2)//15
    disp = int((s.avg_grade_ma-s.avg_grade_mi)//min([10, s.enroll_rate*(1/2)]))
    q=s.quarter

    if q==0:
      write('Edburgh Education',4)
    elif s.is_goal():
      write('THE END',4)
    elif s.crisis != None:
      write(s.crisis.title, 6)
      write('CRISIS!',4,Cr)
    else:
      for j in range(len(bars_list)):
        item = bars_list[j][0]
        value = bars_list[j][2]
        color = bars_list[j][1]
        if value > gridW-1: value = gridW-1
        if value <0: value = 0
        if value < 3: color = Cr
        for i in range(value):
          the_color_array[j][i]=color
        the_string_array[j][i+1]=item

      for i in range(avg):
        the_color_array[8][i]=Avg
      for i in range(disp):
        the_color_array[8][avg-1-i]=Disp
        
    #quarter bar
    for i in range(1,q):
      the_color_array[9][i]=Q
      the_string_array[9][i]=str(i)
    the_string_array[9][0]='Q'
      


    caption="Current state of the puzzle. Textual version: "+str(s)        
    the_state_array = STATE_ARRAY(color_array=the_color_array,
                                  string_array=the_string_array,
                                  text_font=myFont,
                                  caption=caption)
    #print("the_state_array is: "+str(the_state_array))
    the_state_array.show()

    
