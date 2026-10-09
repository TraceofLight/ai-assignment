# Git 트러블슈팅 기록
실행일: 2026-10-09. 아래 SHA의 커밋 메타데이터 기준일은 2026-09-26이다.
작업 브랜치: feature/traceoflight-git-practice. 공유 이력에 대한 강제 push는 수행하지 않았다.
amend/reset 전 SHA는 로컬 실행 기록이며 일반 clone에서 접근이 보장되지 않는다. 재현할 때는 임시 브랜치에서 같은 파일 변경을 새로 커밋한 뒤 위 명령을 실행한다.
[실행 출력](../evidence/git-practice.txt) · [실습 파일](git-practice.md)

## 증빙을 읽는 기준
아래 각 항목의 SHA는 최초 실행 당시 값이다. 현재 이력은 [SHA 대응표](../evidence/commit-id-map.md)로 연결한다.
amend/reset 전 커밋은 일반 clone에서 재현 대상으로 사용하지 않는다.
원격 push 출력은 당시 신규 feature 브랜치 업로드를 증명하며, 이후 revert 커밋 생성 출력과 함께 읽는다.
이 출력만으로 별도 시점의 원격 전체 상태를 증명하지는 않는다.
평가 보완 과정에서는 과거 원격 스냅샷을 새로 만들어 과거 증빙으로 제시하지 않는다.

현재 커밋에서 결과를 확인하는 명령:
```powershell
git show 531cfddee047915aad954cf19e0aaa6e72d1a774 -- docs/git-practice.md
git show 4d5bdb81087906d811461ab828a2bff39da0d071 -- docs/git-practice.md
git show 2bc54f8b3335823e74e9284bbb2df2bbce46dde3:docs/git-practice.md
git show 4ddbc6a906ac6caf5253d00220675085bc950eaa:docs/git-practice.md
git show 86024098ec20996a401826f0cdedd794992457ab -- docs/git-practice.md
```
위 순서는 amend 결과, soft reset 후 재커밋, 원격에 올렸던 잘못된 문구, revert 복원, stash 복원 후 커밋이다.
재실습은 별도의 개인 임시 저장소에서 같은 메모 변경을 만든 뒤 아래 명령을 실행한다.
공유 이력 변경 전 합의와 메시지 수정 기준은 [협업 규칙](CONTRIBUTING.md)을 따른다.

## amend — TraceofLight
- 상황: push 전 실습 메모 커밋의 제목을 배포 기준이 드러나도록 구체화.
- 명령: `git commit --amend -m "docs(collaboration): describe the verified page baseline"`
- 변경 전: b6822eac90384df0bd40d8dba411faf9bcb35306
- 변경 후: abf620117b482a31ce60777fb773e159bbced5ab
- 결과: 파일 내용은 유지하고 메시지와 SHA 변경.
- 선택 이유: 최근 로컬 커밋의 메시지만 수정하면 되므로 reset 대신 amend 사용.
- 주의: 이미 공유한 커밋에는 적용하지 않는다.

## reset --soft — nansu0425
- 상황: 아직 push하지 않은 로컬 정리 설명 커밋을 취소하고 변경 유지.
- 명령: `git reset --soft HEAD~1` → `git status --short` → `git diff --cached --stat` → 다시 commit.
- 변경 전: fa680383a36dfcf9babf5ec3c02c14872c0403e2
- 변경 후: 5dbc08b72523118c14ac22e579e9e874ca0891d1
- 결과: docs/git-practice.md 수정이 staged 상태로 유지되는 것을 확인한 뒤 명확한 메시지로 재커밋.
- 선택 이유: --hard와 달리 변경을 버리지 않고 커밋 경계만 되돌린다.
- 주의: 공유 브랜치나 이미 push한 이력에는 적용하지 않는다.

## 원격 push 후 revert — chanpago
- 상황: 링크 검사를 생략한다는 문구를 실습용으로 커밋하고 feature 브랜치에 push.
- 원격에 올린 대상: 30f3bf5d4a0d1ca0da20b800f5a58631f0ee353e
- 명령: `git revert --no-commit 30f3bf5d4a0d1ca0da20b800f5a58631f0ee353e` 후 팀 메시지 규칙으로 commit.
- 되돌림 커밋: 89b5e79315ec89688f51351ebbd097fbcb3ef722
- 결과: 원래 검증 요구 문구 복원. 잘못된 커밋도 이력에 남아 추적 가능.
- 선택 이유: 원격 이력을 재작성하지 않기 위해 reset 대신 역변경 커밋 사용.
- 주의: --no-commit은 역변경을 staged 상태로 남기므로 반드시 검토 후 commit.

## stash / stash pop — TraceofLight
- 상황: 실습 메모 수정 도중 통합 브랜치 확인 필요.
- 명령: `git stash push -m "collaboration practice notes"` → b2-2 전환 → 작업 브랜치 복귀 → `git stash pop`.
- 결과: 변경이 복원되고 stash 항목이 제거됨. 복원 후 커밋: f6bac099cff013d8c289ff88de5da32fef6c3607.
- 선택 이유: 작업 중인 변경을 커밋하지 않고 일시 보관.
- 주의: pop은 충돌 가능성이 있으므로 status와 diff를 확인한다. stash는 원격 백업이 아니다.

## 비교
| 명령 | 목적 | 이력 영향 |
| --- | --- | --- |
| amend | 최근 로컬 커밋 수정 | 기존 SHA 변경 |
| reset --soft | 커밋 취소, 변경 보존 | 로컬 브랜치 포인터 이동 |
| revert | 공유 변경 취소 | 역변경 커밋 추가 |
| stash/pop | 미커밋 작업 임시 보관/복원 | 작업 트리 변경 |
