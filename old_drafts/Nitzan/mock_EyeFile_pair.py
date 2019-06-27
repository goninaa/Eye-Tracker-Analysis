import pandas as pd
from pathlib import Path
import attr
from attr.validators import instance_of

@attr.s
class EyeFile:
    path = attr.ib(validator=instance_of(Path))
    fname = attr.ib(validator=instance_of(str))
    id_num = attr.ib()
    design = attr.ib()
    data_type = attr.ib()

fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
event_obj = EyeFile(path=event, fname=fix.name, id_num='01', design='1', data_type='events')
