from fastapi import APIRouter, HTTPException, Header
from app.models import ReservationsCreate, Reservations, Canteens
from app.database import (reservations, generate_reservation_id, stud_or_404, can_or_404, res_or_404)
from app.utils import (validate_time_format, validate_date, time_to_min, is_half_hour, overlaps)

router = APIRouter(
    prefix = "/reservations",
    tags = ["reservations"]
)

def meal_for_time(canteen, time_str, duration):

    start_min = time_to_min(time_str)
    end_min = start_min + duration

    for wh in canteen.workingHours:

        wh_start = time_to_min(wh.from_)
        wh_end = time_to_min(wh.to)

        if start_min >= wh_start and end_min <= wh_end:
            return wh.meal
        
    return None

@router.post("", response_model=Reservations, status_code=201)
def create_reservation(res_in: ReservationsCreate):

    student = stud_or_404(res_in.studentId)
    canteen = can_or_404(res_in.canteenId)

    if not validate_date(res_in.date):
        raise HTTPException(status_code=400, detail="Enter todays date or future date")
    if not validate_time_format(res_in.time) or not is_half_hour(res_in.time):
        raise HTTPException(status_code=400, detail="Time format must be HH:MM on full or half hour")
    if res_in.duration not in (30,60):
        raise HTTPException(status_code=400, detail="Duration must be 30 or 60 minutes")
    
    meal = meal_for_time(canteen, res_in.time, res_in.duration)
    if meal is None:
        raise HTTPException(status_code=400, detail="Reservation time must be in working hours")
    
    for reservation in reservations.values():
        if(
            reservation.studentId == student.id
            and reservation.date == res_in.date
            and reservation.status == "Active"
            and overlaps(reservation.time, reservation.duration, res_in.time, res_in.duration)

        ):
            raise HTTPException(status_code=400, detail="Student already has reservation in this time slot")
        
    count = 0
    for reservation in reservations.values():
        if(
            reservation.canteenId == canteen.id
            and reservation.date == res_in.date
            and reservation.status == "Active"
            and overlaps(reservation.time, reservation.duration, res_in.time, res_in.duration)
        ):
            count += 1

    if count >= canteen.capacity:
        raise HTTPException(status_code=400, detail="Canteen is full for this time slot")
    
    reservation_id = generate_reservation_id()

    new_res = Reservations(
        id = reservation_id,
        status = "Active",
        studentId = student.id,
        canteenId = canteen.id,
        date = res_in.date,
        time = res_in.time,
        duration = res_in.duration

    )

    reservations[reservation_id] = new_res
    return new_res

@router.delete("/{reservation_id}", response_model=Reservations)
def cancel_reservation(reservation_id, student_id = Header(..., alias="studentId"),):
     
     reservation = res_or_404(reservation_id)
     student = stud_or_404(student_id)

     if reservation.studentId != student.id:
         raise HTTPException(status_code=403, detail="Student cannot candel this reservation")
     
     reservation.status = "Cancelled"
     return reservation

        


            