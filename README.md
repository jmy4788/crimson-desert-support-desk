# Crimson Desert Support Desk

붉은사막 싱글플레이 지원 허브용 MVP입니다. 공식 공지를 기준으로 패치, known issues, FAQ, Settings Doctor를 한 화면 구조로 연결합니다.

## Stack

- Frontend: React + Vite + TypeScript + Tailwind
- Backend: FastAPI + SQLModel + SQLite
- Search: SQLite FTS5
- Data: `data/seeds/sample_data.json` 기반 샘플 시드

## Structure

- `backend`: FastAPI API, 시드 적재, diff 생성, Settings Doctor 규칙
- `frontend`: 한국어 우선 지원 허브 UI
- `data/seeds`: 데모 시드 데이터
- `scripts/seed_local.py`: 로컬 DB 초기 시드 유틸

## Run

### Windows Quick Start

루트 폴더에서 바로 실행할 수 있는 `.bat` 파일을 같이 제공합니다.

```bat
run_support_desk.bat
```

- `run_support_desk.bat`: 백엔드와 프론트엔드를 각각 새 창으로 동시에 실행
- `run_backend.bat`: 백엔드만 실행
- `run_frontend.bat`: 프론트엔드만 실행
- 기본 주소:
  - Backend: `http://127.0.0.1:8017`
  - Frontend: `http://127.0.0.1:4173`

### 1. Backend

```bash
python -m pip install -e backend[dev]
python scripts/run_backend_server.py
```

기본 API 주소는 `http://127.0.0.1:8017`입니다. 앱 시작 시 DB가 비어 있으면 샘플 시드를 자동 적재합니다.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

기본 프론트 주소는 `http://127.0.0.1:4173`입니다. 다른 API 주소를 쓰려면 `VITE_API_BASE_URL` 환경 변수를 지정하면 됩니다.

## Key Routes

- `/ko`
- `/ko/patches`
- `/ko/patches/:version`
- `/ko/issues`
- `/ko/issues/:slug`
- `/ko/faq`
- `/ko/search`
- `/ko/settings-doctor`

## API

- `GET /api/health`
- `GET /api/patches`
- `GET /api/patches/{version}`
- `GET /api/issues`
- `GET /api/issues/{slug}`
- `GET /api/faq`
- `GET /api/search`
- `POST /api/settings-doctor/query`
- `POST /api/admin/seed`

`POST /api/admin/seed`는 `dev/test` 환경에서만 동작합니다.

## Tests

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

## Import Official Sources

실제 운영 데이터는 `raw_sources/` 아래의 Markdown frontmatter 문서로 넣을 수 있습니다.

공식 공지 초안 자동 생성:

```bash
fetch_official_notices.bat
```

공식 공지 자동 반영:

```bash
sync_official_notices.bat
```

직접 실행:

```bash
python scripts/fetch_official_notices.py --locale ko-KR --pages 4 --clean-output --validate-only
```

검증만:

```bash
python scripts/import_official_source.py --validate-only
```

실반영:

```bash
python scripts/import_official_source.py
```

템플릿:

- `raw_sources/templates/patch_note_template.md`
- `raw_sources/templates/known_issue_template.md`
- `raw_sources/templates/faq_template.md`

## Notes

- 샘플 데이터는 데모용이며, 실제 운영에서는 공식 공지를 자동 수집해 초안 Markdown으로 만든 뒤 검토 후 반영하는 흐름을 권장합니다.
- Settings Doctor는 결정적 규칙만 사용하며, 위험한 레지스트리 수정이나 출처 불명 커뮤니티 팁은 제외했습니다.

## Deploy

현재 배포 기본 조합은 아래를 기준으로 준비되어 있습니다.

- Frontend: Vercel
- Backend: Render

추가된 배포 준비 파일:

- `frontend/vercel.json`
- `render.yaml`
- `.env.example`
- `frontend/.env.example`

중요 환경 변수:

### Vercel

- `VITE_API_BASE_URL`
- `VITE_SITE_URL`

### Render

- `SUPPORT_DESK_DATABASE_URL`
- `SUPPORT_DESK_CORS_ORIGINS`
- `SUPPORT_DESK_APP_ENV=prod`
- `SUPPORT_DESK_AUTO_SEED_ON_START=false`

배포 단계 안내는 `docs/launch/04_vercel_render_setup.md`를 참고하세요.
