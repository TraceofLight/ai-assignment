# 모니터링·확장·비용 대응 계획

현재 실습은 공유 자원을 재사용하는 단일 컨테이너 구성이다. 추가 인스턴스·로드밸런서 생성, 자동 확장, 예산 경보 설정은 **수행하지 않았다**. 아래 기준은 향후 운영 계획이며 관측값에 따라 조정할 초기 기준이다.

## 관측 지표와 대응 기준

운영 시에는 1분 간격으로 수집하고 5분 창으로 판단한다. 24시간 정상 기준선을 확보한 뒤 임계값을 조정한다. 응답시간·오류율은 외부 요청 및 웹 로그에서, 호스트 지표는 OCI Monitoring과 컨테이너 지표를 함께 확인한다.

| 지표 | 초기 경보 기준 | 먼저 확인할 사항 |
|---|---|---|
| `/health` 응답 | 연속 3회 실패 | 프로세스·리슨·방화벽·DNS/TLS 순서로 장애 확인 |
| 요청 p95 응답시간 | 500ms 초과가 10분 지속 | DNS/TLS·외부망 지연과 서버 처리 지연 구분 |
| HTTP5xx 비율 | 5분간 요청 100건 이상에서 1% 초과 | 웹 로그·백엔드 오류 확인; 저트래픽은 개별 실패 확인 |
| CPU | 호스트 CPU 70% 초과가 10분 지속 | 실습 컨테이너 사용량·CPU 제한 및 호스트 부하 비교 |
| 메모리 | 컨테이너 한도의 80% 초과가 10분 지속 또는 OOM 발생 | 누수·동시 처리량·컨테이너 제한 확인 |
| 네트워크 | 허용 대역폭의 70% 초과가 10분 지속 또는 드롭 증가 | 요청량·응답 크기·전송량 및 제한 확인 |

수치는 실측 장애 한계가 아니라 제안값이다. 공유 호스트 전체 CPU 상승만으로 실습 서비스의 병목이라고 단정하지 않는다. `docker stats --no-stream b6-1-cloud-lab`과 로그로 귀속을 확인하며 다른 서비스를 수정하지 않는다.

OCI의 `oci_computeagent`에서 `CpuUtilization`, `MemoryUtilization`, `NetworksBytesIn/Out`을 확인할 수 있다. 누적 네트워크 바이트는 구간 차이를 시간으로 나누어 전송률로 계산하고 재시작에 의한 카운터 초기화를 처리한다. 지표가 없으면 Oracle Cloud Agent의 Monitoring 플러그인·접근 경로를 운영 규약에 따라 점검한다. [Compute 지표](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computemetrics.htm).

공개 증빙에는 집계값만 저장하고 실제 리소스 식별자·전체 서버 현황을 제외한다. [단기 HTTPS 표본](../evidence/health-sample.json)은 현재 응답 확인 자료이며 부하 테스트나 상시 모니터링 구축 증빙은 아니다. CPU·메모리·비용을 이 표본으로 검증했다고 주장하지 않는다. 2026-09-27 UTC 측정에서 20회 모두 HTTP200·본문 OK였으며, nearest-rank 기준 p50 27.93ms, p95 46.79ms였다. 연결·TLS 시간을 포함한 클라이언트 관측값이다.

## 병목 확인 후 확장 판단

1. 10분 이상 지연이 지속되면 요청 증가와 컨테이너 자원 사용이 함께 상승하는지 확인한다. 네트워크 설정 오류나 인증서 오류는 확장으로 해결하지 않는다.
2. 정적 파일 크기·캐시·압축·로그 양 등을 먼저 검토하고 동일 조건에서 다시 측정한다. 공유 인스턴스의 크기나 기존 서비스 제한은 임의로 변경하지 않는다.
3. 최적화 후에도 지연과 CPU/네트워크 포화가 반복되거나, 유지보수 중 가용성 요구가 생기면 **OCI Load Balancer + 독립된 백엔드 2대 이상**을 검토한다. AWS ALB의 HTTP 계층 부하 분산에 대응하는 구성이다. 백엔드 한 대에 LB만 추가하면 컴퓨팅 병목이나 단일 장애점이 해결되지 않는다.
4. 도입 전에 리전·shape·대역폭·백엔드 수·볼륨·로그·전송량의 무료 한도와 예상 월 비용을 확인한다. 무료 범위를 넘는 변경은 운영 규약의 예산 승인 후에만 진행한다. 자동 확장은 현재 비활성 계획이다.

도입안: `인터넷 → HTTPS Load Balancer → 서로 다른 장애 영역의 백엔드 → Caddy`. 백엔드는 사설 주소로 연결하고 웹 포트의 소스를 LB의 NSG로 제한한다. TLS 종료 위치·백엔드 암호화와 인증서 갱신 주체를 사전에 정한다.

