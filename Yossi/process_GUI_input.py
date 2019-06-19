from pathlib import Path
import attr
from attr.validators import instance_of

@attr.s
class EyeFile:
    path = attr.ib(validator=instance_of(Path))
    fname = attr.ib(validator=instance_of(str))
    experiment = attr.ib(validator=instance_of(str))
    id_num = attr.ib(validator=instance_of(str))
    design = attr.ib(validator=instance_of(str))
    data_type = attr.ib(validator=instance_of(str))

folder = Path('CSV/FB') # get folder from GUI.
filelist = [file for file in a.glob('*.csv')] # don't process sub-folders
filelist = [file for file in a.rglob('*.csv')] # process sub-folder

@attr.s
class ProcessFilelist:
    filelist = attr.ib(validator=instance_of(list))
    invalid_files = []

    def instantiate_eye_file(self):
        eyelist = [] # list of EyeFile instances to pass forward
        for eyefile in filelist:
            path = Path(eyefile)
            fname = path.name
            fattrs = fname.split('_')
            if self.validate_fname(fattrs):
                experiment, id_num, design, data_type = fattrs[0], fattrs[3], fattrs[5], fattrs[9]
                if 'fix' in data_type:
                    data_type = 'fixations'
                elif 'message' in data_type:
                    data_type = 'events'
                else:
                    invalid_files.append(fname)
                    continue
                eyelist.append(EyeFile(path, subj_id, design, data_type))

    def validate_fname(self, fname):
        """validates all elements in filename. Adds to invalid files if not"""
        if False: # check elements
            invalid_files.append(fname)
            return False
        return True