from sqlalchemy_media import FileSystemStore, StoreManager



def factory():
    from app.app import app
    return FileSystemStore(f"{app.root_path}/uploads", '/media/')


StoreManager.register("fs", factory, default=True)
