from .storage import LocalStorageProvider
class UploadService:
 def __init__(self,storage=None): self.storage=storage or LocalStorageProvider()
 async def upload(self,file): return await self.storage.save(file)
 def get(self,id): return self.storage.get(id)
 def delete(self,id): return self.storage.delete(id)
