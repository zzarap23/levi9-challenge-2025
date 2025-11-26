from fastapi import FastAPI, HTTPException, Header
from app.routers import students, canteens, reservations

app = FastAPI(
    title="Levi9 challenge"
)

app.include_router(students.router)
app.include_router(canteens.router)
app.include_router(reservations.router)
