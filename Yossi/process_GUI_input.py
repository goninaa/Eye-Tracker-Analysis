from pathlib import Path
import attr
from attr.validators import instance_of

@attr.s
class EyeFile:
    path = attr.ib(validator=instance_of(Path)) # works?
    fname = attr.ib(validator=instance_of(str))
    x = attr.ib()
    y = attr.ib()
    z = attr.ib()

folder = Path() # will be from GUI
filelist = [] 

@attr.s
class ProcessFilelist:
    filelist = attr.ib(validator=instance_of(list))

    def InstantiateEyeFile(self):
        eyelist = [] # list of EyeFile instances to pass forward
        for eyefile in filelist:
            path = Path(eyefile)
            fname = path.name
            fattrs = fname.split('_')
            id_num, design, data_type = fattrs[3], fattrs[5], fattrs[9]
            # break name and filetype
            eyelist.append(EyeFile(path, subj_id, design, data_type))