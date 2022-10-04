from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import Gender, Role, UpdateUser, User

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("aa5ff452-a6a3-4fa6-92e2-3086894bb1e4"),
        first_name="Luiz",
        last_name="Mosciaro",
        gender=Gender.male,
        roles=[Role.admin,Role.user]
    ),
    User(
        id=UUID("e998f610-ab94-4280-8a2e-3232bbf7c903"),
        first_name="Iza",
        last_name="Valeria",
        gender=Gender.female,
        roles=[Role.user]
    )
]

@app.get("/")
async def root():
    return {"Hello":"Mundo"}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_users(user:User):
    db.append(user)
    return {"Id":user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"Deleted User":user.first_name}
    raise HTTPException(
        status_code=404,
        detail=f"User with id {user_id} not found"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update:UpdateUser,user_id:UUID):
    updates = []
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
                updates.append(user.first_name)
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
                updates.append(user.last_name)
            if user_update.gender is not None:
                user.gender = user_update.gender
                updates.append(user.gender)
            if user_update.roles is not None:
                user.roles = user_update.roles
                updates.append(user.roles)
            return f"Updates made in id {user_id}:",updates
    raise HTTPException(
        status_code=404,
        detail=f"User with id {user_id} not found"
    )