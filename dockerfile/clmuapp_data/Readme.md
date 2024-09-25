# pyclmuapp docker container

How to create?

```bash
docker buildx create --name mybuilder
docker buildx ls
docker buildx use mybuilder
docker buildx build --platform linux/amd64,linux/arm64 -t envdes/clmu-app:1.1 --push .
```