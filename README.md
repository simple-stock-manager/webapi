# Simple Stock Manager — webapi

簡単な在庫管理API（FastAPI + PostgreSQL）です。

環境変数:
- `DATABASE_URL` — SQLAlchemy用の接続URL（例: `postgresql+asyncpg://user:pass@host:5432/dbname`）

ローカル実行例（DBが起動していること）:

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/postgres"
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Dockerで実行する例:

```bash
docker build -t simple-stock-manager-webapi .
docker run -e DATABASE_URL="postgresql+asyncpg://postgres:password@db:5432/postgres" -p 8000:8000 simple-stock-manager-webapi
```

APIエンドポイント:
- `POST /items` — アイテム作成
- `GET /items` — アイテム一覧
- `GET /items/{id}` — 単一取得
- `PUT /items/{id}` — 更新
- `DELETE /items/{id}` — 削除
