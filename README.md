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

## Ouvrir le conteneur avec LXC

Lister les conteneurs disponibles:

```bash
lxc list
```

Le conteneur du service doit apparaitre avec le nom `catalog-service`.
Pour ouvrir un terminal dans ce conteneur:

```bash
lxc exec catalog-service -- bash
```

Si `bash` n'est pas disponible:

```bash
lxc exec catalog-service -- sh
```

Une fois dans le conteneur, aller dans le dossier du projet:

```bash
cd /home/ubuntu/LOG430-cantelcox-catalog-service
```

Si le dossier porte un autre nom, le retrouver avec:

```bash
find / -maxdepth 4 -type d -name "LOG430-cantelcox-catalog-service" 2>/dev/null
```

Demarrer ensuite le service:

```bash
docker compose up --build
```

Si Docker bloque sur le telechargement de `python:3.12-slim` avec une erreur
`i/o timeout`, c'est generalement un probleme de connexion entre le conteneur LXC
et Docker Hub. Tester d'abord la connexion depuis le conteneur:

```bash
ping -c 4 registry-1.docker.io
```

Puis essayer de telecharger l'image manuellement:

```bash
docker pull python:3.12-slim
```

Si le `pull` fonctionne, relancer le service:

```bash
docker compose up --build
```

Si le `pull` echoue encore avec un timeout, verifier la connexion Internet de la
VM/LXC, le VPN/proxy, ou relancer la commande apres quelques minutes.

Si la connexion ne passe pas dans le conteneur LXC, tester d'abord depuis le
conteneur:

```bash
ping -c 4 8.8.8.8
```

Si ce test ne recoit aucune reponse, sortir du conteneur:

```bash
exit
```

Puis verifier depuis la machine hote que la connexion Internet fonctionne:

```bash
ping -c 4 8.8.8.8
```

Si la machine hote a Internet, verifier le reseau LXC:

```bash
lxc network list
lxc network show lxdbr0
```

Activer le NAT sur le bridge LXC, puis redemarrer le conteneur:

```bash
lxc network set lxdbr0 ipv4.nat true
lxc restart catalog-service
```

Rentrer de nouveau dans le conteneur et retester:

```bash
lxc exec catalog-service -- bash
ping -c 4 8.8.8.8
docker pull python:3.12-slim
docker compose up --build
```

Si `ipv4.nat` est deja a `true` mais que le ping vers `8.8.8.8` ne passe
toujours pas, tester la passerelle LXC depuis le conteneur:

```bash
ip route
ping -c 4 10.126.16.1
```

Si la passerelle repond mais pas Internet, sortir du conteneur et verifier le
forwarding sur la machine hote:

```bash
exit
sysctl net.ipv4.ip_forward
```

La valeur doit etre `net.ipv4.ip_forward = 1`. Sinon, l'activer:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Si UFW est active sur la machine hote, autoriser le routage depuis le bridge LXC:

```bash
sudo ufw status
ip route | grep default
sudo ufw route allow in on lxdbr0
sudo ufw reload
```

Si le ping ne passe toujours pas, autoriser explicitement le routage entre
`lxdbr0` et l'interface Internet de la machine hote. Remplacer `<interface>`
par l'interface affichee par `ip route | grep default`, par exemple `wlp3s0`,
`eth0` ou `enp0s3`:

```bash
sudo ufw route allow in on lxdbr0 out on <interface>
sudo ufw route allow in on <interface> out on lxdbr0
sudo ufw reload
```

Si UFW affiche `Status: inactive` ou `Firewall not enabled`, le probleme ne
vient pas de UFW. Verifier alors les regles NAT directement sur la machine hote:

```bash
sudo iptables -t nat -S | grep 10.126.16
sudo iptables -S FORWARD
```

Si aucune regle NAT ne correspond au reseau `10.126.16.0/24`, l'ajouter
manuellement. Remplacer `<interface>` par l'interface Internet de la machine
hote, par exemple `wlp2s0`:

```bash
sudo iptables -t nat -A POSTROUTING -s 10.126.16.0/24 -o <interface> -j MASQUERADE
sudo iptables -A FORWARD -i lxdbr0 -o <interface> -j ACCEPT
sudo iptables -A FORWARD -i <interface> -o lxdbr0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

Redemarrer ensuite le conteneur et retester:

```bash
lxc restart catalog-service
lxc exec catalog-service -- bash
ping -c 4 8.8.8.8
docker pull python:3.12-slim
```

Depuis le conteneur, le service sera accessible a l'adresse:

```text
http://127.0.0.1:8040/health
```

Depuis la machine hote, utiliser l'adresse IP du conteneur affichee par `lxc list`.
Par exemple:

```text
http://10.126.16.114:8040/health
```

Pour arreter le service:

```bash
docker compose down
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
