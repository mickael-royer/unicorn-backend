# unicorn-express-server
BFF for Unicorn App
## Build and Run
### Build Docker image with Podman
```
podman build --build-arg-file=.env -t unicorn-bff . 
```
### Run image with Podman
```
podman run -p 3001:3001 unicorn-bff
```
### Init dapr with Podman
```
dapr init --container-runtime podman
```
### Run dapr
```
dapr run --app-id unicorn-bff \
  --app-port 3001 \
  --dapr-http-port 3500 \
  --dapr-grpc-port 50001 \
  --resources-path ../dapr-components \
  -- npm run start
```