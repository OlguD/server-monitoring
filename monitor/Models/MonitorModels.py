from pydantic import BaseModel, Field
from typing import List

class CPUModel(BaseModel):
    usage: float = Field(ge=0, le=100, description="CPU usage percentage")

class MemoryModel(BaseModel):
    usage: float = Field(ge=0, le=100, description="Memory usage percentage")

class DiskModel(BaseModel):
    usage: float = Field(ge=0, le=100, description="Disk usage percentage")

class NetworkModel(BaseModel):
    total_usage_gb: float = Field(ge=0, description="Total network usage in GB")
    sent_mb: float = Field(ge=0, description="Sent data in MB")
    recv_mb: float = Field(ge=0, description="Received data in MB")

class ProcessModel(BaseModel):
    pid: int
    name: str
    cpu_percent: float = Field(ge=0, le=100, description="Process CPU usage")
    memory_percent: float = Field(ge=0, le=100, description="Process memory usage")
    memory_usage: float = Field(ge=0, description="Process memory usage in MB")
    status: str


class AllMonitorModel(BaseModel):
    cpu: CPUModel
    memory: MemoryModel
    disk: DiskModel
    network: NetworkModel
    processes: List[ProcessModel]