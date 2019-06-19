from pathlib import Path
import attr
from attr.validators import instance_of

@attr.s(frozen=True)
class EyeFile:
    """File objects with path attribute and several metadata attributes.
    Instantiated by the ProcessFilelist class, passed to the ProcessData class
    Attributes: path, fname, experiment, id_num, design, design, data_type.
    """
    path = attr.ib(validator=instance_of(Path))
    fname = attr.ib(validator=instance_of(str))
    experiment = attr.ib(validator=instance_of(str))
    id_num = attr.ib(validator=instance_of(str))
    design = attr.ib(validator=instance_of(str))
    data_type = attr.ib(validator=instance_of(str))

#########################################################################
folder = Path('CSV/FB') # get folder or filelist from GUI.
filelist = [file for file in folder.glob('*.csv')] # don't process sub-folders
# filelist = [file for file in folder.rglob('*.csv')] # process sub-folder
#########################################################################

@attr.s
class ProcessFilelist:
    """Processes a list of file.
    Reads attributes from filename and creates a list of EyeFile objects to pass.
    Attributes: filelist, invalid_files, eyelist.
    Methods: instantiate_eye_file, validate_fname.
    """
    filelist = attr.ib(validator=instance_of(list))
    invalid_files = [] ### add invalid files output ###
    eyelist = {} # nested dict of EyeFile instances to pass forward

    def instantiate_eye_file(self):
        """Analizes file attributes and instantiate EyeFile objects."""
        for eyefile in self.filelist:
            path = Path(eyefile)
            fname = path.name
            
            fattrs = fname.split('_')
            try:
                experiment, id_num, design, data_type = fattrs[0], fattrs[3], fattrs[5], fattrs[9]
            except ValueError:
                self.invalid_files.append(fname)
                continue
            
            if 'fix' in data_type:
                data_type = 'fixations'
            elif 'message' in data_type:
                data_type = 'events'
            else:
                self.invalid_files.append(fname)
                continue
            
            eyeitem = EyeFile(path, subj_id, design, data_type)
            try:
                self.eyelist[f'{id_num}_{design}'][data_type] = eyeitem
            except KeyError:
                self.eyelist[f'{id_num}_{design}'] = {data_type: eyeitem}


# if __name__ == "__main__":
#     fix = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_fixations.csv')
#     event = Path('CSV/FB/FB_integration_ID_01_design_1_time_04.11.18_11.43_messages.csv')
#     fix_obj = EyeFile(path=fix, fname=fix.name, id_num='01', design='1', data_type='fixations')
#     event_obj = EyeFile(path=event, fname=fix.name, id_num='01', design='1', data_type='events')