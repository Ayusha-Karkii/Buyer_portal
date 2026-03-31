# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
import models
from auth import hash_password, verify_password, create_token
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Header
from jose import jwt, JWTError

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# REGISTER
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    if len(user.password) < 5:
        raise HTTPException(status_code=400, detail="Password too short")
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# LOGIN
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(email=user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_token({
        "id": db_user.id,
        "email": db_user.email,
        "name": db_user.name
    })
    return {"access_token": token}

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Expecting "Bearer <token>"
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # main.py
from pydantic import BaseModel

class FavouriteItem(BaseModel):
    property_name: str

# Get current user info + favourites
@app.get("/dashboard")
def dashboard(user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(id=user["id"]).first()
    favourites = [f.property_name for f in db_user.favourites]
    return {"name": db_user.name, "role": db_user.role, "favourites": favourites}

# Add favourite
@app.post("/favourite")
def add_favourite(item: FavouriteItem, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(id=user["id"]).first()
    fav = db.query(models.Favourite).filter_by(user_id=db_user.id, property_name=item.property_name).first()
    if fav:
        raise HTTPException(status_code=400, detail="Already in favourites")
    new_fav = models.Favourite(user_id=db_user.id, property_name=item.property_name)
    db.add(new_fav)
    db.commit()
    return {"message": "Added to favourites"}

# Remove favourite
@app.delete("/favourite")
def remove_favourite(item: FavouriteItem, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(id=user["id"]).first()
    fav = db.query(models.Favourite).filter_by(user_id=db_user.id, property_name=item.property_name).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(fav)
    db.commit()
    return {"message": "Removed from favourites"}