'''EdburghEducation.py
("Education Wicked Problem: Disparities" problem)
A SOLUZION problem formulation.
The XML-like tags used here may not be necessary, in the end.
But for now, they serve to identify key sections of this 
problem formulation.  It is important that COMMON_CODE come
before all the other sections (except METADATA), including COMMON_DATA.
'''
#<METADATA>
SOLUZION_VERSION = "0.2"
PROBLEM_NAME = "Edburgh Education"
PROBLEM_VERSION = "0.9"
PROBLEM_AUTHORS = ['A. Arends','A. Bhamidi','A. Singh','L. Tran','L. Yan','S. Tanimoto']
PROBLEM_CREATION_DATE = "10-SEP-2020"
PROBLEM_DESC=\
'''Much of this code was adapted from OnePlayerTicTacToe.py, which itself was an adaptation
created by A. Arends and A. Bhamidi, of Missionaries,py, provided by S. Tanimoto.
As such, said latter individual is listed as an author for this program. If any commented-out
code seems extraneous or irrelevant, it is likely leftover from one of these two
previous files.

This program was made to simulate the struggles of dealing with disparities in education
while balancing other aspects, as an administrator of a school district.
A copy of the output instructions are provided here:
You are the administrator of a school district in Edburgh City.
As administrator, you are responsible for the academic success and future prospects of Edburgh’s students. Your goal is to fix
the issues of educational disparity in the schools within your jurisdiction, which suffer greatly from de facto segregation.
Student success is measured by grades. In your attempts to lessen disparity, you must balance several factors alongside budget,
enrollment rate, teacher qualification, parent satisfaction, and infrastructure integrity. If any of them drop to 0 or below,
you have failed. After each school year, your district is faced with a new crisis. You must choose what to do from the available
courses of action. 
You have five years (20 quarters) to either fix your school district or ruin it. Remember, your career as district administrator
hangs in the balance. Good luck!

'''

#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>

