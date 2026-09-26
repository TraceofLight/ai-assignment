# 실습 원복 체크리스트

## 현재 운영 방침

사용자 요청: **명시적으로 원복을 요청하기 전까지 서비스를 유지한다.** 따라서 아래 작업은 아직 실행하지 않았다. 인스턴스 종료나 리소스 삭제 완료를 의미하지 않는다.

기존 무료 범위 설정을 그대로 사용하며 Compute, Boot Volume/Block Volume, 공인 IP, VCN, Subnet, Route Table, Internet Gateway는 보존한다. 새 인스턴스, 디스크, NAT Gateway, Load Balancer, DB를 만들지 않는다.

## 변경 명세

| 항목 | 실습 전 | 실습 변경 | 원복 |
|---|---|---|---|
| Docker 컨테이너 | 거래 컨테이너 2개 | `b6-1-cloud-lab` 1개 추가 | 해당 이름·라벨 확인 후 제거 |
| 이미지 | Caddy 없음 | `image.txt`의 digest로 Caddy 추가 | 다른 컨테이너가 사용하지 않을 때만 해당 이미지 제거 |
| 서버 디렉터리 | 없음 | `/opt/b6-1-cloud-lab` | 증빙 확보 후 해당 경로만 제거 |
| Caddy 데이터 | 없음 | 위 디렉터리의 `data/`, `config/` | 인증서·ACME 계정 포함. 비밀값을 저장소에 복사하지 않고 경로 정리 시 제거 |
| OS UFW | 80/443 허용 없음 | `b6-1-http`, `b6-1-https` 규칙(IPv4/IPv6) | 추가 표시 파일이 있는 해당 규칙만 제거 |
| OCI NSG | VNIC의 NSG 없음 | `b6-1-web` 생성, TCP80/443 공개 후 VNIC 연결 | 해당 NSG만 분리·제거 |
| OCI Security List SSH | TCP22 source `0.0.0.0/0` | `112.153.56.84/32`, 설명 `b6-1-ssh-admin` | 향후 상태 비교 후 해당 규칙의 source·설명만 이전 값으로 복구 |
| DNS | 사용자 설정 전 | `www.codyssey-domain-test.kro.kr` A → `152.67.213.106` 예정·등록 대기 | 향후 등록한 경우 해당 신규 레코드만 제거 |
| OCI API 서명 키 | 실습 키 없음 | 사용자 제공 키로 `/home/ubuntu/.oci/b6-1-user/config`, `api_key.pem` 구성·인증 성공 | 다른 용도 사용 여부 확인 후 해당 실습 키·config만 정리 |
| OCI IAM | 실습 Dynamic Group/Policy 없음 | `b6-1-ai-research`, `b6-1-network-lab` 생성 | 전용 Policy 후 Dynamic Group 제거 |
| 기존 거래 서비스·NetBird | 실행 중 | 변경 없음 | 중지·삭제·재시작하지 않음 |
| OS의 기존 SSH 규칙 | 기존 상태 | 변경 없음 | 변경 없음 |

변경 전 근거: [baseline.txt](../evidence/baseline.txt). 정확한 OCI ID 및 SSH 이전 값은 [oci-resources.json](oci-resources.json), 적용 결과는 [network-after.txt](../evidence/network-after.txt)에 있다. 전체 iptables 백업과 OCI API 원문은 로컬 `.local/` 및 비공개 pwiki의 `raw/sources/2026-09-27-oci-b6-1/`에 보관한다.

## 1. 명시적 원복 요청 후 서비스 제거

서버에 SSH로 접속한 뒤 실행한다. SSH 키 경로는 pwiki의 ai-research 접속 기록을 따른다.

```bash
sudo bash /opt/b6-1-cloud-lab/rollback.sh
```

스크립트는 컨테이너의 `assignment=b6-1` 라벨을 확인하며, 불일치하면 중단한다. `added-ufw-80`, `added-ufw-443` 표시 파일이 있는 규칙만 삭제하며, 삭제 전에 `ufw show added`의 실제 규칙과 고유 comment가 일치하는지도 확인한다. 불일치하면 컨테이너를 지우기 전에 중단한다. **외부 OCI 규칙이나 DNS는 이 스크립트로 삭제하지 않는다.**

- [ ] 실습 컨테이너가 없어졌는지 `sudo docker ps -a --filter name=b6-1-cloud-lab` 확인.
- [ ] `sudo ufw status numbered`에서 실습 comment가 없어졌는지 확인.
- [ ] `sudo ss -ltnp '( sport = :80 or sport = :443 or sport = :2019 )'` 결과 확인.

격리된 임시 디렉터리와 모의 Docker/UFW 명령으로 규칙 변경·라벨 불일치 시 삭제 중단, 정상 원복 경로, 이미 없는 상태의 네 경우를 검증했다. [검증 기록](../evidence/rollback-safety.txt)은 실제 서비스 원복 완료를 의미하지 않는다.

## 2. OCI와 DNS의 신규 규칙 정리