헬스체크 초기안은 `/health`, 기대 코드200, 응답 `OK`, 간격10초·timeout3초·재시도3회다. 실제 서비스 지원 범위와 애플리케이션 특성에 맞춰 적용한다. DNS 전환 전에 각 백엔드와 LB 경유 응답을 확인하고, 전환 후 30분간 오류율·지연을 비교한다. 실패하면 이전 DNS 대상으로 복구하고 새 구성만 분리한다. DNS TTL 때문에 즉시 전환 완료를 가정하지 않는다.

LB 도입 후에는 `unhealthyBackendServers`, `backendTimeouts`, `httpResponses5xx`, `responseTimeHttpHeader`도 확인한다. 마지막 지표는 평균이므로 외부 요청 p95와 혼동하지 않는다. [Load Balancer 지표](https://docs.oracle.com/en-us/iaas/Content/Balance/Reference/loadbalancermetrics.htm).

## 태그와 비용 추적

현재 실습 식별자는 `assignment=b6-1`이다. 다음은 확장 리소스에 적용할 표준 예시이며, `owner`·`purpose` 및 Defined Tag가 이미 적용됐다는 의미는 아니다.

| 구분 | 예시 | 용도 |
|---|---|---|
| Docker label / OCI Free-form Tag | `assignment=b6-1` | 실습 리소스 검색·정리 |
| OCI Defined Tag | `Lab.assignment=b6-1` | 비용·예산의 실습 범위 필터 |
| OCI Defined Tag | `Lab.owner=lab-operator` | 담당 역할 식별; 개인 이름·이메일 제외 |
| OCI Defined Tag | `Lab.purpose=web-lab` | 용도 분류 |

Docker label은 OCI 청구 태그가 아니다. 비용 추적용으로는 운영 담당자가 승인한 Defined Tag namespace를 사용한다. 공유 호스트 전체 비용을 태그 하나로 이 컨테이너에 정확히 배분할 수 없으므로, 공유 비용과 실습 전용 추가 비용을 분리한다. [OCI 태그](https://docs.oracle.com/en-us/iaas/Content/Tagging/Concepts/taggingoverview.htm).

운영 담당자는 다음 순서로 비용을 추적한다.

1. Cost Analysis에서 당월·일별 집계와 실습 compartment를 선택하고 `Lab.assignment=b6-1`로 필터링한다. Service/SKU별로 Compute·Volume·LB·네트워크 전송·Logging 항목을 비교한다.
2. 태그 없는 비용이 빠지지 않도록 compartment 전체 조회와 대조한다. 태그 변경 전 비용과 공유 자원은 별도로 확인하고 일별 사용량·비용 차이·월말 예측을 기록한다. 비용 데이터의 수집 지연을 고려한다.
3. 무료 범위 유지 중에는 매일 추가 청구 발생 여부를 확인한다. 추가 청구가 있으면 신규 확장을 보류하고 원인이 된 SKU와 실습 전용 자원을 확인한다.
4. 유료 확장이 승인되면 월 예산 `B > 0`에 대해 실제 사용액 50%·80%·100%, 예상 사용액100%의 Budget 경보를 설정한다. 태그 또는 compartment 범위를 지정하고 담당자 수신을 검증한다. 실제 승인 금액·수신처는 공개 문서에 넣지 않는다.

Budgets는 비용을 강제로 막는 한도가 아니며 경보 평가도 실시간이 아니다. 경보만 믿고 비용 증가를 방치하지 않는다. [Cost Analysis](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm), [Budgets](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm).

| 상황 | 대응 |
|---|---|
| 50% 도달 | 현재 사용량과 월말 예상액 확인 |
| 80% 도달 또는 월말 초과 예상 | 확장 보류, LB 대역폭·전송·로그·유휴 실습 자원 확인 |
| 100% 도달 또는 예상 밖 추가 청구 | 운영 담당자에게 보고, 승인된 범위에서 실습 신규 자원만 축소·정리 |

공유 인스턴스를 자동 종료하거나 기존 서비스를 삭제하지 않는다. 조치 후 비용 반영을 다시 확인하고 [정리 체크리스트](cleanup-checklist.md)에 실제 처리 결과를 기록한다.

월 추가 비용 추정은 `Compute 시간 + 볼륨 GB·월 + LB 기본/대역폭 + 과금 대상 전송량 + 로그/모니터링 사용량`으로 작성한다. 적용 시점의 요율·무료 잔여량·세금을 반영하고, 태그별 비용 조회 결과와 비교한다. **현재 무과금 여부에 대한 Billing 감사나 예산 경보 구축은 수행하지 않았다.**
