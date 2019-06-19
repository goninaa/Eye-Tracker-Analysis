import pandas as pd
import attr
from attr.validators import instance_of

# @attr.s
# class ProcessData:
#     fixations = attr.ib(validator=instance_of(EyeFile)) 
#     events = attr.ib(validator=instance_of(EyeFile)) 
        
#     def read_file (self):
#         pd.read_csv(fname)

class ProcessData:
    """ Pipeline to process twin Data instances """
    def __init__(self, files: EyeFile):
        self.files = datacont
        self.fixations = pd.read_csv(self._fname_eyes)
        self.result = {}
        self.metadata = datacont.metadata
        
    def process(self):
        """ Mock processing pipeline """
        self.result['sum'] = self.datacont.sum()
        means = [x.mean() for x in self.datacont.data]
        self.result['mean'] = means
        return self.result
