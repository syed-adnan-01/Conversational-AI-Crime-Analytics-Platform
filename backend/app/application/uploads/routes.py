from fastapi import APIRouter,Depends,File,HTTPException,UploadFile
from app.auth.dependencies import get_current_user
from app.models.user import User
from .service import UploadService
router=APIRouter(); service=UploadService()
async def upload(file:UploadFile,current_user:User): return await service.upload(file)
@router.post('/evidence')
async def evidence(file:UploadFile=File(...),current_user:User=Depends(get_current_user)): return await upload(file,current_user)
@router.post('/fir')
async def fir(file:UploadFile=File(...),current_user:User=Depends(get_current_user)): return await upload(file,current_user)
@router.post('/document')
async def document(file:UploadFile=File(...),current_user:User=Depends(get_current_user)): return await upload(file,current_user)
@router.post('/image')
async def image(file:UploadFile=File(...),current_user:User=Depends(get_current_user)): return await upload(file,current_user)
@router.get('/{upload_id}')
def get(upload_id:str,current_user:User=Depends(get_current_user)):
 item=service.get(upload_id)
 if not item: raise HTTPException(404,'Upload not found')
 return item
@router.delete('/{upload_id}')
def delete(upload_id:str,current_user:User=Depends(get_current_user)): return {'deleted':service.delete(upload_id)}
