# Start the hello_world_service
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "hello_world_service.py", "start"

# Start the server
python server.py