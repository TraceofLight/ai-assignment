# 협업 규칙

## 저장소와 브랜치
옵션 B: 개인 저장소와 collaborator 방식이다. 과제 통합 대상은 `b2-2`이며 main 역할을 맡는다.
현재 기본 브랜치는 `b2-2`다. 다른 과제 브랜치와 `main`에 이번 변경을 섞지 않는다.
실제 권한·보호 설정과 수행 확인은 [평가 보완 기록](evaluation-follow-up.md)에서 구분한다.

- 일반 작업: `feature/<계정>-<작업>`, 예: `feature/traceoflight-evaluation-policy`.
- 긴급 수정: `hotfix/<계정>-<문제>`, 예: `hotfix/traceoflight-broken-link`.
- 계정·작업은 소문자 영문, 숫자, 하이픈 사용. 공백·한글·`temp`·`final` 같은 목적 불명 이름 금지.
- 통합 브랜치의 직접 push 대신 PR 사용. 공유 이력의 무합의 force-push/reset/rebase 금지.
- 작업 브랜치에서 `git fetch origin` 후 `git merge origin/b2-2`로 최신 변경 반영.
- 충돌 해결·리뷰 반영 후 링크 검사와 전체 테스트 재실행.

## 작업 경계
아래는 역할별 작업 경계다. GitHub 권한 부여 또는 독립 승인 기록을 대신하지 않는다.

| 역할 | 담당 영역 | 겹치는 변경의 확인 대상 |
| --- | --- | --- |
| TraceofLight | README, 제출 인덱스, scripts, tests, 통합 검증 | 소개·탐색 담당 역할 |
| nansu0425 | team/nansu0425.md, 협업 규칙, 학습 안내 | chanpago의 HTML·제목 변경 |
| chanpago | team/chanpago.md, HTML 탐색·제목, 충돌 기록 | nansu0425의 소개·학습 안내 |

공용 HTML·문서 수정 전 이슈에 파일/영역·담당자·예상 충돌을 기록한다.
같은 영역을 이미 수정 중이면 관련 PR에 작업 순서를 합의한 뒤 진행한다.

## 커밋과 공유 이력
형식은 `type(module): English description`이다.
feat, fix, docs, test, chore 등을 사용하고 module에는 변경 대상을 적는다.
`update`, `temp`, `wip`, `final`, `bug fix`처럼 대상·효과를 알 수 없는 메시지는 금지한다.
여러 파일을 바꾸거나 판단 근거가 필요하면 작업 의도와 세부 사항을 한국어 개조식으로 기록한다.

잘못된 메시지를 발견했을 때:
1. 로컬·원격 로그를 비교하여 아직 push하지 않은 개인 커밋인지 확인한다.
2. 미공유 최신 커밋이면 `git diff --cached`로 불필요한 staged 변경이 없는지 확인한 뒤 `git commit --amend -m "docs(collaboration): clarify merge checks"`로 수정한다.
3. 미공유 커밋 경계만 정리할 때는 `git reset --soft HEAD~1`, `git diff --cached`, 재커밋 순서로 변경을 보존한다.
4. 이미 공유했다면 메시지 때문에 이력을 재작성하지 않는다. PR 설명을 보완하고, 잘못된 내용은 후속 수정 또는 revert 커밋으로 바로잡는다.

공유 커밋 수정은 관련 이슈에 대상 SHA·이유·영향·복구 방법을 적고 영향을 받는 작업자의 명시적 답변을 받은 뒤 진행한다.
응답 부재는 동의가 아니다. 합의가 없으면 기존 이력을 보존한다.
rebase 실습과 CODEOWNERS는 이번 보너스 범위에서 제외한다.
상세 실행 기록은 [트러블슈팅](troubleshooting-log.md)을 따른다.

## 이슈와 PR
각 작업의 이슈를 먼저 만든다. PR 제목은 `(계정): 변경 내용`이다.
[PR 템플릿](../.github/PULL_REQUEST_TEMPLATE.md)에 What, Why, How 및 `Closes #번호`를 작성한다.
제목의 역할 이름과 GitHub가 표시하는 실제 작성 계정을 구분한다.

- base를 `b2-2`로 확인한다.
- 기본 브랜치 대상 PR의 종료 키워드를 사용하되, 병합 후 이슈 상태를 반드시 확인한다.
- 기존 수동 종료 이슈는 [API 증빙](../evidence/evaluation-github.json)의 closed_events로 확인한다.
- 자동 종료되지 않으면 병합 링크·검증 결과를 댓글에 남긴 후 수동 종료한다.
- 구성원별 PR 2개, 다른 사람 PR 리뷰 2회, 본인 PR 리뷰 반영 1회가 과제 기준이다. 역할별 분류와 실제 계정별 달성 여부는 별개로 확인한다.

