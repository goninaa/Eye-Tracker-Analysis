from pathlib import Path
import PySimpleGUI as sg
import attr
import platform

@attr.s
class eye_GUI:
    """Main GUI for Eye Tracker Analysis.
    Recieves from user files/folder, reference images, screen resolution and fixation point.
    Attributes: filelist, ref_images, screen_res, fix_point, values.
    Methods: get_user_input, get_filelist, get_ref_images, get_screen_res, get_fix_point.
    """
    filelist = []
    ref_images = {}
    screen_res = ()
    fix_point = ()

    def get_user_input(self) -> bool:
        """GUI func to get input from GUI"""
        layout = [
            [sg.Text('Select files or a folder to analyze')],
            [sg.Text('Files', size=(8, 1)) ,sg.Input(), sg.FilesBrowse(file_types=(("CSV Files", "*.csv"),)) if platform.system() == 'Windows' else sg.FilesBrowse()],
            [sg.Text('OR Folder', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
            [sg.Text('Select sample images for all experimental conditions')],
            [sg.Text('Images', size=(8,1)), sg.Input(), sg.FilesBrowse(file_types=(("PNG Files", "*.png"),)) if platform.system() == 'Windows' else sg.FilesBrowse()],
            [sg.Text('Screen resolution'), sg.Input(default_text='1920', size=(6,1)), sg.Text('*'), sg.Input(default_text='1080', size=(6,1)), 
                sg.Text('Fixation point'), sg.Input(default_text='960', size=(6,1)), sg.Text('*'), sg.Input(default_text='237', size=(6,1))],
            [sg.OK(size=(7,1)), sg.Cancel(size=(7,1))]
        ]

        window = sg.Window('Eye Tracker Analysis', layout)
        self.event, self.values = window.Read()
        window.Close()
        return True if self.event == 'OK' else False
    
    def get_filelist(self) -> None:
        """Extract filelist from GUI"""
        if self.values[0]:
            self.filelist = self.values[0].split(';')
        elif self.values[1]:
            folder = Path(self.values[1])
            self.filelist = [file for file in folder.glob('*.csv')]
        else:
            raise Exception('Folder/files not found')

    def get_ref_images(self) -> None:
        """Creates dict of reference images"""
        ref_images = self.values[2].split(';')
        image_cond = []
        for img in ref_images:
            i = img.split('_')
            i = i[len(i)-1].split('.')
            image_cond.append(i[0])
        self.ref_images = dict(zip(image_cond, ref_images))
    
    def get_screen_res(self) -> None:
        """Extract screen resolution from GUI"""
        self.screen_res = (self.values[3], self.values[4])

    def get_fix_point(self) -> None:
        """Extract fixation point from GUI"""
        self.fix_point = (self.values[5], self.values[6]) 
    
    def run(self) -> bool:
        """Main function to run the GUI"""
        if not self.get_user_input():
            return False
        self.get_filelist()
        self.get_ref_images()
        self.get_screen_res()
        self.get_fix_point()
        return True

if __name__ == "__main__":
    user_input=eye_GUI()
    assert user_input.run()
    print(user_input.ref_images)

