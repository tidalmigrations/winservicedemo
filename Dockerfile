# This image is compatible with:
# Windows_Server-2022-English-Full-ECS_Optimized-2023.08.09
# (ami-0752842f81d2d1ea3)
# Known issue: sometimes the generated default Docker NAT subnetwork
# conflicts with the VPC subnet where ECS-optimized instance is
# launched. `docker network ps` and `docker network inspect <network>`
# to check.
FROM mcr.microsoft.com/windows-cssc/python3.7.2servercore:ltsc2022

WORKDIR /user/src/app

# Demonstrate a server
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --user
COPY server.py .
COPY templates/jokes.html ./templates/jokes.html

# Demonstrate a service
# Install Microsoft Visual C++ 2019 Redistributable
RUN Invoke-WebRequest -Uri https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile vc_redist.x64.exe; \
    Start-Process -FilePath .\vc_redist.x64.exe -ArgumentList '/install', '/passive', '/norestart' -Wait; \
    Remove-Item vc_redist.x64.exe
COPY hello_world_service.py .

# Install the service
RUN python -m pip install pywin32; \
    python hello_world_service.py install

# Copy the entrypoint script
COPY entrypoint.ps1 .

ENTRYPOINT ["powershell", "./entrypoint.ps1"]
EXPOSE 5000
