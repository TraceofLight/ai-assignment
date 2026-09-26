# 제출 인덱스
저장소: https://github.com/TraceofLight/ai-assignment/tree/b2-2

## 팀과 결과물
- 역할 이름: TraceofLight, nansu(nansu0425), chanpago
- 선택 결과물: (B) 팀 소개. [텍스트 HTML](src/index.html)과 [TraceofLight](team/traceoflight.md), [nansu0425](team/nansu0425.md), [chanpago](team/chanpago.md) 소개 문서.
- 통합 브랜치: b2-2. 작업 브랜치: feature/<계정>-<작업>.
- PR 제목의 계정별로 작업을 구분한다. 실제 GitHub 작성자·검토 계정은 각 링크에서 확인한다.

## 역할별 Issue / PR
| 역할 | 작업 | Issue | PR |
| --- | --- | --- | --- |
| TraceofLight | 팀 소개 HTML과 제출 구조 구성 | [#1](https://github.com/TraceofLight/ai-assignment/issues/1) | [#2](https://github.com/TraceofLight/ai-assignment/pull/2) |
| nansu0425 | 팀 소개와 브랜치 협업 안내 추가 | [#3](https://github.com/TraceofLight/ai-assignment/issues/3) | [#5](https://github.com/TraceofLight/ai-assignment/pull/5) |
| chanpago | 팀 소개와 HTML 탐색 구조 보강 | [#4](https://github.com/TraceofLight/ai-assignment/issues/4) | [#6](https://github.com/TraceofLight/ai-assignment/pull/6) |
| TraceofLight | Git 트러블슈팅 네 가지 실습과 기록 | [#7](https://github.com/TraceofLight/ai-assignment/issues/7) | [#8](https://github.com/TraceofLight/ai-assignment/pull/8) |
| nansu0425 | 페이지 제목과 학습 안내 정리 | [#9](https://github.com/TraceofLight/ai-assignment/issues/9) | [#11](https://github.com/TraceofLight/ai-assignment/pull/11) |
| chanpago | 충돌 재검증과 제출 인덱스 완성 | [#10](https://github.com/TraceofLight/ai-assignment/issues/10) | [#12](https://github.com/TraceofLight/ai-assignment/pull/12) |

## 검토 항목과 반영
아래는 댓글에 표시한 검토 역할별 인덱스다. 독립된 계정의 승인 횟수를 의미하지 않는다.
| 역할 | 다른 역할의 PR 검토 항목 | 수정 후 답글 |
| --- | --- | --- |
| TraceofLight | [검토 1](https://github.com/TraceofLight/ai-assignment/pull/5#issuecomment-6080584031), [검토 2](https://github.com/TraceofLight/ai-assignment/pull/6#issuecomment-6080594672), [검토 3](https://github.com/TraceofLight/ai-assignment/pull/11#issuecomment-6080656117) | [반영 1](https://github.com/TraceofLight/ai-assignment/pull/2#issuecomment-6080570142), [반영 2](https://github.com/TraceofLight/ai-assignment/pull/8#issuecomment-6080650085) |
| nansu0425 | [검토 1](https://github.com/TraceofLight/ai-assignment/pull/2#issuecomment-6080564200), [검토 2](https://github.com/TraceofLight/ai-assignment/pull/6#issuecomment-6080595246), [검토 3](https://github.com/TraceofLight/ai-assignment/pull/8#issuecomment-6080635682), [검토 4](https://github.com/TraceofLight/ai-assignment/pull/12#issuecomment-6080660097) | [반영 1](https://github.com/TraceofLight/ai-assignment/pull/5#issuecomment-6080592027), [반영 2](https://github.com/TraceofLight/ai-assignment/pull/11#issuecomment-6080657467) |
| chanpago | [검토 1](https://github.com/TraceofLight/ai-assignment/pull/2#issuecomment-6080564679), [검토 2](https://github.com/TraceofLight/ai-assignment/pull/5#issuecomment-6080584544), [검토 3](https://github.com/TraceofLight/ai-assignment/pull/8#issuecomment-6080636219) | [반영 1](https://github.com/TraceofLight/ai-assignment/pull/6#issuecomment-6080609708), [반영 2](https://github.com/TraceofLight/ai-assignment/pull/12#issuecomment-6080670388) |

## 필수 문서와 증빙
- [협업 규칙](docs/CONTRIBUTING.md)
- [충돌 해결 2회](docs/conflict-resolution.md): [첫 번째 원본](evidence/conflict-1.txt), [두 번째 원본](evidence/conflict-2.txt)
- [Git 트러블슈팅 4종](docs/troubleshooting-log.md): [실습 메모](docs/git-practice.md), [명령 실행 출력](evidence/git-practice.txt)
- [Git 그래프](evidence/git-log-graph.txt), [커밋 시간 흐름](evidence/commit-timeline.txt)
- [검증 출력](evidence/validation.txt), [증빙 범위](evidence/README.md)
- [작성자 계정 확인](evidence/author-mapping.md)

## 검증과 적용 범위
| 항목 | 결과 |
| --- | --- |
| 팀 소개 문서 및 HTML | 세 역할의 소개와 링크 구성 |
| 역할별 PR | 각 2개, 총 6개 |
| 검토와 반영 | 위 댓글 및 수정 커밋으로 연결 |
| 충돌 | 동일 hunk 충돌 2회 실제 실행 |
| Git 실습 | amend, reset --soft, 원격 push 후 revert, stash/pop |
| 로컬 검증 | 링크 검사, 테스트 7건 |
| 통합 대상 | 과제 브랜치 b2-2 사용 |
| 독립 계정의 approve / main 보호 규칙 | 이 작업에서 충족한 것으로 표시하지 않음 |
| 보너스 | 제외 |

Git 커밋 메타데이터 기준일은 2026-09-26이며, GitHub 이슈·PR·댓글 및 검증 실행일은 2026-10-09다.
증빙 스냅샷은 해당 파일에 기재한 SHA까지의 상태다. 최종 병합 상태는 위 PR 링크와 b2-2에서 확인한다.
