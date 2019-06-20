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

#########################################################
# manual data, would be replaced by the GUI             #
folder = Path('CSV/FB')                                 #
filelist = [file for file in folder.glob('*.csv')]      #
ref_images = [  Path('FB_on_full_screen_Body.jpg'),     #
                Path('FB_on_full_screen_Face.jpg'),     #
                Path('FB_on_full_screen_Person.jpg')]   #
resolution = 1080*1920                                  #
fix_point = (960, 237)                                  #
#########################################################

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
            eyeitem = EyeFile(path=path, fname=fname, experiment=experiment, id_num=id_num, design=design, data_type=data_type)
            try:
                self.eyelist[f'{id_num}_{design}'][data_type] = eyeitem
            except KeyError:
                self.eyelist[f'{id_num}_{design}'] = {data_type: eyeitem}


if __name__ == "__main__":
    files = ProcessFilelist(filelist)
    files.instantiate_eye_file()
    print(files.eyelist)