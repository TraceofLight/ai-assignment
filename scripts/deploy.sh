#!/usr/bin/env bash
set -euo pipefail
cd /opt/b6-1-cloud-lab
name=b6-1-cloud-lab
if docker container inspect "$name" >/dev/null 2>&1; then
  echo '기존 실습 컨테이너가 있습니다. 중복 배포를 중단합니다.' >&2
  exit 1
fi
if ss -H -ltn '( sport = :80 or sport = :443 or sport = :2019 )' | grep -q .; then
  echo '80/443/2019 포트가 사용 중입니다. 기존 서비스를 확인하세요.' >&2
  exit 1
fi
image=$(tr -d '\r\n' < image.txt)
install -d -o 1000 -g 1000 data config
docker run --rm --network none --cap-drop ALL --cap-add NET_BIND_SERVICE --entrypoint caddy \
  -v "$PWD/Caddyfile:/etc/caddy/Caddyfile:ro" "$image" validate --config /etc/caddy/Caddyfile
docker run -d --name "$name" --label assignment=b6-1 \
  --restart unless-stopped --network host --user 1000:1000 \
  --read-only --cap-drop ALL --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges --memory 128m --cpus 0.5 --pids-limit 100 \
  --log-opt max-size=5m --log-opt max-file=2 \
  --tmpfs /tmp:rw,noexec,nosuid,size=16m \
  -v "$PWD/Caddyfile:/etc/caddy/Caddyfile:ro" \
  -v "$PWD/site:/srv:ro" -v "$PWD/data:/data" -v "$PWD/config:/config" \
  "$image"
