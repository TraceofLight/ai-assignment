# B6-1 · OCI 웹 서비스 배포 실습

AWS의 VPC·EC2·Security Group을 OCI의 VCN·Compute·NSG에 대응한 실습이다. 기존 인스턴스 운영 규약에 따라 공유 자원을 재사용하고 실습 전용 컨테이너와 접근 규칙만 추가했다. 공유 인스턴스·볼륨·기존 서비스는 유지하며, 정리는 실습에서 추가한 구성에 한정한다.

## 제출물과 접속 검증

- 서비스 URL: **https://www.codyssey-domain-test.kro.kr/**
- 선택한 외부 검증 방식: **A — 브라우저 접속**. 방식 B인 `/health`의 HTTP 200과 `OK`도 확인했다.
- [관리자 SSH 접속 실행 로그](evidence/ssh-session.txt): 기존 사설 관리망에서 공개키 인증·원격 명령 실행·종료 코드 0 확인.
- 공인 IP HTTP 검증: [결과](evidence/http-after.txt). 서버 주소는 `<PUBLIC_IP>`로 치환했다.
- [아키텍처](docs/architecture.png), [IAM](docs/iam.md), [트러블슈팅](docs/troubleshooting.md), [정리 체크리스트](docs/cleanup-checklist.md).
- [단계별 접속 검증](docs/validation.md), [모니터링·확장·비용 대응 계획](docs/operations.md).
- [실습 컨테이너와 내부 HTTP 검증](evidence/final-server.txt), [네트워크 확인](evidence/network-after.txt), [권한 허용·거부](evidence/iam.txt).
- 증빙은 실제 실행 결과에서 과제 관련 부분만 발췌했다. 개인 인프라의 이름·주소·식별자는 공개하지 않는다. [증빙 표기 기준](evidence/README.md).

![외부 웹 접속](evidence/screenshots/external-page.png)

아래는 저장한 실제 명령 출력 중 실습 컨테이너와 localhost 응답만 발췌해 브라우저로 열람한 화면이다.

![Docker 및 내부 접속 검증](evidence/screenshots/docker-validation.png)

## 구성

| 과제 요소 | OCI 적용 |
|---|---|
| VPC / Public Subnet | 기존 VCN 및 공인 IP 사용이 가능한 서브넷 재사용 |
| Internet Gateway / Route Table | 기존 IGW, `0.0.0.0/0 → IGW` 라우트 확인 |
| EC2 | 기존 Ubuntu Compute 인스턴스 재사용 |
| Security Group | 전용 NSG 및 기존 Security List, 호스트 UFW |
| 접근 제어 | HTTP80·HTTPS443 공개, SSH22는 지정 관리자 IP `/32`로 제한 |
| IAM | Instance Principal의 제한 역할로 네트워크 조회·NSG 규칙 수정 검증 |
| 웹 서버 | Caddy Docker 컨테이너, `/health` → `200 OK` |
| 정리 | 운영 규약에 따라 공유 자원 유지, 추가 구성의 원복 절차 작성 |

요청 흐름은 인터넷 → IGW → public subnet → NSG/Security List → UFW → Caddy다. NSG와 Security List의 허용은 합쳐지므로 어느 한쪽의 불필요한 허용도 함께 점검한다. IAM은 네트워크 통신이 아니라 OCI API 작업 권한을 제어한다.

**NSG가 Security List보다 우선하는 구조는 아니다.** 두 규칙 집합 중 허용되는 트래픽이 OCI 네트워크 계층을 통과한 뒤, 이 배포의 호스트 UFW와 웹 서버 설정도 만족해야 한다. Stateful 규칙은 응답 트래픽을 추적한다. 같은 방향의 트래픽이 stateful·stateless 규칙에 모두 해당하면 stateless가 우선하므로 반대 방향 허용도 필요하다. [OCI 보안 규칙](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securityrules.htm).

공개 포트는 웹 서비스에 필요한 TCP80/443, 관리 포트는 지정 IP의 TCP22로 한정한다. 컨테이너 관리 API·DB·개발 서버 포트는 공개하지 않는다. 아웃바운드는 공인 IP·IGW 기본 라우트·egress 및 OS 규칙이 함께 필요하다. 공인 IP 없는 사설 인스턴스의 외부 시작 통신에는 NAT Gateway를 고려하지만, 이번 구성에는 추가하지 않는다. [OCI 네트워크 개요](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/overview.htm).

![아키텍처](docs/architecture.png)

## 배포와 검증

- 이미지: `caddy:2-alpine`, 배포 시 [image.txt](image.txt)의 digest로 고정.
- 실행: [deploy.sh](scripts/deploy.sh)의 `docker run`, 컨테이너 `b6-1-cloud-lab`, 재시작 정책 `unless-stopped`.
- **포트 매핑:** `--network host` 사용으로 `-p` 매핑 없음. TCP80/443에 직접 리슨하며 UFW INPUT 규칙 적용. 관리 API는 localhost2019로 제한.
- 읽기 전용 루트, 사용자1000, `NET_BIND_SERVICE`만 허용. 메모리128MiB·CPU0.5·PID100·로그5MiB×2 제한.
- 실습 경로 `/opt/b6-1-cloud-lab`에 `Caddyfile`, `image.txt`, `site/`, 스크립트를 배치한다. 이미 사용 중인 포트나 동명 컨테이너가 있으면 배포가 중단된다.

```bash
sudo bash /opt/b6-1-cloud-lab/deploy.sh
curl --fail --include http://localhost/health
python scripts/verify.py https://www.codyssey-domain-test.kro.kr
```

## 도메인과 HTTPS

DNS A 레코드를 배포 대상 공인 IP로 연결하고 Caddy로 Let's Encrypt 인증서를 발급했다. HTTP는 HTTPS로 리다이렉트된다. 인증서 자동 갱신을 위해 Caddy 데이터 디렉터리를 유지한다.

HTTPS 검증 결과와 인증서 신뢰 검증은 해당 증빙 파일에 기록한다. 재배포 시에는 `Caddyfile`의 도메인을 자신의 도메인으로 변경한다.

- [HTTPS 200 응답](evidence/https-after.txt), [인증서 신뢰 검증](evidence/tls-certificate.json).
- [단기 응답시간 측정](evidence/health-sample.json): 외부 단일 클라이언트의 순차 요청 표본이며 부하·다중 네트워크 검증과 구분한다.
- DNS 설정 → TTL/전파 확인 → HTTP 리다이렉트 → HTTPS 검증 순서는 [검증 절차](docs/validation.md)를 따른다.

## 확장과 비용 대응

현재는 기존 무료 범위를 유지하며 추가 로드밸런서나 인스턴스를 생성하지 않는다. 확장이 필요하면 응답시간·오류율과 CPU·메모리·네트워크 지표로 병목을 먼저 확인한다. 지속적인 병목이나 가용성 요구가 확인될 때 OCI Load Balancer와 복수 백엔드를 검토한다.

[운영 계획](docs/operations.md)에 관측 주기·경보 기준·도입 조건·태그별 비용 추적·예산 초과 대응을 정리했다. 이 문서의 경보·비용 설정·로드밸런서는 **향후 계획**이며 현재 적용 완료 증빙이 아니다.
