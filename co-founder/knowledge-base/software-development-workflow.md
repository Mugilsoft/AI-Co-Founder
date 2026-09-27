# Software Development Workflow — Reference Document

**Mugil Soft Solutions — Knowledge Base**

> Standard workflow for code generation, debugging, and deployment at Mugil Soft Solutions.

---

## Code Generation Workflow

When generating code for a project:

1. **Understand existing architecture** — Review the current codebase structure, patterns, and conventions before writing new code
2. **Identify affected files** — List all files that will be created, modified, or deleted
3. **Explain changes** — Describe what the changes do and why they are needed
4. **Provide exact file paths** — Use complete, unambiguous file paths
5. **Provide complete implementation** — Include complete, working code (not fragments or pseudocode) where appropriate
6. **Include dependencies** — List all package dependencies, NuGet packages, npm packages, or pip packages required
7. **Include configuration** — Provide configuration changes (appsettings.json, environment variables, etc.)
8. **Include database changes** — Provide migrations, schema changes, or seed data
9. **Include tests** — Provide unit tests and integration tests for new functionality
10. **Explain how to run** — Provide exact commands to build, run, and test
11. **Explain how to verify** — Describe how to confirm the changes work correctly

### Rules
- Do not randomly change unrelated code
- Maintain existing comments and documentation unrelated to the change
- Follow existing naming conventions and patterns in the codebase
- Preserve existing test coverage

---

## Debugging Workflow

When debugging an issue:

1. **Root Cause** — Identify the underlying cause, not just the symptom
2. **Evidence** — Show the evidence that supports the root cause analysis (logs, stack traces, test results)
3. **Fix** — Provide the specific code fix with exact file paths and line numbers
4. **Exact Commands** — Provide commands to apply and verify the fix
5. **Verification** — Describe how to confirm the fix resolves the issue
6. **Secondary Issues** — Identify any related issues that may have been caused by or masked by the original bug

---

## Deployment Workflow

### Pre-Deployment Checklist
- [ ] All tests pass (unit, integration, system)
- [ ] Code review completed
- [ ] Security review completed (for production deployments)
- [ ] Privacy review completed (if personal data is involved)
- [ ] AI governance review completed (for AI systems)
- [ ] Database migrations tested
- [ ] Configuration verified for target environment
- [ ] Monitoring and alerting configured
- [ ] Rollback plan documented
- [ ] Documentation updated

### Deployment Steps
1. Create deployment package / container image
2. Deploy to staging environment
3. Run smoke tests on staging
4. Verify monitoring is operational
5. Deploy to production (with approval for high-risk systems)
6. Run production smoke tests
7. Monitor for issues (increased monitoring period)
8. Confirm successful deployment

### Post-Deployment
- Monitor error rates and performance
- Verify all features function correctly
- Check database integrity
- Confirm logging and monitoring are capturing data
- Document any issues encountered

---

## Project Structure Standards

### .NET Projects
```
ProjectName/
├── src/
│   ├── ProjectName.API/          # Web API project
│   ├── ProjectName.Core/         # Domain models, interfaces, business logic
│   ├── ProjectName.Infrastructure/ # Data access, external services
│   └── ProjectName.Shared/       # Shared utilities, DTOs
├── tests/
│   ├── ProjectName.UnitTests/
│   └── ProjectName.IntegrationTests/
├── docs/
├── docker-compose.yml
├── .gitignore
└── README.md
```

### Angular Projects
```
project-name/
├── src/
│   ├── app/
│   │   ├── core/                 # Singleton services, guards, interceptors
│   │   ├── shared/               # Shared components, directives, pipes
│   │   └── features/             # Feature modules (lazy loaded)
│   ├── assets/
│   ├── environments/
│   └── styles/
├── angular.json
├── package.json
└── README.md
```

### Python AI/ML Projects
```
project-name/
├── src/
│   ├── data/                     # Data loading and processing
│   ├── models/                   # Model definitions
│   ├── training/                 # Training scripts
│   ├── evaluation/               # Evaluation and metrics
│   ├── inference/                # Inference/serving
│   └── utils/                    # Utility functions
├── tests/
├── notebooks/                    # Jupyter notebooks for exploration
├── configs/                      # Configuration files
├── requirements.txt
└── README.md
```

---

*Mugil Soft Solutions — Knowledge Base Document*
