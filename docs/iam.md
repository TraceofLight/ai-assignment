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

## 권한과 네트워크의 차이

웹 요청 허용 여부는 NSG/Security List/UFW가 판단한다. IAM permission이 있어도 네트워크 80번이 닫혀 있으면 HTTP 접속은 실패하며, 웹 페이지가 열려 있어도 OCI API 권한이 생기지는 않는다.

원복 시 `b6-1-network-lab` 정책을 먼저 제거하고, 다른 정책의 참조가 없는지 확인한 뒤 해당 Dynamic Group을 제거한다. 서비스 유지 중에는 삭제하지 않는다.

참고: [OCI Dynamic Group matching rule](https://docs.oracle.com/en-us/iaas/Content/Identity/dynamicgroups/Writing_Matching_Rules_to_Define_Dynamic_Groups.htm), [OCI API별 permission](https://docs.oracle.com/en-us/iaas/Content/Identity/policyreference/corepolicyreference_topic-Permissions_Required_for_Each_API_Operation.htm).
