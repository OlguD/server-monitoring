from pydantic import BaseModel

class ServerConfig(BaseModel):
    name: str
    ip: str
    port: int
    username: str
    password: str
    status: str