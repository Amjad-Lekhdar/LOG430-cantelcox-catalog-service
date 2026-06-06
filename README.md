# CanTelcoX Catalog Service

Microservice responsable du catalogue commercial CanTelcoX.

Le service expose une API REST versionnee pour lister, creer, modifier et
desactiver les plans mobiles. Le stockage est in-memory pour cette premiere
tranche, avec une structure DDD/hexagonale prete pour un adapter PostgreSQL.

## Run local

```bash
cd services/catalog-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8040 --reload
```

## Endpoints

```text
GET    /health
POST   /v1/catalog/plans
GET    /v1/catalog/plans
GET    /v1/catalog/plans/{plan_id}
PUT    /v1/catalog/plans/{plan_id}
DELETE /v1/catalog/plans/{plan_id}
```