class State:
  def __init__(self, old=None):
    # Default new state is a state objects initialized as the
    # initial state.
    # If called with old equal to a non-empty state, then
    # the new instance is made to be a copy of that state.
    self.budget = -1
    self.avg_grade_mi = 30
    self.avg_grade_ma = 30
    self.enroll_rate = 30
    self.teacher_qual = 30
    self.parent_satis = 30
    self.infra_integ = 30
    self.quarter = 0
    self.crisis = crises[0]
    self.used_lims = [] #Contains used limited-use operator IDs
    if not old is None:
      self.budget = old.budget
      self.avg_grade_mi = old.avg_grade_mi
      self.avg_grade_ma = old.avg_grade_ma
      self.enroll_rate = old.enroll_rate
      self.teacher_qual = old.teacher_qual
      self.parent_satis = old.parent_satis
      self.infra_integ = old.infra_integ
      self.quarter = old.quarter
      self.crisis = old.crisis
      self.used_lims = old.used_lims[:]
      

  def can_act(self,b,agmi,agma,er,tq,ps,ii,szn=None,n_op=None,use_lim=None,when=4):
    # Tests whether it's legal to act

    # The game detects if it should be a 'choose city' time by the fact that no b increments
    # will be 800 or higher, and that during this time there is a special value for budget
    if self.budget == -1 and b >= 400:
      return True
    if self.budget == -1 and b <= 400:
      return False
    # This is the opposite of the above, disabling the choose city operators
    if self.budget != -1 and b >= 400:
      return False

    if szn != None:
      if self.quarter % 4 != szn:   # 1 means fall, 2 - winter, 3 - spring, 0 - summer
        return False
    
    if self.crisis != None:
      for fx in self.crisis.fx:
        if eval(fx)>0:            # The operator is valid if it increases this variable
          return True
      return False

    if use_lim != None:
      if self.used_lims.count(n_op) >= use_lim:
        return False           # This checks if an operator has been used its maximum number of times

    if self.quarter < 4:
      if when > self.quarter:
        return False            # The operators procedurally unlock to avoid overwhelming players early on
    
    return True
    

  def act(self,b,agmi,agma,er,tq,ps,ii,n_op,use_lim=None):
    # If it's legal to do the action, this makes a new state with
    # the new values of the variables
    new_state = State(old=self) # Make a copy of the current state.

    # This sets the defaults for choosing a city, since budget is a special value initially
    if self.budget == -1:
      new_state.budget = b
      new_state.avg_grade_mi = agmi
      new_state.avg_grade_ma = agma
      new_state.enroll_rate = er
      new_state.teacher_qual = tq
      new_state.parent_satis = ps
      new_state.infra_integ = ii
      new_state.quarter = 1
      new_state.flav_txt = flav_txts[n_op]
      return new_state

    # This is the incrementer for all non-'choose a city' operators

    new_state.quarter += 1

    # If this is a winter quarter that isn't the first one, introduce a crisis
    if new_state.quarter % 4 == 2 and new_state.quarter != 2:
      new_state.crisis = crises[int(new_state.quarter // 4)]

      inc = new_state.crisis.values[:]
      b += inc[0]
      agmi += inc[1] 
      agma += inc[2]
      er += inc[3]
      tq += inc[4]
      ps += inc[5]
      ii += inc[6]
    else: new_state.crisis = crises[0]

    new_state.flav_txt = flav_txts[n_op]

    # Increments for the new state
    new_state.budget += b
    # These variables cannot go above 100, so...
    new_state.avg_grade_mi = min([new_state.avg_grade_mi + agmi//3, 100])
    new_state.avg_grade_ma = min([new_state.avg_grade_ma + agma//3, 100])
    new_state.enroll_rate = min([new_state.enroll_rate + er, 100])
    new_state.teacher_qual = min([new_state.teacher_qual + tq, 100])
    new_state.parent_satis = min([new_state.parent_satis + ps, 100])
    new_state.infra_integ = min([new_state.infra_integ + ii, 100])

    # If there's a use limit for this operator, note the use
    if use_lim != None:
      new_state.used_lims.append(n_op)


    return new_state

  def is_goal(self):
    # The goal isn't the first turn, of course
    if self.budget == -1: return False

    # There are 3 general possible goal states, as follows:
    
    #1: If something drops to or below 0, the player has failed. This isn't really a 'goal' in a human sense,
    #but for problem-solving, it counts, as it ends the game
    if (self.budget <= 0 or self.avg_grade_mi <= 0 or self.avg_grade_ma <= 0 or\
            self.enroll_rate <= 0 or self.teacher_qual <= 0 or self.parent_satis <= 0 or\
            self.infra_integ <= 0):
      return True

    #2: Next, if the player gets everything where sufficiently high, they have succeeded
    if (self.budget > 0 and self.avg_grade_mi >= 75 and self.avg_grade_ma >= 75 and\
            self.enroll_rate >= 75 and self.teacher_qual >= 75 and self.parent_satis >= 75 and\
            self.infra_integ >= 75):
      return True

    #3: End of 5-year term, at Quarter 20, with neither other state having been reached
    return (self.quarter > 20)
  

  def __eq__(self, s2):
    if s2==None: return False
    if self.budget != s2.budget: return False
    if self.avg_grade_mi != s2.avg_grade_mi: return False
    if self.avg_grade_ma != s2.avg_grade_ma: return False
    if self.enroll_rate != s2.enroll_rate: return False
    if self.teacher_qual != s2.teacher_qual: return False
    if self.parent_satis != s2.parent_satis: return False
    if self.infra_integ != s2.infra_integ: return False
    if self.quarter != s2.quarter: return False
    return True

  def __str__(self):
    
    # Output for 'choose city' initial state
    if self.budget == -1: return """Instructions:
You are the administrator of a school district in Edburgh City.
As administrator, you are responsible for the academic success and future prospects of Edburgh’s students. Your goal is to alleviate
the issues of educational disparity in the schools within your jurisdiction, which suffer greatly from de facto segregation.
Student success is measured by grades. In your attempts to lessen disparity, you must balance several factors alongside budget,
enrollment rate, teacher qualification, parent satisfaction, and infrastructure integrity. If any of them drop to 0 or below,
you have failed. After each school year, your district is faced with a new crisis. You must choose what to do from the available
courses of action. 
\nYou have five years (20 quarters) to either fix your school district or ruin it. Remember, your career as district administrator
hangs in the balance. Good luck!
Choose a city and district. The options just so happen to both be called "Edburgh".
(if this is your first try at this game, the high-income option is suggested, as it is slightly easier):"""

    # Output for non-'choose city' states
    
    st = ''
    st += '\n'+self.flav_txt+'\n'

    if self.quarter%4==1:
      st += 'Welcome to a new school year at Edburgh.'


    #The stats will still show, even if it is a goal state

    #To prevent division by 0
    if self.enroll_rate <= 10:
      disp_display = 'A Lot'
    else:
      disp_display = str((self.avg_grade_ma-self.avg_grade_mi)*10//(self.enroll_rate**0.5))
        
    st +='\nBelow are the stastistics of your district. Pick one of the listed operators to take action.'+\
         '\nBudget: '+str(self.budget)+'\nAverage Grade of Minority Groups: '+str(self.avg_grade_mi)+\
         '\nAverage Grade of Majority Groups: '+str(self.avg_grade_ma)+'\nAverage Grade Overall: '+\
         str((self.avg_grade_mi+(self.avg_grade_ma*2))//3)+' --- Enrollment Rate: '+str(self.enroll_rate)+\
         ' --- Disparity: '+disp_display+'\nTeacher Qualification: '+str(self.teacher_qual)+\
         ' --- Parent Satisfaction: '+str(self.parent_satis)+' --- Infrastructure Integrity: '+\
         str(self.infra_integ)+'\nQuarter: '+str(self.quarter)+'\n'

    if self.crisis != None:
      st += '\n'+self.crisis.name+'\n'
    
    # If the state is a goal, output the appropriate goal message
    # Note that it uses 21 and not 20, because the quarter increments before the goal state is checked, and
    # we want the player to get one of the two main endings before it defaults to the third
    if self.is_goal():
      if (self.budget <= 0 or self.avg_grade_mi <= 0 or self.avg_grade_ma <= 0 or\
            self.enroll_rate <= 0 or self.teacher_qual <= 0 or self.parent_satis <= 0 or\
            self.infra_integ <= 0) and self.quarter <= 21:
        st += '''\nWhether through mistakes, inaction, or incompetence,\n you allowed the state of the district
to deteriorate beyond reason. Within the week, you are swiftly removed from office, every other citizen
near-unanimously decrying your name. Let us hope that your replacement can fix the damage you caused.'''
      elif (self.budget > 0 and self.avg_grade_mi >= 85 and self.avg_grade_ma >= 85 and\
            self.enroll_rate >= 85 and self.teacher_qual >= 85 and self.parent_satis >= 85 and\
            self.infra_integ >= 85) and self.quarter <= 21:
        st += '''\nThe skill you brought to the office, or maybe your sheer luck in random choices, has made
the district better than it ever has been before. Though the laws state that you cannot serve two terms in
a row, you have been assured left and right that, should you ever choose to run in another election, you
will have no trouble winning. Here's hoping your successor keeps the success you brought about.'''
      else:
        st += '''\nYour time in office came and went in a flash. While you certainly made changes, nothing
noteworthy came about from them. Perhaps you will be re-elected in the election after the next one, perhaps
not. It remains to be seen how your successor will perform.'''
      st += '''\nYou have reached an end state, and thus the game is done. To learn more about the issue of
educational disparity and inequality in the real world, please peruse the following links at your leisure
(all are functional as of 9-17-2020):
https://soeonline.american.edu/blog/reducing-inequality-in-the-us-education-system
https://uei.uchicago.edu/sites/default/files/documents/UEI%202017%20New%20Knowledge%20-%20Addressing%20Educational%20Inequality.pdf
https://www.oecd.org/education/school/39989494.pdf'''
      st += '''\n(Be aware that the programming of this game is not equipped to handle a player continuing
to explore past Quarter 20. Proceed at your own risk.)'''

    return st

  def __hash__(self):
    return (str(self)).__hash__()
    

def copy_state(s):
  return State(old=s)

class Crisis:
  def __init__(self, title, fx, values, name):
    self.name = name
    self.fx = fx
    self.values = values
    self.title = title

#b,agmi,agma,er,tq,ps,ii
crises = [None,
          Crisis('Dropout Surge',['er'],[-50,-20,-10,-40,0,0,0],\
                 '''Dropout rates have reached a record high since 2000!
Students struggling with poor mental health feel discouraged and incapable of attending school and succeeding.
The poor state of the economy has left many students from low-income households forced to work during school hours to help
support their families.'''),
          Crisis('Teacher Strike',['agmi','agma'],[-100,-10,-10,0,-35,0,0],\
                 '''A large majority of teachers in Edburgh join a teachers union.
Exasperated at the school administration’s refusal of their demands for higher wages, the union members go on strike,
refusing to come to work! After a week-long strike, the district finally reconsiders their stance and the teachers
return to work. Your administration has had to pay for substitute teachers for the week, as well as for the hike in
teacher salaries. Students have suffered due to the interruption in their learning.'''),
          Crisis('Inspection Fail',['ps','ii'],[-125,0,0,0,0,-20,-30],\
                 '''Edburgh School’s infrastructure quality fails state inspection!
The state inspector exclaimed, "The playground equipment is borderline life-threatening to the children, and the
support columns are withering away from water damage." The district must pay a fine and close the school for 2 days to make
immediate repairs. Angry parents flood the district email with complaints, upset that their children have been unknowingly
attending school in these terrible conditions.'''),
          Crisis('Hurricane',['b'],[-200,-20,-10,-40,-10,-10,-50],\
                 '''Oh no! A hurricane has badly damaged the town of Edburgh.
Many homes have been destroyed, and a majority of the schools were hit hard as well. Many students from low income areas
are left without homes and struggle to find somewhere to live. Every Edburgh resident is suffering.''')
          ]

flav_txts = ['You have chosen the low-income city of Edburgh.',
             'You have chosen the high-income city of Edburgh.',
             '''Fundraising events increase the budget. However, they force teachers to take time out of their busy schedules.
There are also additional setup and clean-up costs.''',
             '''Teachers and parents have to invest a lot of time in lobbying efforts, which are slow and laborious.
However, they will later benefit from their efforts.''',
             '''The extra charges recover school funds but result in parent dissatisfaction.
Poorer students are put at a disadvantage.''',
             '''By spending less on maintaining infrastructure, a greater portion of the budget is left available.
Unfortunately, teachers and parents are left unhappy about this decision. Minority students, who depend more on
school facilities for their learning, are also left worse off.''',
             '''Although low income students benefit, rich parents express dissatisfaction that school funds are being spent
on a program that doesn’t benefit their kids. Enrollment rates increase with this added support.''',
             '''Strengthening the links between school and home help parents, especially in disadvantaged communities, help
their children learn. The increased emotional support especially helps disadvantaged students and lowers dropout rates.
Parents are happy with the implementation of this support system, but school resources are further strained.''',
             '''Pre-K programs help students succeed academically at an early age. Although the programs are costly,
increased academic involvement from a young age reduces the likeliness of students to drop out later on.''',
             '''By investing in updated textbooks, all students benefit academically. Disadvantaged kids especially thrive
because they may lack access to resources such as tutors and prep books outside of school. Teacher quality improves because
they have better resources to guide their instruction.''',
             '''By adding computers to the library, students are able to be more productive during school hours. Students
without access to computers at home can now complete schoolwork that requires the internet at school.''',
             '''All students benefit from school-wide wifi because it allows them to access online educational resources for free.
Since they are more likely to have limited or no access to the internet at home, students from minority groups benefit more.
Teachers may also enjoy access to additional teaching aids from the internet.''',
             '''The investment in teacher training greatly improves teaching quality. In turn, improved teaching quality
helps both groups of students academically.''',
             '''The addition of diversity aspects to teacher training benefits kids from different backgrounds especially
since teachers are more understanding and accommodating towards them. Teacher quality improves with this change.''',
             '''By recruiting teachers from diverse backgrounds, students from minority backgrounds feel more comfortable.
Everyone benefits from a more diverse range of perspectives, and parents are happy with this implementation.''',
             '''When teachers spend extra time with low-performing students, it prevents these students from being discouraged.
As a result, the dropout rate decreases. Parents don’t have to spend as much time helping their children with homework.
However, the school has to pay for teachers to work overtime and teachers have to sacrifice their time.
Classrooms and teaching implements are also used more intensively.''',
             '''A more personalized grade report helps engage parents, especially those who don’t usually
have the extra time to invest in their children’s schooling. Enrollment rates increase.
These reports require more effort from teachers, and cost money to produce.''',
             '''The shift to online homework hurts disadvantaged students who do not have good internet access or
computers to work on. Students from the majority group are likely to have easy access to electronic devices/internet,
and homework is easier to grade on an electronic medium, so privileged students and teachers benefit.''',
             '''Disadvantaged schools have the greatest need for experienced teachers, but often struggle with attracting
experienced teachers due to their poor reputation. By offering incentives, more experienced teachers will be motivated to
apply to these roles, and teach where their expertise is needed the most.''',
             '''By spreading awareness of and subsidizing pathways (such as second chance education programs) for dropouts
to earn a high school equivalency, dropout rates decrease, and students understand that there are alternate paths towards
academic certification.''',
             '''Conventional thinking leads to the assumption that providing parents a free choice of where to send their kids
to school would increase equity; however, it leads to the popular schools being overcrowded and potentially not having an
even social mix. Moreover, those who lack access to information are likely to make uninformed choices. By ensuring a social
mix, disparities can be lowered, although parents may not appreciate having their choices restricted.''']

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
INITIAL_STATE = State()
#</INITIAL_STATE>

#<OPERATORS>
#b,agmi,agma,er,tq,ps,ii,szn,n_op,use_lim,when
#b,agmi,agma,er,tq,ps,ii,n_op,use_lim
phi0 = Operator("Choose the low-income city.",
  lambda s: s.can_act(500,20,40,30,30,30,30),
  lambda s: s.act(500,20,40,30,30,30,30,0))

phi1 = Operator("Choose the high-income city.",
  lambda s: s.can_act(700,40,60,40,40,40,40),
  lambda s: s.act(700,40,60,40,40,40,40,1))

phi2 = Operator("Host fundraising events.",
  lambda s: s.can_act(75,0,0,0,-10,0,-10,when=1),
  lambda s: s.act(75,0,0,0,-10,0,-10,2))

phi3 = Operator("Lobby for increased state funding.",
  lambda s: s.can_act(150,0,0,0,-15,-10,0,None,3,3,when=1),
  lambda s: s.act(150,0,0,0,-15,-10,0,3,3))

phi4 = Operator("Increase charge for sports uniforms.",
  lambda s: s.can_act(40,-5,0,0,0,-15,0,1,when=1),
  lambda s: s.act(40,-5,0,0,0,-15,0,4))

phi5 = Operator("Divest from infrastructure maintenance.",
  lambda s: s.can_act(100,-10,0,-5,-5,-5,-30,0,when=1),
  lambda s: s.act(100,-10,0,-5,-5,-5,-30,5))

phi6 = Operator("Introduce an outreach program for minority students.",
  lambda s: s.can_act(-50,20,0,10,0,-10,0,3,6,3,when=1),
  lambda s: s.act(-50,20,0,10,0,-10,0,6,3))

phi7 = Operator("Allow parents increased access to school resources for homework help.",
  lambda s: s.can_act(-30,10,5,5,0,5,0,when=2),
  lambda s: s.act(-30,10,5,5,0,5,0,7))

phi8 = Operator("Invest further in Pre-Kindergarten programs.",
  lambda s: s.can_act(-40,5,5,20,0,0,0,when=2),
  lambda s: s.act(-40,5,5,20,0,0,0,8))

phi9 = Operator("Obtain updated textbooks.",
  lambda s: s.can_act(-75,20,10,0,10,0,5,0,when=2),
  lambda s: s.act(-75,20,10,0,10,0,5,9))

phi10 = Operator("Add computers to libraries.",
  lambda s: s.can_act(-50,20,10,0,0,0,20,None,10,1,when=2),
  lambda s: s.act(-50,20,10,0,0,0,20,10,1))

phi11 = Operator("Offer school-wide free wifi.",
  lambda s: s.can_act(-100,15,5,5,5,0,20,None,11,1,when=2),
  lambda s: s.act(-100,15,5,5,5,0,20,11,1))

phi12 = Operator("Invest in teacher training.",
  lambda s: s.can_act(-50,10,10,0,20,0,0,when=3),
  lambda s: s.act(-50,10,10,0,20,0,0,12))

phi13 = Operator("Add diversity aspects to teacher training.",
  lambda s: s.can_act(-50,20,5,0,10,0,0,when=3),
  lambda s: s.act(-50,20,5,0,10,0,0,13))

phi14 = Operator("Actively recruit more teachers from diverse backgrounds.",
  lambda s: s.can_act(-25,10,5,0,10,10,0,0,when=3),
  lambda s: s.act(-25,10,5,0,10,10,0,14))

phi15 = Operator("Ask teachers to spend extra time helping low-performing students.",
  lambda s: s.can_act(-20,10,5,20,-10,5,-5,when=3),
  lambda s: s.act(-20,10,5,20,-10,5,-5,15))

phi16 = Operator("Introduce a more personalized grade report structure.",
  lambda s: s.can_act(-20,5,5,5,-10,10,0,when=3),
  lambda s: s.act(-20,5,5,5,-10,10,0,16))

phi17 = Operator("Shift all homework to an online platform.",
  lambda s: s.can_act(-50,-10,15,-5,5,-5,15,None,17,1),
  lambda s: s.act(-50,-10,15,-5,5,-5,15,17,1))

phi18 = Operator("Attract qualified teachers from other areas, covering relocation and transport costs.",
  lambda s: s.can_act(-75,15,10,0,0,0,-5),
  lambda s: s.act(-75,15,10,0,0,0,-5,18))

phi19 = Operator("Sponsor the cost of GED tests for students who don't graduate.",
  lambda s: s.can_act(-20,5,0,30,0,5,-10),
  lambda s: s.act(-20,5,0,30,0,5,-10,19))

phi20 = Operator("Limit parents' school choice, using a lottery system for distribution of students into schools.",
  lambda s: s.can_act(20,15,5,5,0,-35,5,None,20,1),
  lambda s: s.act(20,15,5,5,0,-35,5,20,1))
              

OPERATORS = [phi0, phi1, phi2, phi3, phi4, phi5, phi6, phi7, phi8, phi9,\
             phi10, phi11, phi12, phi13, phi14, phi15, phi16, phi17, phi18, phi19, phi20]
#</OPERATORS>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>

#</STATE_VIS>
