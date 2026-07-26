from abc import ABC,abstractmethod
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
class StorageProvider(ABC):
 @abstractmethod
 async def save(self,file:UploadFile)->dict: ...
 @abstractmethod
 def get(self,id:str): ...
 @abstractmethod
 def delete(self,id:str)->bool: ...
class LocalStorageProvider(StorageProvider):
 def __init__(self,root:Path|None=None): self.root=root or Path('/tmp/crimesphere-uploads'); self.root.mkdir(parents=True,exist_ok=True); self.items={}
 async def save(self,file):
  id=uuid4().hex; path=self.root/id; path.write_bytes(await file.read()); item={'id':id,'filename':file.filename,'content_type':file.content_type,'path':str(path)}; self.items[id]=item; return item
 def get(self,id): return self.items.get(id)
 def delete(self,id):
  item=self.items.pop(id,None)
  if item: Path(item['path']).unlink(missing_ok=True)
  return item is not None
class CatalystStorageProvider(StorageProvider):
 async def save(self,file): raise NotImplementedError('TODO: Catalyst File Store provider')
 def get(self,id): raise NotImplementedError('TODO: Catalyst File Store provider')
 def delete(self,id): raise NotImplementedError('TODO: Catalyst File Store provider')
