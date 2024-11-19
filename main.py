# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
#from database import SessionLocal, engine, Base
from supabase_ import SessionLocal, engine, Base
from models import User, Download
import schemas 
from schemas.user import LoginData

app = FastAPI()

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to my API!"}

@app.post("/users/")  # response_model es opcional
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user_username = db.query(User).filter(User.username == user.username).first()
    existing_user_email = db.query(User).filter(User.email == user.email).first()

    if existing_user_username:
        print("Usuario ya registrado con ese nombre de usuario:", user.username)
        raise HTTPException(status_code=400, detail="Username already registered")
    elif existing_user_email:
        print("Usuario ya registrado con ese correo electrónico:", user.email)
        raise HTTPException(status_code=400, detail="Email already registered")

    # Si pasa las verificaciones, crea el nuevo usuario
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=User.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


# Endpoint para recuperar todos los usuarios
@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    # Consulta a la base de datos para obtener todos los usuarios
    users = db.query(User).all()
    return users

@app.post("/login/")
def login(data: LoginData, db: Session = Depends(get_db)):
    # Busca al usuario por nombre de usuario
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not user.verify_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
        )

    return {"message": "Login successful", "user_id": user.id}  # Agrega el user_id a la respuesta


@app.post("/downloads/")
def register_download(download: schemas.DownloadCreate, db: Session = Depends(get_db)):
    # Crear un registro de descarga
    new_download = Download(user_id=download.user_id, filename=download.filename)
    db.add(new_download)
    db.commit()
    db.refresh(new_download)
    return new_download

@app.get("/downloads/{user_id}")
def get_user_downloads(user_id: int, db: Session = Depends(get_db)):
    downloads = db.query(Download).filter(Download.user_id == user_id).all()
    return downloads

