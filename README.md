<!-- CAR WASH MANAGEMENT SYSTEM · deep sky #0284c7 on #0d1117 · widgets verified 2026-09-12 -->

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,100:0284c7&height=190&section=header&text=CAR%20WASH%20MANAGEMENT&fontSize=52&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=roles%20%C2%B7%20tickets%20%C2%B7%20attendance%20%C2%B7%20reports%20%E2%80%94%20django&descSize=17&descAlignY=60" alt="Car Wash Management" />

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=19&duration=2600&pause=900&color=38BDF8&center=true&vCenter=true&width=760&height=95&lines=three+roles+%E2%80%94+superadmin+%C2%B7+author+%C2%B7+employer;tickets+%C2%B7+attendance+%C2%B7+requests+%C2%B7+notes;django+%2B+bootstrap+5+%2B+postgres-ready" alt="typing" />

<p>
  <img src="https://img.shields.io/badge/django-backend-0d1117?style=for-the-badge&logo=django&logoColor=44b78b" alt="django" />
  <img src="https://img.shields.io/badge/postgresql-production-0d1117?style=for-the-badge&logo=postgresql&logoColor=336791" alt="postgres" />
  <img src="https://img.shields.io/badge/bootstrap-5-0d1117?style=for-the-badge&logo=bootstrap&logoColor=7952b3" alt="bootstrap" />
  <img src="https://img.shields.io/badge/rbac-3%20roles-0284c7?style=for-the-badge&logoColor=white" alt="rbac" />
  <img src="https://img.shields.io/badge/timezone-asia%2Fdhaka-0d1117?style=for-the-badge&logoColor=38bdf8" alt="tz" />
  <img src="https://img.shields.io/badge/license-MIT-0d1117?style=for-the-badge&logoColor=38bdf8" alt="license" />
</p>

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0284c7,100:0d1117&height=3" alt="" />

## ▍$ cat overview.txt

A complete operations system for a car wash business — three permission tiers,
service tickets, daily attendance, and a built-in communication loop between
management and staff. Role-aware dashboards, paginated lists, and a reporting
layer on top. Postgres in production, SQLite for a zero-config local spin-up.

```yaml
domain    : car wash operations
roles     : superadmin (all) · author (manager) · employer (worker)
comms     : requests + replies · instructions · private notes
db        : postgresql (prod) · sqlite (dev)
tz        : Asia/Dhaka aware
security  : rbac decorators · csrf · django auth · orm (sqli-safe)
```

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0284c7,100:0d1117&height=3" alt="" />

## ▍$ ls modules/

| MODULE | WHAT IT DOES |
|---|---|
| `dashboard` | role-specific home — quick stats, recent activity, relevant nav |
| `customers` | full customer database with service history |
| `services` | service catalogue with per-type pricing |
| `tickets` | service tickets with status pipeline |
| `attendance` | daily check-in tracking with times |
| `requests` | employer → author requests, author ↔ employer replies |
| `instructions` | authored guidance pushed to employees |
| `notes` | private author → employer messaging |
| `reports` | operational reporting across the system |

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0284c7,100:0d1117&height=3" alt="" />

## ▍$ ./setup

```bash
git clone https://github.com/mhjahed/carwashmanagement.git
cd carwashmanagement

python -m venv venv && source venv/bin/activate   # windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations && python manage.py migrate
python manage.py setup_initial_data               # seeds demo accounts
python manage.py runserver                        # → http://127.0.0.1:8000
```

**seeded accounts** *(change in production)*

| ROLE | USER | PASSWORD | SCOPE |
|---|---|---|---|
| superadmin | `admin` | `admin123` | everything |
| author | `author` | `jahed1234` | instructions, oversight |
| employer | `employer` | `employer123` | attendance, requests |

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0284c7,100:0d1117&height=3" alt="" />

## ▍$ cat api.http

| METHOD | ROUTE | PURPOSE |
|---|---|---|
| POST | `/accounts/login/` · `/accounts/signup/author/` · `/accounts/signup/employer/` | auth |
| GET/POST | `/carwash/` · `/carwash/create/` | services |
| GET/POST | `/carwash/customers/` · `/carwash/customers/create/` | customers |
| GET/POST | `/attendance/` · `/attendance/mark/` | attendance |
| GET/POST | `/requests/` · `/requests/create/` · `/requests/reply/<id>/` | communication |

## ▍$ tree .

```
carwash_management/
├── accounts/      custom user + roles · auth · dashboards
├── carwash/       customers · services · tickets
├── attendance/    daily attendance + notes
├── requests/      request / reply pipeline
├── reports/       report generation
├── templates/     base + per-app views
├── static/ · media/
└── carwash_management/  settings · urls · wsgi
```

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0284c7,100:0d1117&height=3" alt="" />

## ▍$ systemctl status deploy

▸ `deploy.sh` — automated Linux/Ubuntu rollout ▸ `WINDOWS_DEPLOYMENT.md` — IIS guide
▸ `DEPLOYMENT_INSTRUCTIONS.md` — manual path ▸ automated backups — pg_dump + media archive, 7-day retention
▸ `python manage.py test` — test suite · `coverage` ready

<br/>

<div align="center">

`protections: rbac decorators · csrf · hashed passwords · orm sanitisation · session hygiene`
`built end-to-end by` **[MH JAHED](https://github.com/mhjahed)** · `mhjahed@proton.me`

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0284c7,100:0d1117&height=110&section=footer" alt="" />
