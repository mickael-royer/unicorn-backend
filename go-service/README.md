# unicorn-express-server
Publish service for Unicorn App
## Build and Run
### Build Docker image with Podman
```
podman build --build-arg-file=.env -t unicorn-publish . 
```
### Run image with Podman
```
podman run -p 8050:8050 unicorn-publish
```
### Init dapr with Podman
```
dapr init --container-runtime podman
```
### Run dapr
```
dapr run --app-id unicorn-publish \
  --app-port 8050 \
  --dapr-http-port 3502 \
  --dapr-grpc-port 50003 \
  --resources-path ../dapr-components \
  -- go run main.go
```
