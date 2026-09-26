# OCI 웹 서비스 실습 실행 계획

> 실행 지침: superpowers:executing-plans에 따라 단계별 실행 및 검증.

**목표:** 기존 ai-research 인스턴스에 원복 가능한 공개 웹 서비스를 배포하고 OCI 대응 과제 증빙을 작성한다.

**구조:** 기존 네트워크와 VM을 재사용하고 단일 Caddy 컨테이너로 정적 웹·health·TLS를 제공한다. 운영 전후 상태를 비교하고 실습 전용 변경만 제거할 수 있게 한다.

**기술:** OCI Compute/VCN, Ubuntu, Docker, Caddy, SSH, curl, DNS, Markdown, PNG.

1. 변경 전 상태 수집 → `evidence/baseline.txt`, 비공개 방화벽 백업 `.local/` 저장. 외부 HTTP 미제공 확인.
2. 최소 서비스 구성 → `Caddyfile`, `site/index.html`, `scripts/deploy.sh`, `scripts/rollback.sh` 작성. 쉘 구문·Caddy 구성 검증.
3. 전용 경로 `/opt/b6-1-cloud-lab` 배포 → localhost 및 외부 `/health` 200 검증. 필요한 HTTP/HTTPS 규칙만 추가하고 기록.
4. 장애 재현 → 실습 health 경로만 일시 503으로 변경, 증상·로그 수집 후 정상 복구. 기존 서비스 health 유지 확인.
5. DNS/HTTPS → 사용자 A 레코드 반영 확인, TLS 및 웹 화면 캡처. 외부 네트워크/OCI 권한 제한은 정확히 기록.
6. 제출 산출물 → `README.md`, `docs/architecture.png`, `docs/troubleshooting.md`, `docs/cleanup-checklist.md`, 증빙 스크린샷 작성.
7. 최종 검증 → 기존 컨테이너 ID/시작 시각과 health, 신규 서비스 정상, 원복 절차 범위 확인. 사용자 요청 전까지 서비스 유지.

## 실행 결과 (2026-09-27)

1~3 완료. 4는 인위적 503 대신 실제 발생한 capability·CRLF·OCI ingress 오류의 재현/해결로 대체했다. 5는 DNS 미등록 및 공유 도메인 인증서 발급 제한으로 대기. 6~7 산출물과 외부 HTTP·Docker·IAM·기존 서비스 보존을 검증했다. 원복은 실행하지 않았다.
