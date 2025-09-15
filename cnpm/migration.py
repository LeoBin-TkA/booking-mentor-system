from models import Base, engine

def run_migration():
    print("👉 Đang tạo bảng...")
    Base.metadata.create_all(engine)
    print("✅ Tạo bảng thành công!")

if __name__ == "__main__":
    run_migration()
