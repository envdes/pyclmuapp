# pyclmuapp docker container

How to create?

```bash
docker buildx create --name mybuilder
docker buildx ls
docker buildx use mybuilder
docker buildx build --platform linux/amd64,linux/arm64 -t junjieyuuom/pyclmuapp:latest --push .
```

How to use?

```bash
docker run --hostname clmu-app -p 8080:7860 pyclmuapp
```