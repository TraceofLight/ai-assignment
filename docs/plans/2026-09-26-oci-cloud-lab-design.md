# OCI 웹 서비스 실습 설계

사용자 승인: AWS 요구사항을 OCI에 대응시킨다. ai-research의 기존 무료 범위 설정을 사용한다. 인스턴스를 종료하지 않으며, 사용자의 명시적 요청 전까지 실습 서비스를 유지한다.

- 기존 OCI 춘천 ai-research VM, VCN, Subnet, Internet Gateway, 볼륨 재사용.
- 독립 컨테이너 `b6-1-cloud-lab`로 정적 페이지와 `/health` 제공.
- Caddy 웹 서버로 HTTP 및 도메인 기반 HTTPS 제공. Docker host network를 사용해 호스트 UFW 규칙을 적용하고 Docker 포트 게시의 방화벽 우회를 피한다.
- 도메인: `www.codyssey-domain-test.kro.kr`, A 레코드: `152.67.213.106`.
- 기존 거래 컨테이너와 NetBird 설정·데이터·생명주기는 변경하지 않는다.
- 변경 전 컨테이너 ID, 이미지, 방화벽, 사용 포트와 기존 health를 저장한다. 실습 리소스만 명시적으로 추적한다.
- 원복은 실습 컨테이너·파일·추가 규칙에 한정한다. 공유 리소스 종료/삭제와 전체 Docker 정리는 금지한다.
- 인프라 조회 권한 부족 등 미검증 항목은 실제 확인 결과와 분리해 문서화한다.

완료 기준: 외부 IP HTTP 200 및 고정 health 응답, DNS/HTTPS 검증(전파·접근 허용 후), 실제 장애 재현·해결 증빙, 아키텍처 PNG, 원복 체크리스트, 기존 서비스 정상 확인.
