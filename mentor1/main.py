from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
import sqlite3
from datetime import datetime, timedelta
import secrets
# CONFIG
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # mật khẩu ứng dụng Gmail

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# DATABASE HELPER
def get_db():
    conn = sqlite3.connect("mentor_booking.db")
    conn.row_factory = sqlite3.Row
    return conn

# MODELS
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# UTILS
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def send_email(to_email: str, subject: str, content: str):
    msg = MIMEText(content, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())

# ======================
# API ENDPOINTS
# ======================

# 1. Đăng ký
@app.post("/register")
def register(user: UserRegister):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=? OR username=?", (user.email, user.username))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Username hoặc Email đã tồn tại")

    hashed_pw = get_password_hash(user.password)
    cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                   (user.username, user.email, hashed_pw))
    conn.commit()

    # Gửi email thông báo
    send_email(
        user.email,
        "Đăng ký thành công Mentor Booking",
        f"<h3>Xin chào {user.username},</h3><p>Bạn đã đăng ký thành công!</p>"
    )

    return {"msg": "Đăng ký thành công, vui lòng kiểm tra email"}

# 2. Đăng nhập
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (form_data.username,))
    user = cursor.fetchone()
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Sai username hoặc password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# 3. Lấy thông tin người dùng từ token
@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

    return {"username": username}

# 4. Quên mật khẩu (gửi link reset)
@app.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (req.email,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Email không tồn tại")

    token = secrets.token_urlsafe(32)
    expire_time = datetime.utcnow() + timedelta(hours=1)

    cursor.execute("UPDATE users SET reset_token=?, reset_token_expire=? WHERE email=?",
                   (token, expire_time, req.email))
    conn.commit()

    reset_link = f"http://localhost:8000/reset-password?token={token}"

    send_email(
        req.email,
        "Đặt lại mật khẩu Mentor Booking",
        f"<p>Vui lòng click vào link sau để đặt lại mật khẩu (hết hạn sau 1h):</p><a href='{reset_link}'>Reset Password</a>"
    )

    return {"msg": "Vui lòng kiểm tra email để đặt lại mật khẩu"}

# 5. Đặt lại mật khẩu
@app.post("/reset-password")
def reset_password(req: ResetPasswordRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE reset_token=?", (req.token,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=400, detail="Token không hợp lệ")

    expire_time = datetime.fromisoformat(user["reset_token_expire"])
    if datetime.utcnow() > expire_time:
        raise HTTPException(status_code=400, detail="Token đã hết hạn")

    new_hashed_pw = get_password_hash(req.new_password)
    cursor.execute("UPDATE users SET password_hash=?, reset_token=NULL, reset_token_expire=NULL WHERE id=?",
                   (new_hashed_pw, user["id"]))
    conn.commit()

    return {"msg": "Cập nhật mật khẩu thành công"}


