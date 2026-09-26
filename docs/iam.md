# 최소권한 IAM

초기 인프라와 역할 준비 후, 실습 API 작업은 Instance Principal의 제한 역할로 수행했다. 역할은 실습 대상 인스턴스 한 대에 매칭하며, 관리자 권한을 부여하지 않았다. OCI API 인증 자료는 웹 컨테이너에 전달하지 않는다.

```text
Allow dynamic-group id <DYNAMIC_GROUP_OCID> to {
  VCN_READ, SUBNET_READ, VNIC_READ, ROUTE_TABLE_READ,
  INTERNET_GATEWAY_READ, SECURITY_LIST_READ,
  NETWORK_SECURITY_GROUP_READ, NETWORK_SECURITY_GROUP_LIST_SECURITY_RULES,
  NETWORK_SECURITY_GROUP_UPDATE_SECURITY_RULES
} in compartment id <COMPARTMENT_OCID>
```

네트워크 조회 8개와 NSG 규칙 수정 1개 permission만 허용한다. 수정 범위는 해당 compartment의 NSG이며 특정 NSG 한 개만으로 제한된 정책은 아니다. VM 생성·종료·크기 변경, 볼륨, Object Storage, DB, IAM 관리 권한은 부여하지 않는다.

| 실제 실습 | 결과 |
|---|---|
| Subnet / NSG 규칙 조회 | 성공 |
| 기존 NSG HTTP 규칙 재적용 | 성공, 접근 범위 변화 없음 |
| IAM 정책 목록 / Block Volume 목록 조회 | `NotAuthorizedOrNotFound` 거부 |

[실행 증빙](../evidence/iam.txt). 초기 생성·연결 작업과 이후 제한 역할의 검증 범위를 구분한다. 이후 검증은 `oci --auth instance_principal ...`로 실행했다.

네트워크 규칙은 패킷 접근을, IAM은 리소스 API 작업을 제어한다. IAM 권한이 있어도 HTTP 포트가 막히면 웹 접속은 실패하고, 웹에 접속할 수 있어도 OCI 리소스 변경 권한이 생기지 않는다.

[추가 역할 검증](../evidence/limited-role.json)