## 실질 리뷰와 승인
**LGTM/좋아요만 남기는 리뷰는 금지한다.** 파일 또는 라인, 문제·위험, 제안 또는 질문을 포함한다.
예: "`src/index.html`의 팀 목록에서 한쪽 변경만 선택하면 다른 팀원 링크가 사라집니다. 두 링크를 유지하고 링크 검사를 다시 실행해 주세요."
작성자는 수정 SHA·검증 결과로 답하거나, 미반영 이유를 근거와 함께 답한다.

[실제 코멘트](https://github.com/TraceofLight/ai-assignment/pull/2#issuecomment-6080564200)와
[반영 답글](https://github.com/TraceofLight/ai-assignment/pull/2#issuecomment-6080570142)은 파일·문제·수정 결과를 연결한 예다.
이 댓글의 실제 작성 계정은 TraceofLight이며, 독립된 approve로 계산하지 않는다.

승인자는 PR 작성자가 아닌 write 이상 권한 보유자여야 한다.
검토 대상은 최종 diff, 실행 결과, 이슈 범위, 충돌 해결의 의미 보존이다.
검토자는 확인한 SHA와 근거를 남기고 GitHub의 Approve를 사용한다.
변경이 추가되면 변경된 부분을 재검토하고 최신 SHA에 대해 다시 승인한다.
승인할 사람이 없으면 승인 요건 충족으로 표시하지 않는다.

병합 전 체크리스트:
- [ ] What/Why/How와 연결 이슈, 담당 범위 확인
- [ ] 실질 코멘트 1개 이상과 작성자의 응답·반영 확인
- [ ] 독립 승인 1회 이상과 승인 대상 SHA 확인
- [ ] 미해결 의견·충돌 없음
- [ ] 링크 검사·전체 테스트·diff 검사 성공
- [ ] 아래 배포 준비 확인 및 검증 결과 PR 기록

이 목록은 운영 기준이다. 과거 PR의 승인 여부는 [실제 스냅샷](../evidence/evaluation-github.json)으로 별도 판정한다.

## 충돌 대응
1. `git status`와 양쪽 SHA를 확인하고 관련 PR에 충돌 파일·담당자·원인을 공유한다.
2. 작성자가 해결을 담당하고, 겹치는 영역 담당자에게 선택 이유를 확인받는다. 응답이 없고 의도가 불명확하면 병합을 보류한다.
3. [비자명 충돌 판단 기준](conflict-resolution.md)에 따라 양쪽 변경을 비교한다.
4. 마커 제거뿐 아니라 링크·제목·문장 의미 보존을 확인하고 전체 검증을 다시 실행한다.
5. 기록에 양쪽 SHA, 명령, 원본, 선택 이유, 결과 SHA와 PR 링크를 남긴다.

## 핫픽스와 배포 준비
핫픽스도 PR·독립 승인 절차를 생략하지 않는다. 실제 긴급 장애 증빙이 아닌 운영 절차다.

1. 이슈에 영향·재현·복구 기준을 적고 담당자와 검토자를 정한다.
2. 최신 `origin/b2-2`에서 `hotfix/<계정>-<문제>`를 만들고 최소 변경만 적용한다.
3. 회귀 검증 후 PR을 열어 긴급 사유·What/Why/How·`Closes`를 작성한다.
4. 우선 검토를 요청하되, 실질 코멘트·응답·승인 1회와 미해결 의견 해소를 확인한다.
5. 병합 SHA로 아래 배포 준비를 재확인한다. 이 결과물은 정적 파일이며 별도 운영 배포 환경은 없다.
6. `src/index.html`을 열어 제목·팀원 링크·문서 탐색을 확인하고 이슈에 완료 결과를 남긴다. 장애가 남으면 공유 이력을 reset하지 않고 revert PR로 복구한다.

배포 준비 기준:
- [ ] Python 3.10 이상에서 `python scripts/run.py` 성공
- [ ] `python -m unittest discover -s tests` 성공
- [ ] `git diff --check` 성공
- [ ] HTML 제목·팀원 3명·필수 문서 링크 존재, 충돌 마커 없음
- [ ] 대상 SHA와 실행 출력 기록, 외부 배포 여부를 과장하지 않음
