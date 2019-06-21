from pathlib import Path
import attr
from attr.validators import instance_of
from typing import Union

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

@attr.s
class ProcessFilelist:
    """Processes a list of file.
    Reads attributes from filename and creates a list of EyeFile objects to pass.
    Attributes: filelist, invalid_files, eyedict.
    Methods: instantiate_eye_file, assert_csv, extract_file_attrs.
    """
    filelist = attr.ib(validator=instance_of(list))
    invalid_files = [] ### should add invalid files output ###
    eyedict = {} # nested dict of EyeFile instances to pass forward

    def get_file_attrs(self) -> None:
        """analizes file attributes and instantiate EyeFile objects"""
        for eyefile in self.filelist:
            path = Path(eyefile)
            fname = path.name
            if not self.assert_csv(path): # accepts only .csv files
                self.invalid_files.append(fname)
                continue
            
            fattrs = self.extract_file_attrs(fname)
            if not fattrs: # accepts files only if named in the appropriate pattern
                self.invalid_files.append(fname)
                continue
            experiment, id_num, design, data_type = fattrs[0], fattrs[3], fattrs[5], fattrs[9]
            
            if 'fix' in data_type:
                data_type = 'fixations'
            elif 'message' in data_type:
                data_type = 'events'
            else: # accepts only fixations or messages files
                self.invalid_files.append(fname)
                continue
            self.instantiate_eye_file(path, fname, experiment, id_num, design, data_type)
    
    def assert_csv(self, path: Path) -> bool:
        """asserts that a file is a csv file"""
        return str.lower(path.suffix) == '.csv'
    
    def extract_file_attrs(self, fname: str) -> Union[list, bool]:
        """if the file named appropriately, extracts its attributes from filename"""
        fattrs = fname.split('_')
        if len(fattrs) < 9:
            return False
        else:
            return fattrs
    
    def instantiate_eye_file(self, path: Path, fname: str, experiment: str, id_num: str, design: str, data_type: str) -> EyeFile:
        """instantiate EyeFile objects"""
        eyeitem = EyeFile(path=path, fname=fname, experiment=experiment, id_num=id_num, design=design, data_type=data_type)
        try:
            self.eyedict[f'{id_num}_{design}'][data_type] = eyeitem
        except KeyError:
            self.eyedict[f'{id_num}_{design}'] = {data_type: eyeitem}

if __name__ == "__main__":
    files = ProcessFilelist(filelist)
    files.get_file_attrs()
    print(files.eyedict)
    print(files.invalid_files)