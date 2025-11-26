from fastapi import HTTPException

students = {}
canteens = {}
reservations = {}

students_counter = 1
canteens_counter = 1
reservations_counter = 1

def generate_student_id():
    global students_counter
    current = students_counter
    students_counter += 1
    return str(current)

def generate_canteen_id():
    global canteens_counter
    current = canteens_counter
    canteens_counter += 1
    return str(current)

def generate_reservation_id():
    global reservations_counter
    current = reservations_counter
    reservations_counter += 1
    return str(current)

def stud_or_404(student_id):
    student_id = str(student_id)
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def can_or_404(canteen_id):
    canteen_id = str(canteen_id)
    canteen = canteens.get(canteen_id)
    if canteen is None:
        raise HTTPException(status_code=404, detail="Canteen not found")
    return canteen

def res_or_404(reservation_id):
    reservation_id = str(reservation_id)
    reservation = reservations.get(reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

def require_admin(student_id):
    student = stud_or_404(student_id)
    if not student.isAdmin:
        raise HTTPException(status_code=403, detail="Student is not admin")
    return student

