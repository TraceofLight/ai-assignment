# 접속·네트워크 검증 절차

아래 `<...>`는 운영 환경에서 채우는 값이다. 명령의 기대 결과는 재현 가이드이며 실제 결과를 가장한 출력이 아니다. 리소스 OCID·주소·생성 시각은 운영 기록에서 관리하고 공개 저장소에 복사하지 않는다.

## 관리자 SSH 접속 실행 증빙

[실제 SSH 로그](../evidence/ssh-session.txt)는 2026-10-04 관리자 PC에서 `ssh -v`로 수집했다. 기존 사설 관리망(VPN)을 통해 접속했으며 `Authenticated to ... using "publickey"`, 원격 `SSH_EXECUTION_OK`·UTC 시각 출력, `Exit status 0`과 로컬 종료 코드 0을 확인했다. 기존 `known_hosts`에 저장된 동일 서버의 키를 `HostKeyAlias`로 지정해 검증했으며 호스트 키 검증을 끄지 않았다.

같은 수집 시점의 공인 주소 TCP22 접속은 시간 초과였다. 원인은 확정하지 않았고 네트워크 규칙을 변경하지 않았다. 따라서 이번 로그는 **사설 관리망을 통한 관리자 SSH 성공 증빙**이며 현재 공인 경로 SSH 성공을 입증하지 않는다. 웹 서비스의 외부 HTTP/HTTPS 검증과는 별개다. 기존 네트워크 요약의 SSH 성공 문장은 초기 구성 당시 기록이다.

계정·주소·키 경로·지문만 비식별 처리했고 인증 방식·원격 출력·종료 상태는 실제 결과를 보존했다. 서버 설정 변경이나 서비스 재시작 없이 출력 명령만 실행했다.

## DNS부터 HTTPS까지

1. 도메인의 A 레코드에 배포 대상 공인 IP를 설정한다. DNS를 바꾸기 전에 웹 서버 도메인 설정과 TCP80/443 허용 여부를 확인한다.
2. 다음 조회에서 권한 DNS 및 공용 resolver 응답이 설정한 주소와 일치하는지 확인한다. 불일치하면 레코드·TTL을 확인하고 캐시 만료 후 다시 조회한다. 전파 완료 시간을 고정값으로 가정하지 않는다.

```bash
dig +short A <DOMAIN>
dig @1.1.1.1 +short A <DOMAIN>
dig @8.8.8.8 +short A <DOMAIN>
```

3. HTTP 리다이렉트와 HTTPS를 확인한다. `-k`로 인증서 오류를 우회하지 않는다.

```bash
curl --max-time 10 -I http://<DOMAIN>/health
curl --fail --max-time 10 -i https://<DOMAIN>/health
python scripts/verify.py https://<DOMAIN>
```

기대 결과: HTTP는 HTTPS로 308, HTTPS `/health`는 200과 `OK`, 루트 페이지는 200과 `HELLO CLOUD`. [실제 DNS 검증](../evidence/dns-verified.txt), [실제 HTTPS 검증](../evidence/https-after.txt).

## 장애 발생 시 계층별 확인

| 단계 | 검사 명령 | 확인할 결과 |
|---|---|---|
| 웹 서버 | `curl --fail -i http://localhost/health` | 200 및 `OK` |
| 포트 리슨 | `sudo ss -ltnp '( sport = :80 or sport = :443 )'` | 웹 서버가 대상 포트에서 리슨 |
| 호스트 방화벽 | `sudo ufw status numbered` | 필요한 웹 포트 허용, 관리 포트 소스 제한 |
| VNIC / NSG | `oci --auth instance_principal network vnic get --vnic-id <VNIC_OCID>` | 대상 VNIC에 실습 NSG 연결 |
| NSG 규칙 | `oci --auth instance_principal network nsg rules list --nsg-id <NSG_OCID> --all` | TCP80/443 허용, 불필요한 포트 없음 |
| Security List | `oci --auth instance_principal network security-list get --security-list-id <SL_OCID>` | NSG와 합쳐도 SSH가 지정 IP로만 제한됨 |
| 라우트 | `oci --auth instance_principal network route-table get --rt-id <ROUTE_TABLE_OCID>` | `0.0.0.0/0 → IGW` |
| 게이트웨이 | `oci --auth instance_principal network internet-gateway get --ig-id <IGW_OCID>` | 해당 VCN의 IGW 활성화 |
| 아웃바운드 | `curl --fail --max-time 10 -I https://example.com` | 외부 HTTPS 응답 |
| 외부 클라이언트 | `curl --fail --max-time 10 -i http://<PUBLIC_IP>/health` | 200 및 `OK` |

조회 시 기본 리전이 다르면 `--region <REGION>`을 추가한다. 전체 방화벽·포트 목록 대신 관련 규칙만 발췌해 증빙한다. 실제 실패 사례는 [HTTP timeout](../evidence/http-before.txt), 분석과 해결은 [트러블슈팅](troubleshooting.md)을 따른다.

SSH 실패 시에는 `ssh -vv -o ConnectTimeout=10 <SSH_USER>@<HOST>`의 연결 단계와 TCP22 규칙을 확인한다. 이 명령은 진단 예시이며 실습에서 SSH 실패를 재현했다는 뜻은 아니다. 공개 로그에서는 사용자·주소·키 경로를 제거한다.

## 관리 접속 대안과 검증 범위

- 지정 IP `/32`: 구성이 단순하지만 관리자 공인 IP 변경 시 규칙 갱신이 필요하다.
- Jump Host/Bastion: 접속 경로를 집중 관리할 수 있지만 별도 접근 정책·가용성·운영 비용 검토가 필요하다.
- VPN: 관리 포트를 사설망으로 제한할 수 있지만 클라이언트·키·접속 권한 관리가 필요하다.

현재 증빙은 외부 단일 클라이언트 기준이다. 모바일/별도 네트워크 검증은 아직 수행하지 않았다. 추가 검증 시 Wi-Fi와 분리된 모바일망 등에서 같은 URL과 `/health`를 요청하고, 시간·HTTP 상태·응답만 기록한다. 출발지 IP 등 개인 네트워크 정보는 제출하지 않는다.
