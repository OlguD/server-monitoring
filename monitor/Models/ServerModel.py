from pydantic import BaseModel, Field

class ServerModel(BaseModel):
    name: str = Field(description="Server name")
    ip: str = Field(description="Server IP address")
    port: int = Field(description="Server port number")
    cpu: float = Field(ge=0, le=100, description="CPU usage percentage")
    memory: float = Field(ge=0, le=100, description="Memory usage percentage")
    disk: float = Field(ge=0, le=100, description="Disk usage percentage")
    network: float = Field(ge=0, description="Total network usage in GB")
    sent: float = Field(ge=0, description="Sent data in MB")
    received: float = Field(ge=0, description="Received data in MB")
    processes: int = Field(ge=0, description="Number of processes running on the server")
    status: str = Field(description="Server status")
    last_updated: str = Field(description="Last updated time")