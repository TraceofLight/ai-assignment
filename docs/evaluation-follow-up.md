# 평가 피드백 보완

보완일: 2026-10-09. 후속 작업 작성자: TraceofLight.
[Issue #15](https://github.com/TraceofLight/ai-assignment/issues/15)의 문서·증빙 보완 범위다.
기존 실습 커밋의 날짜·역할과 이번 보완 커밋의 실제 작성 일자를 구분한다.

## 권한·보호와 수행 이력
- 옵션 B(개인 저장소 + collaborator) 방식으로 과제를 구성했다.
- 저장소 소유자는 작업 중 권한·보호 설정 작업을 수행했다고 확인했다. 이는 소유자 확인 이력이며, 과거 설정 시각·초대 수락·개별 승인 로그의 API 증빙과는 구분한다.
- 2026-10-09 API 스냅샷에서 TraceofLight의 admin/maintain/push 권한과 기본 브랜치 `b2-2`를 확인했다.
- `main` 보호 설정은 PR 승인 최소 1회, 관리자 적용, 대화 해결 필수, force-push·삭제 불허다.
- 이 설정 스냅샷의 대상은 `main`이다. 과제 통합 브랜치 `b2-2`의 과거 설정 또는 당시 모든 PR의 승인까지 증명하지 않는다.
- 이번 보완에서는 collaborator 초대 및 보호 규칙을 변경하지 않았다.

[GitHub API 스냅샷](../evidence/evaluation-github.json)의 `captured_at`은 UTC다.
`collaborators`, `main_protection`, `pull_requests`, `issues`, `comment_examples`에 실제 조회값을 담았다.
PR #2/#5/#6/#8/#11/#12/#14는 모두 병합 상태다. 각 PR의 `reviews` 배열은 비어 있어 독립 approve 증빙으로 제출할 수 없다.
제목의 역할별 2개 PR 분류와 실제 GitHub 생성 계정의 참여 증빙은 구분한다.

재조회 명령:
```powershell
gh api repos/TraceofLight/ai-assignment/collaborators
gh api repos/TraceofLight/ai-assignment/branches/main/protection
gh api repos/TraceofLight/ai-assignment/pulls/2
gh api repos/TraceofLight/ai-assignment/pulls/2/reviews
gh api repos/TraceofLight/ai-assignment/issues/1/events
```

## 운영 기록 문구 양식
아래는 설정·검토 작업 후 남길 문구의 예다. 꺾쇠 부분에 실제 값과 근거 링크를 채운다.

- 권한: "협업 계정 <계정>을 collaborator로 초대하고, 수락 후 write 권한을 확인했다. 근거: <권한 증빙>."
- 보호: "<대상 브랜치>에 PR 필수·승인 1회·관리자 적용 규칙을 설정했다. 확인 시각: <시각>, 근거: <설정 증빙>."
- 실질 리뷰: "<파일:라인>의 <위험>을 확인했다. <수정안>을 적용하고 <검증 명령> 결과를 남겨 달라."
- 반영: "<수정 SHA>에서 <변경>을 반영하고 <검증>을 통과했다. 원래 질문: <댓글 링크>."
- 승인: "<작성자와 다른 검토자>가 <최종 SHA>의 변경과 검증을 확인하고 승인했다. 근거: <실제 Approve 링크>."
- 병합: "<PR>을 <통합 SHA>로 병합하고 <이슈>의 종료 및 배포 준비를 확인했다."

## 평가 항목별 반영
| 항목 | 보완 위치·근거 | 범위 |
| --- | --- | --- |
| 1 | 위 옵션 선택·소유자 확인, API collaborators | 과거 참여 권한의 별도 로그는 미확보 |
| 2 | API main_protection, 위 대상 브랜치 구분 | main 설정 확인, 과거 b2-2 적용 증빙과 구분 |
| 3, 10 | [PR 템플릿](../.github/PULL_REQUEST_TEMPLATE.md) | What/Why/How/Closes 및 검증·리뷰 체크 |
| 4, 5 | API pull_requests와 기존 [제출 인덱스](../SUBMISSION.md) | 병합 7건 확인, 독립 approve는 미확보 |
| 6, 12, 18 | [충돌 기록](conflict-resolution.md) | 동일 hunk 2건, 비자명 판단·선택 기준·담당자 흐름 |
| 7, 13 | [Git 실습](troubleshooting-log.md) | 현재 SHA와 명령·원격 적용 출력의 연결 |
| 8, 9 | [협업 규칙](CONTRIBUTING.md) | 상호 참조, 이름 예시·금지 이름 |
| 11 | 협업 규칙의 실질 리뷰, API comment_examples | LGTM만 금지, 파일·근거·제안과 반영 답글 |
| 14 | 협업 규칙의 배포 준비, 후속 PR 검증 결과 | 정적 파일 검증, 외부 배포 수행 주장은 제외 |
| 15 | 협업 규칙의 승인·병합 체크리스트 | 운영 기준 명문화, 과거 독립 승인과 구분 |
| 16 | API issues의 closed_events, 협업 규칙 | 실제 수동 종료 시각·계정, 현재 기본 브랜치 반영 |
| 17, 20 | 협업 규칙의 커밋과 공유 이력 | 미공유 amend/reset, 공유 후 수정·revert, 합의 절차 |
| 19 | 협업 규칙의 핫픽스 | 긴급 브랜치·우선 검토·승인·검증·복구 순서 |
| 21 | 협업 규칙의 작업 경계 | 파일/영역 담당과 충돌 사전 공유 |
| 22 | 협업 규칙의 보너스 범위 | rebase/CODEOWNERS 추가 실습 제외 |

[보완 검증 기록](../evidence/evaluation-validation.txt): 전체 문서 링크, 테스트 7건, 정적 HTML, 충돌 2건 재검증.

평가지의 번호가 비어 있는 핫픽스 항목을 순서에 따라 19번으로 표기했다.
정책 문서 보완과 실제 계정 참여·승인 요건의 충족은 같은 의미가 아니다.
