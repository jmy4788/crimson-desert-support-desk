# Incoming

이 폴더에 실제 import할 Markdown 문서를 넣습니다.

예시:

- `patch-1-01-03.md`
- `issue-blurry-screen.md`
- `faq-version-check.md`
- `auto\\patch-board78-1-01-02.md`
- `auto\\issue-board68-01-sample.md`

검증만:

```bash
python scripts/import_official_source.py --validate-only
```

실반영:

```bash
python scripts/import_official_source.py
```

공식 공지 초안 자동 생성:

```bash
python scripts/fetch_official_notices.py --locale ko-KR --pages 4 --clean-output --validate-only
```
