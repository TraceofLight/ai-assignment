# 충돌 해결 기록
실행일: 2026-10-09. 커밋 메타데이터의 기준일과 구분한다.

## 비자명 충돌 판단과 선택 기준
같은 파일의 같은 hunk를 서로 다르게 수정하거나, 이동/삭제와 내용 변경이 겹치면 비자명 충돌로 분류한다.
마커 탐지는 충돌 위치만 알려 준다. 어떤 의미를 보존할지는 아래 기준으로 판단한다.

- 서로 다른 팀원 링크처럼 독립된 목적은 둘 다 보존하되 중복 HTML 구조는 한 번만 둔다.
- title/h1처럼 하나의 값을 요구하는 필드는 두 값을 붙여 넣지 않는다. 두 변경의 목적을 비교해 하나의 표현으로 통합한다.
- 삭제 이유·새 경로·요구사항 우선순위가 불명확하면 담당자에게 PR에서 문의하고 해결을 보류한다.
- 자동 병합 성공도 의미 보존을 보장하지 않는다. [협업 규칙](CONTRIBUTING.md)의 담당자 확인·검증·기록 절차를 따른다.

## 1. 동일 hunk 수정 충돌
- 역할: chanpago(탐색), nansu0425(협업 안내)
- 공통 기준: 61a9d66. 작업 HEAD: a8d017c. 통합 HEAD: 28b64a4.
- 명령: `git switch feature/chanpago-team-navigation` → `git merge b2-2 --no-commit`
- 결과: README.md와 src/index.html에서 content 충돌, 종료 코드 1.
- [충돌 원본](../evidence/conflict-1.txt)
- 해결: 두 팀원 소개 링크를 모두 보존하고 소개 문장은 두 목적을 한 문장으로 통합.
- 검증: 로컬 링크 검사와 기존 유틸 테스트 4건 통과.
- 관련 PR: [#6](https://github.com/TraceofLight/ai-assignment/pull/6)
- 재현: 별도 임시 clone에서 a8d017c를 checkout하고 28b64a4를 merge하면 동일 충돌 발생.
- 예방: 목록의 인접 행이나 같은 소개 문장을 바꾸기 전에 작업 범위를 공유하고 최신 통합 브랜치를 확인.
- 해결 커밋: 4ca64953e8f2d492c173f6de0fc98597b648fb01

비자명 판단: README의 인접한 팀원 행과 HTML summary/목록이 같은 hunk에서 서로 다르게 수정됐다.
ours만 고르면 nansu0425 링크가, theirs만 고르면 chanpago 링크가 빠진다.
목록 전체를 단순 중복 보존하면 TraceofLight 항목과 HTML 구조가 중복된다.
따라서 세 팀원 링크를 한 목록에 유지하고, summary에 소개 탐색과 이슈/PR 검토 목적을 함께 담았다.
[검토 근거](https://github.com/TraceofLight/ai-assignment/pull/6#issuecomment-6080594672)와 충돌 원본으로 선택 이유를 추적한다.

## 2. HTML 제목과 헤딩의 동일 hunk 충돌
- 역할: chanpago(제출 기록), nansu0425(학습 안내)
- 공통 기준: 376988b. 작업 HEAD: e4aeb1d. 통합 HEAD: 48dcae8.
- 명령: `git switch feature/chanpago-submission-audit` → `git merge b2-2 --no-commit`
- 결과: src/index.html의 title과 h1 주변에서 content 충돌, 종료 코드 1.
- [충돌 원본](../evidence/conflict-2.txt)
- 해결: 제목과 h1을 모두 'Codyssey · 팀 소개와 Git 협업 기록'으로 통일하고 학습 기록 링크 보존.
- 관련 PR: [#12](https://github.com/TraceofLight/ai-assignment/pull/12)
- 재현: 별도 임시 clone에서 e4aeb1d를 checkout하고 48dcae8을 merge.
- 예방: 같은 제목을 여러 브랜치에서 변경할 때는 통합 문구를 먼저 합의.
- 해결 커밋: 63c81ef87dfc27a70499d45c6aa6a9502241da67

비자명 판단: 양쪽이 title과 h1의 같은 hunk에 서로 다른 단일 제목을 제안했다.
한쪽만 선택하면 다른 쪽의 팀 소개 또는 협업 실습 목적이 약해지고, 둘 다 붙이면 title/h1이 중복된다.
따라서 '팀 소개와 Git 협업 기록'으로 목적을 합치고 title과 h1을 일치시켰다.
이는 마커만 지우는 처리가 아니라 제목의 의미·HTML 구조를 함께 판단한 해결이다.

## 현재 SHA로 재현
위 SHA는 최초 실행 당시 기록이다. 현재 이력은 [SHA 대응표](../evidence/commit-id-map.md)를 따른다.
아래 명령은 worktree를 바꾸지 않고 현재 커밋 객체로 충돌을 재검증한다.
각 명령의 종료 코드 1과 CONFLICT 출력이 예상 결과다.

```powershell
git fetch origin b2-2
git merge-tree --write-tree --name-only 67fbef2ec01c78d873f87098de309e613bb4669a 3003877655aad99e11eacfa05f5e69bde74ef2b1
git merge-tree --write-tree --name-only 2b163821103086c911189cf5a4b3f66fe3a355d1 5ca65c7e411368914c13643c271b0c411b5c092c
```

2026-10-09 재검증에서 첫 명령은 README.md와 src/index.html, 둘째는 src/index.html의 content 충돌을 확인했다.
현재 해결 커밋:
[1차 6583a45](https://github.com/TraceofLight/ai-assignment/commit/6583a45124d81cf64a733233ede7fd04095e1599),
[2차 9b8df0d](https://github.com/TraceofLight/ai-assignment/commit/9b8df0d2b7039689178089374170787cb5b17af6).
