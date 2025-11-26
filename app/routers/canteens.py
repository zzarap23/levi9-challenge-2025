from fastapi import APIRouter, HTTPException, Header
from typing import List
from datetime import datetime
from app.models import CanteensCreate, CanteensUpdate, Canteens
from app.database import (canteens, reservations, generate_canteen_id, can_or_404, require_admin)
from app.utils import (validate_time_format, validate_date, time_to_min, iterate_date, min_to_time, overlaps)

router = APIRouter(
    prefix = "/canteens",
    tags = ["canteens"]
)

@router.post("", response_model=Canteens, status_code=201)
def create_canteen(canteen_in: CanteensCreate, student_id = Header(..., alias="studentId"), ):
        
        require_admin(student_id)

        if canteen_in.capacity <= 0:
                raise HTTPException(status_code=400, detail="Capacity must be positive")
        
        for wh in canteen_in.workingHours:
                if not validate_time_format(wh.from_) or not validate_time_format(wh.to):
                        raise HTTPException(status_code=400, detail="Invalid working hours time format")
                
        canteen_id = generate_canteen_id()

        canteen = Canteens(
                id = canteen_id,
                name = canteen_in.name,
                location = canteen_in.location,
                capacity = canteen_in.capacity,
                workingHours = canteen_in.workingHours
        )

        canteens[canteen_id] = canteen

        return canteen

@router.get("", response_model=List[Canteens])
def list_canteens():
        return list(canteens.values())

#ovde je bio 

@router.put("/{canteen_id}", response_model=Canteens)
def update_canteen(canteen_id, update: CanteensUpdate, student_id = Header(..., alias="studentId"), ):
        require_admin(student_id)
        canteen = can_or_404(canteen_id)

        if update.name is not None:
                canteen.name = update.name
        if update.location is not None:
                canteen.location = update.location
        if update.capacity is not None:
                if update.capacity <= 0:
                        raise HTTPException(status_code=400, detail="Capacity must be positive")
                canteen.capacity = update.capacity
        if update.workingHours is not None:
                for wh in update.workingHours:
                        if not validate_time_format(wh.from_) or not validate_time_format(wh.to):
                                raise HTTPException(status_code=400, detail="Invalid working hours time format")
                canteen.workingHours = update.workingHours

        canteens[canteen_id] = canteen
        canteen = can_or_404(canteen_id)
        return canteen

@router.delete("/{canteen_id}", status_code=204)
def delete_canteen(canteen_id, student_id = Header(..., alias="studentId"), ):
        require_admin(student_id)
        canteen = can_or_404(canteen_id)

        for reservation in reservations.values():
                if reservation.canteenId == canteen.id and reservation.status == "Active":
                        reservation.status = "Cancelled"

        del canteens[canteen_id]
        return None

def compute_remaining_capacity_for_slot(canteen, date_str, slot_start_time, duration):
        used = 0
        for reservation in reservations.values():
                if(
                        reservation.canteenId == canteen.id
                        and reservation.date == date_str
                        and reservation.status == "Active"
                        and overlaps(reservation.time, reservation.duration, slot_start_time, duration)
                ):
                        used += 1
        return canteen.capacity - used

@router.get("/status")
def all_canteens_status(startDate, endDate, startTime, endTime, duration):

        try:
                duration = int(duration)
        except:
                raise HTTPException(status_code=400, detail="Invalid duration")
        if not validate_date(startDate) or not validate_date(endDate):
                raise HTTPException(status_code=400, detail="Invalid dates")
        
        start_dt = datetime.strptime(startDate, "%Y-%m-%d").date()
        end_dt = datetime.strptime(endDate, "%Y-%m-%d").date()

        if start_dt > end_dt:
                raise HTTPException(status_code=400, detail="Starting date must be before or equal to end date")
        
        if not validate_time_format(startTime) or not validate_time_format(endTime):
                raise HTTPException(status_code=400, detail="Invalid time format")
        
        if time_to_min(startTime) >= time_to_min(endTime):
                raise HTTPException(status_code=400, detail="Starting time must be before end time")
        
        if duration not in(30,60):
                raise HTTPException(status_code=400, detail="Duration must be 30 or 60")
        
        response = []

        for canteen in canteens.values():
                slots = []

                for current_date in iterate_date(startDate, endDate):
                        date_str = current_date.strftime("%Y-%m-%d")

                        for wh in canteen.workingHours:
                                wh_start = max (
                                        time_to_min(wh.from_),
                                        time_to_min(startTime)
                                )

                                wh_end = min (
                                        time_to_min(wh.to),
                                        time_to_min(endTime)
                                )

                                t = wh_start

                                while t + duration <= wh_end:
                                        slot_time_str = min_to_time (t)
                                        remaining = compute_remaining_capacity_for_slot(canteen, date_str, slot_time_str, duration)
                                        slots.append(
                                                {
                                                        "date": date_str,
                                                        "meal": wh.meal,
                                                        "startTime": slot_time_str,
                                                        "remainingCapacity": remaining
                                                }
                                        )
                                        t += duration
                response.append({
                        "canteenId": canteen.id,
                        "slots": slots
                })
        return response

@router.get("/{canteen_id}/status")
def single_canteen_status(canteen_id, startDate, endDate, startTime, endTime, duration):
        canteen = can_or_404(canteen_id)

        try:
                duration = int(duration)
        except:
                raise HTTPException(status_code=400, detail="Invalid duration")

        if not validate_date(startDate) or not validate_date(endDate):
                raise HTTPException(status_code=400, detail="Invalid dates")
        start_dt = datetime.strptime(startDate, "%Y-%m-%d").date()
        end_dt = datetime.strptime(endDate, "%Y-%m-%d").date()
        if start_dt > end_dt:
                raise HTTPException(status_code=400, detail="Starting date must be before or equal to end date")
        
        if not validate_time_format(startTime) or not validate_time_format(endTime):
                raise HTTPException(status_code=400, detail="Invalid time format")
        
        if time_to_min(startTime) >= time_to_min(endTime):
                raise HTTPException(status_code=400, detail="Starting time must be before end time")
        
        if duration not in(30,60):
                raise HTTPException(status_code=400, detail="Duration must me 30 or 60")
        
        slots = []

        for current_date in iterate_date(startDate, endDate):
                date_str = current_date.strftime("%Y-%m-%d")

                for wh in canteen.workingHours:
                    wh_start = max (
                            time_to_min(wh.from_),
                            time_to_min(startTime)
                            )

                    wh_end = min (
                            time_to_min(wh.to),
                            time_to_min(endTime)
                            )

                    t = wh_start

                    while t + duration <= wh_end:
                            slot_time_str = min_to_time (t)
                            remaining = compute_remaining_capacity_for_slot(canteen, date_str, slot_time_str, duration)
                            slots.append(
                                    {
                                            "date": date_str,
                                            "meal": wh.meal,
                                            "startTime": slot_time_str,
                                            "remainingCapacity": remaining
                                    }
                            )
                            t += duration
        return{
                "canteenId": canteen.id,
                "slots": slots

                }

@router.get("/{canteen_id}", response_model=Canteens)
def get_canteen(canteen_id):
        return can_or_404(canteen_id)

                
        




                
                            
        

        



                

