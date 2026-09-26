# Codyssey Git 협업 · 팀 소개
간단한 텍스트 HTML 페이지와 팀 소개 문서로 Git 협업 절차를 연습한다.

## 팀
| 역할 이름 | GitHub | 소개 |
| --- | --- | --- |
| TraceofLight | [TraceofLight](https://github.com/TraceofLight) | [소개](team/traceoflight.md) |
| nansu | [nansu0425](https://github.com/nansu0425) | 소개 문서 작업 예정 |
| chanpago | [chanpago](https://github.com/chanpago) | [소개](team/chanpago.md) |

## 실행
[src/index.html](src/index.html)을 브라우저에서 연다. 외부 라이브러리나 서버는 필요 없다.
Python 3.10 이상에서 `python scripts/run.py`로 문서·HTML 링크를 점검한다.
깨진 링크가 있으면 해당 파일과 대상 경로를 출력하고 종료 코드 1을 반환한다.
기존 Git 규칙 유틸리티의 테스트는 `python -m unittest discover -s tests`로 실행한다.

## 작업 기준
- 선택한 결과물: (B) 팀 소개. HTML은 소개 문서의 입구다.
- 통합 브랜치: `b2-2`. 과제별 브랜치 저장소이므로 이번 작업에서 main 역할을 맡는다.
- 작업 브랜치: `feature/<계정>-<작업>`.
- PR 제목: `(계정): 변경 내용`.
- Git 커밋 메타데이터의 기준일은 2026-09-26이며, GitHub 활동 시각 및 검증 실행일과 별개다.
- [제출 인덱스](SUBMISSION.md) · [협업 규칙](docs/CONTRIBUTING.md)
- [충돌 해결](docs/conflict-resolution.md) · [Git 실습](docs/troubleshooting-log.md)

GitHub Flow는 작업을 작은 브랜치로 나누고 PR로 검토하기 쉽다.
통합 브랜치를 실행 가능한 상태로 유지한다.
각 변경의 이유와 검증 결과를 이슈에서 PR까지 추적한다.
