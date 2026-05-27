# Stage 3 Authentication

Stage 3 adds JWT authentication for the SaaS workspace.

Backend:

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

Implemented:

- Password hashing with bcrypt.
- JWT access and refresh tokens.
- Bearer token validation.
- Role-based dependency helper.
- Initial `users` and `businesses` SQLAlchemy models.
- Auth service and repository layer.

Frontend:

- Login page.
- Signup page.
- Protected dashboard routes.
- Local token storage.
- Authenticated Axios requests.
- Logout action.

Stage 4 will replace startup table creation with Alembic migrations and expand the full database model set.

