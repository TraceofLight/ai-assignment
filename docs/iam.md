# 실습 IAM과 인증 경로

## 설정과 운영 역할

사용자가 제공한 API 서명 키로 전용 프로필 `B6_LAB`의 인증을 검증하고 초기 OCI 설정을 수행했다. 이 키는 기존 사용자 권한을 따르므로, 그 자체를 최소권한 실습 역할이라고 간주하지 않는다. 기존 계정·관리자 그룹·기존 정책은 변경하지 않았다.

이후 다음 실습 역할을 만들고 `--auth instance_principal`로 검증했다. 웹 컨테이너에는 사용자 API 키나 OCI config를 마운트하지 않는다.

- Dynamic Group: `b6-1-ai-research`.
- matching rule: **ai-research의 instance OCID 한 대만** 일치.
- Policy: `b6-1-network-lab`, 대상 인스턴스와 네트워크가 속한 compartment에 생성.
- 실제 정책의 ID는 [oci-resources.json](oci-resources.json)에 기록.

```text
Allow dynamic-group id <DYNAMIC_GROUP_OCID> to {
  VCN_READ, SUBNET_READ, VNIC_READ, ROUTE_TABLE_READ,
  INTERNET_GATEWAY_READ, SECURITY_LIST_READ,
  NETWORK_SECURITY_GROUP_READ, NETWORK_SECURITY_GROUP_LIST_SECURITY_RULES,
  NETWORK_SECURITY_GROUP_UPDATE_SECURITY_RULES
} in compartment id <COMPARTMENT_OCID>
```

정책은 실제로 한 줄 statement로 적용했다. 네트워크 경로 확인과 실습 NSG 규칙 실습에 필요한 9개 permission만 허용한다. NSG 규칙 수정은 **해당 compartment의 NSG 전체**에 적용되며 특정 NSG 한 개로 제한된 정책은 아니다. VM 생성·종료·크기 변경, 볼륨, Object Storage, DB, IAM 관리 권한은 부여하지 않는다. 전역 `manage all-resources`를 실습 역할에 부여하지 않는다.

## 실제 검증

[iam.txt](../evidence/iam.txt)는 사용자 API 키를 지정하지 않고 Instance Principal로 실행한 결과다.

| 검증 | 결과 |
|---|---|
| `network subnet get` | 성공 |
| `network nsg rules list` | 성공 |
| `network nsg rules update` | 기존 HTTP 규칙을 같은 값으로 갱신 성공; 공개 범위 변화 없음 |
| `iam policy list` | `NotAuthorizedOrNotFound` 거부 |
| `bv volume list` | `NotAuthorizedOrNotFound` 거부 |

설정 전 Instance Principal은 네트워크 조회도 거부되었다. 계정 키 인증 성공과 역할의 최소권한 검증은 서로 다른 결과로 기록한다. 초기 리소스 생성·연결은 기존 사용자 인증으로 수행했고, 제한 역할은 이후 네트워크 조회·NSG 규칙 관리용이다.

## 초기 준비와 제한 역할 실습 기록

과제는 **IAM 사용자 또는 Role**을 허용하므로, 사용자 결정에 따라 별도 IAM 계정을 생성하지 않고 기존 `b6-1-ai-research` 역할을 사용한다. 이메일·콘솔 비밀번호·새 사용자 API 키가 필요하지 않다.

1. **초기 준비:** 기존 관리자 프로필 `B6_LAB`으로 네트워크 구성과 실습 Dynamic Group/Policy 생성을 수행했다. 이 이력을 제한 역할 수행으로 바꾸어 기록하지 않는다.
2. **제한 역할 실습:** ai-research에 SSH로 접속한 뒤 모든 OCI 명령에 `--auth instance_principal`을 명시한다. 네트워크 구성 조회, 기존 HTTP/HTTPS NSG 규칙 재적용, 전후 규칙 동일 여부 및 IAM/볼륨 조회 거부를 실제 검증한다. [별도 실행 증빙](../evidence/limited-role.json) 참고.
3. **실행 범위:** 해당 compartment의 네트워크 조회와 NSG 규칙 수정만 허용한다. 초기 리소스 생성·VNIC 연결·Security List 변경을 이 역할로 수행했다는 의미는 아니다. 서버 SSH/OS 권한과 OCI IAM 권한도 별개다.

이는 사용자와 합의한 **초기 구성 후 제한 역할로 실습** 방식의 기록이다. 원문을 초기 준비까지 관리자 사용 금지로 해석하면 그 부분은 대체한 진행 조건에 해당한다. 실습 역할 자체에는 관리자 권한을 부여하지 않았다.

새 계정 준비 중 생성했던 빈 그룹 `b6-1-operators`와 정책 `b6-1-operator-network`는 계정을 만들지 않기로 한 사용자 결정에 따라 제거했다. 새 사용자·키는 생성하지 않았으며 기존 역할·서비스는 유지한다.

2026-09-27 01:53~01:54 KST 재검증 결과:

| 수행 항목 | 결과 |
|---|---|
| VCN/Subnet/VNIC/Route Table/IGW/Security List/NSG 조회 | 제한 역할로 모두 성공 |
| NSG HTTP80·HTTPS443 규칙 재적용 | 제한 역할의 UpdateNetworkSecurityGroupSecurityRules 성공 |
| 적용 전후 NSG 규칙 비교 | 두 규칙의 전체 조회 결과 동일, 접근 범위 변화 없음 |
| IAM 정책·Block Volume 목록 조회 | 각각 `NotAuthorizedOrNotFound` 거부 |
| 별도 계정 준비 리소스 정리 | 임시 그룹·정책 부재 및 기존 사용자 1명만 존재 확인 |
| 외부 HTTP/HTTPS·기존 서비스 | 모두 정상, 기존 컨테이너 ID·시작 시각 동일 |

외부 접속과 기존 서비스 보존 근거: [preservation-after-role.txt](../evidence/preservation-after-role.txt).

## 권한과 네트워크의 차이

웹 요청 허용 여부는 NSG/Security List/UFW가 판단한다. IAM permission이 있어도 네트워크 80번이 닫혀 있으면 HTTP 접속은 실패하며, 웹 페이지가 열려 있어도 OCI API 권한이 생기지는 않는다.

원복 시 `b6-1-network-lab` 정책을 먼저 제거하고, 다른 정책의 참조가 없는지 확인한 뒤 해당 Dynamic Group을 제거한다. 서비스 유지 중에는 삭제하지 않는다.

참고: [OCI Dynamic Group matching rule](https://docs.oracle.com/en-us/iaas/Content/Identity/dynamicgroups/Writing_Matching_Rules_to_Define_Dynamic_Groups.htm), [OCI API별 permission](https://docs.oracle.com/en-us/iaas/Content/Identity/policyreference/corepolicyreference_topic-Permissions_Required_for_Each_API_Operation.htm).
