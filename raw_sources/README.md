# Raw Sources

실제 공식 데이터를 넣을 때는 이 폴더를 사용합니다.

## 폴더 구조

- `incoming/`: 실제로 import할 Markdown 문서를 넣는 곳
- `templates/`: 복사해서 쓰는 예시 템플릿

## 기본 사용 흐름

1. 자동 초안을 만들려면 먼저 아래 실행

```bash
python scripts/fetch_official_notices.py --locale ko-KR --pages 4 --clean-output --validate-only
```

2. `incoming/auto/`에 생성된 초안을 검토하고 필요한 필드만 보정
3. 자동 초안이 부족하면 `templates/`에서 가장 가까운 유형의 파일을 복사
4. frontmatter 값을 실제 공식 데이터 기준으로 수정
5. 문서 본문 아래에 공식 원문을 붙여 넣기
6. 아래 명령으로 검증

```bash
python scripts/import_official_source.py --validate-only
```

7. 검증이 통과하면 실제 반영

```bash
python scripts/import_official_source.py
```

## 자동 수집 주의

- 자동 수집은 공식 공지 HTML을 기반으로 초안 문서를 생성합니다.
- `patch_note`는 비교적 안정적이지만 `known_issue`는 공지 한 건을 여러 issue 초안으로 쪼갤 수 있습니다.
- 생성된 `slug`, `category`, `status`, `platforms`는 휴리스틱 결과이므로 import 전 한 번 검토하는 편이 좋습니다.

## 일반 주의

- import 대상은 frontmatter가 있는 Markdown 파일만 처리합니다.
- 연결 대상 `issue slug`나 `patch version`이 아직 DB에 없으면 문서는 저장되지만 링크는 경고와 함께 건너뜁니다.
- 공식 URL, 게시일, 확인일, 요약, 라벨은 비워 두지 않는 편이 좋습니다.
