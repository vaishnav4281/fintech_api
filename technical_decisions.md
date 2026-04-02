# 🛠️ Technical Decisions & Trade-offs - Finance Dashboard API

This document outlines the architectural choices and technical trade-offs made during the development of this project.

---

## 1. Core Framework: FastAPI
**Decision:** We selected FastAPI (Python 3.12+) as the core backend framework.
*   **Rationale:** FastAPI provides native, top-tier performance for asynchronous REST operations and robust type validation through Pydantic. It significantly reduces boilerplate code for API documentation (Swagger/OpenAPI) and ensures strict contractual consistency.
*   **Trade-off:** Requires a steeper learning curve regarding dependency injection patterns compared to older frameworks like Flask.

## 2. ORM & Data Layer: SQLAlchemy 2.0
**Decision:** Leveraged SQLAlchemy 2.0 with the "Declarative Base" pattern.
*   **Rationale:** SQLAlchemy 2.0 provides a powerful, type-safe abstraction for building complex aggregation queries (Dashboard analytics) while maintaining portability between database dialects (SQLite/PostgreSQL).
*   **Trade-off:** Higher initial overhead in setting up models and relationships compared to lighter ORMs, but necessary for the complex dashboard logic required.

## 3. Persistent Storage Strategy: Hybrid (SQLite / PostgreSQL)
**Decision:** The system is built to support **SQLite** for local development/testing and **PostgreSQL** (via Neon) for production deployment.
*   **Rationale:** 
    *   **SQLite** enables immediate, zero-config testing by an examiner without needing to set up a remote database. 
    *   **PostgreSQL** provides the industrial-grade features (concurrency, data types, indexes) needed for a real financial dashboard.
*   **Trade-off:** We avoided PostgreSQL-only extensions (like native full-text search) to ensure the migration scripts (`Alembic`) remain cross-compatible with SQLite.

## 4. Security & Access Control: JWT & RBAC
**Decision:** Adopted **JWT** (JSON Web Tokens) with a centralized **Role-Based Access Control (RBAC)** dependency system.
*   **Rationale:** Stateless authentication via JWT is scalable and ideal for dashboard apps. Our centralized `permissions.py` guard pattern allows us to apply security rules (e.g., `Admin Only`) across entire modules with a single line of code, ensuring an audit-proof security layer.
*   **Trade-off:** Token invalidation (logout) is managed via expiration; a blacklisting system could be added for mission-critical security but was omitted to keep the architecture lean for this assignment.

## 5. Deletion Strategy: Soft-Delete (is_deleted Flag)
**Decision:** All `DELETE` operations on Users and Records are **Soft-Deletes**.
*   **Rationale:** In financial systems, audit trails and data integrity are paramount. Hard deletion can break referential integrity and makes forensic auditing impossible. Soft-deletion preserves the data in the database while hiding it from API consumers.
*   **Trade-off:** Increases storage overhead over time and requires all global filters to explicitly filter out `is_deleted = True` rows (which we automated via the service layer).

## 6. Architecture Pattern: Service Layer (SoC)
**Decision:** Implemented a **Service Layer Pattern** separating Routers (HTTP) from DB Logic (Services).
*   **Rationale:** Ensures **Separation of Concerns (SoC)**. Routers only handle request parsing/response formatting, while business rules and data aggregation are isolated in service modules (`record_service.py`, `dashboard_service.py`).
*   **Trade-off:** Adds extra files/folders compared to a monolithic structure, but increases maintainability and testability.

## 7. Error Handling: Global Interceptor
**Decision:** Specialized FastAPI `ExceptionHandlers` for consistent error reporting.
*   **Rationale:** Instead of standard browser error pages, every error (Auth, Validation, 404, etc.) returns a structured JSON payload with specific field-level details. This allows frontend developers to clear, actionable feedback to users.
*   **Trade-off:** Requires careful handling to avoid leaking internal system details in production logs.
