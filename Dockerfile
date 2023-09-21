# This image is compatible with:
# Windows_Server-2022-English-Full-ECS_Optimized-2023.08.09
# (ami-0752842f81d2d1ea3)
# Known issue: sometimes the generated default Docker NAT subnetwork
# conflicts with the VPC subnet where ECS-optimized instance is
# launched. `docker network ps` and `docker network inspect <network>`
# to check.
FROM mcr.microsoft.com/windows-cssc/python3.7.2servercore:ltsc2022

WORKDIR /user/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --user
COPY server.py .
COPY templates/jokes.html ./templates/jokes.html

ENTRYPOINT ["python", "server.py"]
EXPOSE 5000