- [ ] `oci-resources.json`의 `lab_nsg_id`를 조회하고 이름 `b6-1-web`, 태그 `assignment=b6-1`을 확인.
- [ ] 현재 VNIC의 `nsg-ids`를 새로 조회하고 **그 목록에서 실습 NSG ID 하나만 제외**하여 갱신. 조회의 최신 `etag`를 `--if-match`로 지정. 실습 이후 추가된 다른 NSG는 유지.
- [ ] 해당 NSG의 VNIC 목록이 비어 있고 다른 서비스가 재사용하지 않는지 확인한 뒤 실습 NSG 제거. 전체 Security List를 삭제하지 않음.
- [ ] Security List를 새로 조회하고 `b6-1-ssh-admin`, TCP22, source `112.153.56.84/32` 규칙이 여전히 정확히 일치하는지 확인. 다른 값으로 바뀌었으면 자동 복구하지 말고 후속 변경 의도를 확인.
- [ ] 원래 SSH 상태로 완전히 되돌릴 경우 **해당 규칙만** source `0.0.0.0/0`, description `null`로 복구. 다른 ingress/egress를 그대로 보존하고 최신 `etag`와 `--if-match` 사용. 이 작업은 SSH를 다시 전체 공개하므로, 좁힌 보안 규칙을 유지할지 원복 시 판단.
- [ ] 새 SSH 연결과 NetBird·기존 MiroFish health 정상 확인. 현재 개인 공인 IP가 바뀌면 OCI 콘솔 또는 기존 NetBird 경로로 source `/32`를 먼저 갱신해야 함.
- [ ] 사용자가 추가한 `www` A 레코드만 제거. 다른 도메인·레코드 유지.

조회·분리 명령 형태는 다음과 같다. `<...>`는 manifest와 **원복 시점의 최신 조회 결과**로 채운다. `[]`를 고정 입력하면 나중에 추가된 NSG까지 분리하므로 사용하지 않는다.

```bash
oci --config-file /home/ubuntu/.oci/b6-1-user/config --profile B6_LAB \
  network vnic get --vnic-id <vnic_id>
oci --config-file /home/ubuntu/.oci/b6-1-user/config --profile B6_LAB \
  network vnic update --vnic-id <vnic_id> \
  --nsg-ids '<현재 목록에서 lab_nsg_id만 제외한 JSON 배열>' --if-match <최신_etag> --force
oci --config-file /home/ubuntu/.oci/b6-1-user/config --profile B6_LAB \
  network nsg vnics list --nsg-id <lab_nsg_id> --all
```

## 3. IAM과 실행용 인증 파일 정리

- [ ] `lab_policy_id`가 `b6-1-network-lab`이고 태그가 실습용인지 확인 후 해당 정책만 제거.
- [ ] 다른 정책이 `lab_dynamic_group_id`를 참조하지 않는지 확인 후 `b6-1-ai-research` Dynamic Group만 제거.
- [ ] 사용자 제공 API 키는 지문 **`fa:ed:53:9a:81:71:a8:0c:85:00:20:69:f2:36:40:b0`**. 다른 용도로 재사용하지 않는지 확인하고, 실습 정리용 OCI 호출을 모두 마친 뒤 해당 키만 폐기. 기존 SSH 키나 다른 사용자 API 키는 유지.
- [ ] 폐기 후 서버 `/home/ubuntu/.oci/b6-1-user/`의 `api_key.pem`, `config`를 제거. 개인키는 이 과제 저장소나 공개 증빙에 복사하지 않음. 사용자 요청으로 저장한 비공개 pwiki 원본은 보존.
- [ ] 이전에 에이전트가 생성한 `/home/ubuntu/.oci/b6-1/` 키(지문 `4f:ef:b8:d1:2a:7a:f0:a2:d1:67:9f:21:b0:c0:1f:56`)는 별개이며 현재 사용하지 않음. 등록 여부를 확인해 해당 전용 파일·등록만 정리. 사용자 제공 키와 혼동하지 않음.
- [ ] 사용자 기본 `~/.oci/config`, 기존 OCI CLI 설치, OCI 사용자/관리자 그룹 자체는 보존.

## 4. 선택: 실습 파일과 이미지 제거

먼저 다음으로 원복용 경로와 이미지 사용 여부를 확인한다.

```bash
sudo realpath /opt/b6-1-cloud-lab
sudo docker ps -a --filter ancestor=caddy:2-alpine
sudo docker image inspect caddy:2-alpine --format '{{json .RepoDigests}}'
```

- [ ] `/opt/b6-1-cloud-lab`이 정확한 실습 경로인지 확인하고 다른 프로젝트 파일이 없는지 확인.
- [ ] 필요한 증빙을 로컬 저장소에 보관.
- [ ] 다른 컨테이너가 Caddy 이미지를 사용하면 이미지 유지.

확인 후에만 다음을 실행한다. 컨테이너가 남아 있으면 이미지 제거는 실패하며, 강제 옵션은 사용하지 않는다.

```bash
sudo docker image rm caddy:2-alpine
sudo rm -r -- /opt/b6-1-cloud-lab
```

`docker system prune`, 전체 방화벽 복원, 다른 프로젝트의 `compose down`, Compute 종료, 볼륨 삭제는 실행하지 않는다. 전체 방화벽 백업을 나중에 덮어쓰면 실습 이후의 정당한 변경을 잃을 수 있으므로, 기록한 변경만 역순으로 제거한다.

## 5. 기존 상태 검증

```bash
sudo docker inspect --format '{{.Name}} {{.Id}} {{.State.StartedAt}}' \
  openclaw-trading-mirofish-1 openclaw-trading-execution-tools-1
curl --fail http://127.0.0.1:5001/health
systemctl is-active docker netbird
```

- [ ] 기존 컨테이너 ID와 상태를 [baseline.txt](../evidence/baseline.txt)와 비교.
- [ ] MiroFish `status: ok` 및 Docker/NetBird `active` 확인.
- [ ] VM과 기존 볼륨·공인 IP·네트워크가 유지되는지 확인.
- [ ] 수행 시각과 결과를 `evidence/rollback.txt`에 별도로 저장. 아직 원복하지 않은 상태를 완료로 표시하지 않음.
