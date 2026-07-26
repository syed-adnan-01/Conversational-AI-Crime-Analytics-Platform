from fastapi import APIRouter,Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from .service import AnalyticsService
router=APIRouter(); service=AnalyticsService()
@router.get('/crime-trends',summary='Crime trends from registered cases')
def trends(current_user:User=Depends(get_current_user)): return service.monthly()
@router.get('/crime-types',summary='Case counts by crime type')
def crime_types(current_user:User=Depends(get_current_user)): return service.crime_types()
@router.get('/monthly',summary='Monthly case counts')
def monthly(current_user:User=Depends(get_current_user)): return service.monthly()
@router.get('/yearly',summary='Yearly case counts')
def yearly(current_user:User=Depends(get_current_user)): return service.yearly()
@router.get('/officers',summary='Case counts by assigned officer')
def officers(current_user:User=Depends(get_current_user)): return service.officers()
@router.get('/districts',summary='Case counts by police station')
def districts(current_user:User=Depends(get_current_user)): return service.districts()
@router.get('/evidence',summary='Evidence analytics unavailable')
def evidence(current_user:User=Depends(get_current_user)): return []
@router.get('/timeline',summary='Timeline analytics unavailable')
def timeline(current_user:User=Depends(get_current_user)): return []
@router.get('/chargesheets',summary='Chargesheet analytics unavailable')
def chargesheets(current_user:User=Depends(get_current_user)): return []
