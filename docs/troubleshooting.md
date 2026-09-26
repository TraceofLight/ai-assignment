# 트러블슈팅 보고서

실습일: 2026-09-26~27(KST). 실제 명령 출력은 `evidence/`에 저장한다.

## 1. Caddy 실행 파일의 capability와 Docker 제한 충돌 — 해결

| 단계 | 내용 |
|---|---|
| 증상 | 구성 검증용 컨테이너 실행 시 `exec /usr/bin/caddy: operation not permitted`, 종료 코드 255 |
| 가설 | `--cap-drop ALL`로 제거한 Linux capability가 실행 파일에 필수로 지정되어 있음 |
| 검증 | 이미지 내부 `getcap /usr/bin/caddy`에서 `cap_net_bind_service=ep` 확인. `caddy version`만 실행해도 동일 실패하므로 설정 파일이나 HTTP 라우팅 문제가 아님 |
| 조치 | 모든 capability 제거는 유지하고 `--cap-add NET_BIND_SERVICE`만 추가. 검증 컨테이너와 실제 서비스 모두 적용 |
| 결과 | 같은 이미지의 `caddy version` 종료 코드 0, Caddy 구성 검증 성공, localhost `/health` 200 확인 |
| 재발 방지 | digest로 이미지 고정, 배포 전 같은 권한으로 구성 검증. `--privileged`나 전체 권한 복구를 사용하지 않음 |

근거: [capability-troubleshooting.txt](../evidence/capability-troubleshooting.txt).

## 2. Windows 줄바꿈이 이미지 참조에 섞임 — 해결

- **증상:** `docker: invalid reference format`으로 배포 중단.
- **가설:** `image.txt`의 CRLF에서 CR이 `$(cat image.txt)` 결과에 남음.
- **검증:** 원격 `od -An -tx1 image.txt`의 마지막 바이트가 `0d 0a`임을 확인.
- **조치:** `tr -d '\r\n' < image.txt`로 줄바꿈만 제거.
- **결과:** digest 이미지 참조 인식 및 배포 성공.
- **재발 방지:** `.gitattributes`에서 셸·텍스트 파일의 LF 지정.

## 3. localhost 정상, 외부 IP 접속 시간 초과 — 해결

- **증상:** VM 내부 `http://127.0.0.1/health`는 200, 외부 `http://152.67.213.106/health`는 curl 종료 코드 28.
- **가설:** OCI Security List/NSG의 HTTP ingress 미허용.
- **검증:** Caddy가 `*:80`, `*:443`에서 리슨. UFW에 80/443 허용 적용. Docker host network로 포트 게시 NAT/브리지 문제 제외. 초기 Instance Principal은 `NotAuthorizedOrNotFound`로 조회 불가. 이후 사용자 제공 API 키로 조회한 결과 VNIC의 NSG가 비어 있고 Security List에는 22/ICMP만 존재함을 확인. 기본 IGW 라우트는 정상.
- **조치:** 실습 전용 NSG `b6-1-web`에 stateful TCP 80/443 source `0.0.0.0/0` 규칙을 생성하고 해당 VNIC에 연결.
- **결과:** 외부 Windows PC에서 `/health` 200 + `OK`, `/` 200 + `HELLO CLOUD` 확인. 네트워크 규칙 누락이 원인이었음을 조치 전후 비교로 확인.
- **재발 방지:** 앱 리슨 → OS 방화벽 → OCI 규칙 → 외부 클라이언트 순서로 각각 확인하고, 신규 규칙에 실습 식별자를 남김.

근거: [http-before.txt](../evidence/http-before.txt), [deployment.txt](../evidence/deployment.txt), [http-after.txt](../evidence/http-after.txt), [network-after.txt](../evidence/network-after.txt).

## 4. 공유 도메인의 Let's Encrypt 인증서 발급 한도 — 해결

- **증상:** ACME `HTTP 429`, `too many certificates (50) already issued for "kro.kr" in the last 168h0m0s`.
- **가설·검증:** 발급 서버가 공유 상위 도메인 기준 제한을 명시. HTTP 애플리케이션 오류와 별개.
- **조치:** 2026-09-27 00:53 KST에 사용자 A 레코드 반영을 공용 DNS 두 곳과 서버에서 확인했다. HTTP 308 → HTTPS 리다이렉트도 확인. Caddy의 자동 재시도를 유지하며 CA가 안내한 시각 전에 강제 재발급을 반복하지 않는다. 자체 서명 인증서를 정상 공개 HTTPS 증빙으로 사용하지 않음.
- **결과:** 재시도 안내 시각(`2026-09-26 16:03 UTC`, KST 2026-09-27 01:03) 이후 `caddy reload --config /etc/caddy/Caddyfile --force`를 한 번 실행. 운영 CA HTTP-01 검증 및 공개 인증서 발급 성공. 외부 HTTPS 200 + `OK`, 기본 CA 신뢰·호스트명 검증 통과. 컨테이너/VM 재시작 없이 적용.
- **재발 방지:** 공유 무료 도메인도 상위 도메인 단위 제한 영향을 받을 수 있음을 기록. 공개 IP HTTP 검증과 HTTPS 보너스 결과를 분리.

근거: [DNS](../evidence/dns-verified.txt), [발급 로그](../evidence/tls-issued.txt), [HTTPS 응답](../evidence/https-after.txt), [인증서](../evidence/tls-certificate.json). 참고: [Caddy reload](https://caddyserver.com/docs/command-line#caddy-reload), [Let’s Encrypt 재시도 정책](https://letsencrypt.org/docs/rate-limits/#retrying-after-hitting-rate-limits).
