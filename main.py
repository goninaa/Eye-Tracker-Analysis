from read_data import *
from visualization import *
from process_GUI_input import *
from eye_GUI import *

# yossi

# f.eyedict
for key, value in f.eyedict:
    data = IdData(key, value)
    data.run()



