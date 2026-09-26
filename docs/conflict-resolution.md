# 충돌 해결 기록
실행일: 2026-10-09. 커밋 메타데이터의 기준일과 구분한다.

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
