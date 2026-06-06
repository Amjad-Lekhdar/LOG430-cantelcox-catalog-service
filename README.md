# CanTelcoX Catalog Service

Microservice responsable du catalogue commercial CanTelcoX.

Le service expose une API REST versionnee pour gerer un Product Catalog BSS:
plans versionnes, promotions, add-ons, regles de compatibilite et audit. Le
stockage est in-memory pour cette tranche, avec une structure DDD/hexagonale
prete pour un adapter PostgreSQL.

Les changements commerciaux d'un plan ne modifient jamais une version existante.
Une modification de prix, donnees, appels, description ou dates cree une nouvelle
`PlanVersion`, puis met a jour `active_version_id` sur le `Plan`.

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

POST   /v1/catalog/plans/{plan_id}/versions
GET    /v1/catalog/plans/{plan_id}/versions
GET    /v1/catalog/plans/{plan_id}/versions/{version}

POST   /v1/catalog/promotions
GET    /v1/catalog/promotions

POST   /v1/catalog/addons
GET    /v1/catalog/addons

POST   /v1/catalog/compatibility-rules
GET    /v1/catalog/compatibility-rules

GET    /v1/catalog/audit-logs
```
