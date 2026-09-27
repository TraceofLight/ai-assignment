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

## 권한 부족 시 점진적 조정

다음은 후속 작업의 절차이며, 현재 권한을 추가로 확대한 기록은 아니다.

1. 실패한 API·시각·request ID를 기록하고 리전·대상·역할 매칭을 확인한다. `NotAuthorizedOrNotFound`는 잘못된 대상이나 리전에서도 발생할 수 있다.
2. 기존 권한 관리 담당자가 해당 작업에 필요한 permission과 compartment를 확인한다. 실습 역할 스스로 정책을 변경하지 않는다.
3. 예를 들어 조회만 필요하면 `NETWORK_SECURITY_GROUP_READ`와 `NETWORK_SECURITY_GROUP_LIST_SECURITY_RULES`로 시작한다. 실제 규칙 수정이 필요할 때만 `NETWORK_SECURITY_GROUP_UPDATE_SECURITY_RULES` 추가를 검토한다. `manage all-resources`로 우회하지 않는다.
4. 변경 사유·최소 범위·검토자·허용 기간·정책 전후 차이를 운영 기록에 남긴 후 적용한다. 공개 증빙에는 식별자를 제거한 작업명과 결과만 남긴다.
5. 필요한 작업 성공과 무관한 IAM/볼륨 작업 거부를 함께 재검증한다. 임시 권한은 작업 종료 후 회수하며, 예상치 못한 영향이 있으면 직전 정책으로 복구한다.

Monitoring·비용 조회가 필요해도 현재 웹 실습 역할에 일괄 추가하지 않는다. 운영 담당자의 기존 조회 권한을 사용하거나 별도 최소 범위를 검토한다. [API별 필요 권한](https://docs.oracle.com/en-us/iaas/Content/Identity/policyreference/corepolicyreference_topic-Permissions_Required_for_Each_API_Operation.htm).
