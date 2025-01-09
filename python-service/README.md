# unicorn-express-server
BFF for Unicorn App
## Build and Run
### Build Docker image with Podman
```
podman build --build-arg-file=.env -t unicorn-sub . 
```
### Run image with Podman
```
podman run -p 3001:3001 unicorn-sub
```
### Init dapr with Podman
```
dapr init --container-runtime podman
```
### Run dapr
```
dapr run --app-id python-process \
  --app-port 5001 \
  --dapr-http-port 3501 \
  --dapr-grpc-port 50002 \
  --resources-path ../dapr-components \
  -- uvicorn app.api:app --host 0.0.0.0 --port 5001
```