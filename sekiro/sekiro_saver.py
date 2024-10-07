import shutil
import os

class SekiroSaver:
    def __find_save_dir__(self):
        for root, dirs, _ in os.walk(self.sekiro):
            for d in dirs:
                save_file = os.path.join(root, d, 'S0000.sl2')
                if os.path.exists(save_file):
                    return os.path.join(root, d)
        return None
    
    def __make_save_path__(self, d):
        files = []
        files.append(os.path.join(d, 'S0000.sl2'))
        files.append(os.path.join(d, 'S0000.sl2.bak'))
        return files
        
    def __init__(self):
        appdata = os.getenv("APPDATA")
        sekiro = os.path.join(appdata, "Sekiro")
        self.sekiro = sekiro
        self.default_save_dir = self.__find_save_dir__()
        print(f'Found save dir: {self.default_save_dir}')

    def open_default_save_dir(self):
        os.startfile(self.default_save_dir)

    def list_backups(self):
        backups = os.path.join(self.sekiro, 'manual_saves')
        return os.listdir(backups)

    def save(self, name):
        dir_path = os.path.join(self.sekiro, 'manual_saves', name)
        if os.path.exists(dir_path):
            raise Exception(f'Save {name} already exists')
        
        os.makedirs(dir_path, exist_ok=True)
        
        saves = self.__make_save_path__(self.default_save_dir)
        for save in saves:
            full_path = os.path.join(dir_path, os.path.basename(save))
            shutil.copy2(save, full_path)

    def load(self, name):
        dir_path = os.path.join(self.sekiro, 'manual_saves', name)
        if not os.path.exists(dir_path):
            raise Exception(f'Save {name} does not exist')
        
        saves = self.__make_save_path__(dir_path)
        for save in saves:
            if not os.path.exists(save):
                raise Exception(f'Save {name} is incomplete')

            full_path = os.path.join(self.default_save_dir, os.path.basename(save))
            os.remove(full_path)
            shutil.copy2(save, full_path)