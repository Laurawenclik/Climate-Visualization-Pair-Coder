# Climate Visu PostgreSQL Deployment

This directory contains a Docker Compose configuration for a PostgreSQL instance intended for the
Climate-Visualization-Pair-Coder application.

The database name is `climate_visu`. The provided SQL initialization script creates the existing
`public.result` and `public.status` tables without changing their schema.

## Contents

- `compose.yaml` — PostgreSQL container configuration.
- `.env.example` — environment-variable template. It contains no real credentials.
- `init/createDB.sql` — SQL script that creates the application's tables on first initialization.
- `.gitignore` — prevents local secrets and common database backup files from being committed.

## Important security notes

- Do not expose PostgreSQL directly to the public Internet.
- The Compose file publishes PostgreSQL on `127.0.0.1` by default. This is intentionally safe for
  initial setup but does not allow remote coder computers to connect directly.
- Before enabling remote access, the Inria administrator must approve the access method and configure
  the required firewall/network rules. Prefer an approved private network/VPN or an SSH tunnel.
- Do not commit `.env` or share it through source control, email, or this deployment archive.
- Use a long, unique password and restrict access to `.env`.
- Configure and test backups separately. A Docker volume provides persistence across container
  recreation, but it is not a backup.
- PostgreSQL image initialization variables are applied only when the data directory is empty.
  Initialization scripts in `/docker-entrypoint-initdb.d/` are run only on first initialization of
  an empty data directory.
- The `postgres:16` tag is a major-version tag, not an immutable image digest. The administrator
  should follow the organization's image-update and security-patching policy.

## Prerequisites

- Docker Engine and Docker Compose plugin installed and supported on the host.
- Permission to run Docker Compose.
- An approved location for persistent database data and backups.
- Approval from the server administrator for the chosen network/access model.

The host has been reported as CentOS Stream 8. Confirm with the administrator that the operating
system is still supported under the organization's policy before deployment.

## Deployment steps

### 1. Review the configuration

Review `compose.yaml` and `init/createDB.sql`. The SQL script creates tables; it does not issue
`CREATE DATABASE`. The database itself is created by the official PostgreSQL image using
`POSTGRES_DB=climate_visu`.

### 2. Create the server-side environment file

From this directory, copy the template:

```bash
cp .env.example .env
```

Edit `.env` and replace `POSTGRES_PASSWORD` with a long, unique random secret. Protect the file
from other users, for example:

```bash
chmod 600 .env
```

Do not put the actual password in this README or in version control.

### 3. Start PostgreSQL

```bash
docker compose pull
docker compose up -d
docker compose ps
```

Check the logs if necessary:

```bash
docker compose logs --tail=100 postgres
```

### 4. Verify the database and tables

```bash
docker compose exec postgres sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
```

List the tables:

```bash
docker compose exec postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\dt public.*"'
```

The expected application tables are `public.result` and `public.status`.

### 5. Network access — do not enable until approved

The default `POSTGRES_BIND_IP=127.0.0.1` binds the published port to loopback on the host. Remote computers
will not be able to connect with this default.

Do not change `POSTGRES_BIND_IP` to `0.0.0.0` as a shortcut. The administrator must first select and
approve the network architecture (for example, an approved VPN/private network or SSH tunnel), then
configure the host firewall and PostgreSQL access controls accordingly. The chosen configuration may
require changes to Compose, `pg_hba.conf`, or both.

### 6. Configure the local Flask applications

After the administrator confirms the network method, configure each coder's local Flask application
with the approved database host/address, port, database name (`climate_visu`), username, and password.
Keep credentials in a local environment file or another approved secrets mechanism, not in frontend
JavaScript or committed source code.

The browser should communicate with the local Flask application; it should not connect directly to
PostgreSQL.

## Database initialization and persistence

The official PostgreSQL image creates the `climate_visu` database and runs
`init/createDB.sql` only when initializing an empty data directory. The named Docker volume
`climate_visu_data` then persists the database files.

Restarting or recreating the container while retaining this volume does not re-run the SQL
initialization script. Do not remove the volume to troubleshoot unless the administrator has confirmed
that all data can be discarded. Removing a volume can permanently delete the database.

## Backups and restore

Before the database contains valuable data, agree on a backup schedule, retention period, protected
backup location, and restore test with the administrator. A volume is not a backup.

A logical backup can be made with a command similar to the following, run by an authorized operator:

```bash
docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' > climate_visu.sql
```

Store backups securely; they may contain sensitive project data. Test restoration in a separate, non-production database before relying on a backup.

## Troubleshooting

- **Container is unhealthy or will not start:** inspect `docker compose logs postgres`.
- **Initialization SQL errors:** check the logs. Initialization scripts are not automatically retried against an already initialized volume.
- **Remote connection fails:** confirm the approved VPN/tunnel/network route, host firewall, bind address, PostgreSQL access rules, and credentials with the administrator.
- **Port 5432 is already in use:** choose an approved alternative host port using `POSTGRES_PORT`, then use that port in client configuration.

## Deployment status

The following items must be confirmed before production use:

- [ ] Docker and Docker Compose are available and supported on the host.
- [ ] CentOS Stream 8 support status is confirmed.
- [ ] Persistent storage and backups are approved.
- [ ] A secure remote access method is approved for external coders.
- [ ] Firewall and PostgreSQL access rules are configured and tested.
- [ ] The initial database and both tables are verified.
- [ ] Backup and restore procedures are tested.
