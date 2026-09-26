#!/usr/bin/env bash
# 명시적 원복 요청을 받은 경우에만 실행. VM/볼륨/기존 컨테이너는 유지한다.
set -euo pipefail
cd /opt/b6-1-cloud-lab
name=b6-1-cloud-lab
# 오래된 표시 파일만 믿지 않고, 현재 규칙의 고유 comment도 함께 확인한다.
test ! -f added-ufw-80 || ufw show added | grep -Fx "ufw allow 80/tcp comment 'b6-1-http'" >/dev/null
test ! -f added-ufw-443 || ufw show added | grep -Fx "ufw allow 443/tcp comment 'b6-1-https'" >/dev/null
if docker container inspect "$name" >/dev/null 2>&1; then
  test "$(docker inspect --format '{{index .Config.Labels "assignment"}}' "$name")" = b6-1
  docker rm -f "$name"
fi
# 실습에서 실제 추가한 규칙만, 고유 comment와 함께 제거한다.
if test -f added-ufw-80; then
  ufw --force delete allow 80/tcp comment b6-1-http
  rm added-ufw-80
fi
if test -f added-ufw-443; then
  ufw --force delete allow 443/tcp comment b6-1-https
  rm added-ufw-443
fi
curl --fail --silent --show-error http://127.0.0.1:5001/health
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
echo '실습 컨테이너와 추가 UFW 규칙을 제거했습니다. 파일·이미지·DNS 정리는 체크리스트를 따르세요.'
