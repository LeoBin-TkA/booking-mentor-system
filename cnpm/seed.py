from models import SessionLocal, User

def run_seed():
    session = SessionLocal()
    print("Đang thêm dữ liệu...")

    session.query(User).delete()

    users = [
        User(name="Nguyen Van A", email="a@example.com"),
        User(name="Tran Thi B", email="b@example.com"),
        User(name="Le Van C", email="c@example.com"),
    ]

    session.add_all(users)
    session.commit()
    print("Seed dữ liệu thành công!")

if __name__ == "__main__":
    run_seed()

