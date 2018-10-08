
from lib.memory_management import memory
from pathlib import Path

class FileSystemControl:
    
    _CURRENT_PATH = 'current_path'
    
    current_path = ""
    
    @memory
    async def __init__(self,memory,initial_path=None):
        
        await memory_path = memory.get(self._CURRENT_PATH)
        
        if initial_path:
            path = Path(initial_path)
        elif memory_path:
            path = Path(memory_path)
        else:
            path = Path.cwd()
        
        if not path.exists():
            raise Exception('Provided path does not exists!')
             
        self.current_path = path
        
    @memory
    async def set_path(self, memory, path,relative=False):
        new_path = Path(path) if not relative else Path(str(self.current_path),path)
        if not new_path.exists():
            raise Exception('Provided path does not exists!')
        await memory.set(self._CURRENT_PATH,str(new_path))
        
    @memory
    async def move_up(self, memory, times = 0):
        new_path = self.current_path.parents[times]
        await memory.set(self._CURRENT_PATH,str(new_path))
    
    def list_directory(self):
        dir_path = self.current_path
        if not dir_path.is_dir():
            dir_path = Path(*dir_path.parts[:-1])
        return [x for x in self.current_path.iterdir()]
    
    def retrieve_file(self, file_name=None):
        if self.current_path.is_file():
            return self.current_path.read_bytes()
        else:
            if file_name:
                file_path = Path(self.current_path,file_name)
                if file_path.is_file():
                    return file_path.read_bytes()
                
        raise Exception('No file specified')
    
    def save_file(self,file_bytes,file_name):
        file_path = Path(self.current_path,file_name)
        file_path.write_bytes(file_bytes)
    