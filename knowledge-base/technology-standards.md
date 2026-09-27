# Technology Standards — Reference Document

**Mugil Soft Solutions — Knowledge Base**

> Mugil Soft Solutions' preferred technology stack, selection criteria, and coding standards. Technology selection is driven by requirements, budget, team capability, security, scalability, and maintenance — not novelty.

---

## Preferred Technology Stack

### Backend
| Technology | Use Case |
|-----------|----------|
| **C#** | Primary backend language |
| **.NET / ASP.NET Core** | Web APIs, web applications, background services |
| **Entity Framework Core** | ORM for database access |
| **REST APIs** | Standard API design pattern |

### Frontend
| Technology | Use Case |
|-----------|----------|
| **Angular** | Primary SPA framework |
| **TypeScript** | Strongly-typed frontend code |
| **HTML / CSS** | Standard web markup and styling |
| **Angular Material** | UI component library |

### AI / Machine Learning
| Technology | Use Case |
|-----------|----------|
| **Python** | Primary AI/ML language |
| **PyTorch** | Deep learning and neural networks |
| **scikit-learn** | Traditional ML (classification, regression, clustering) |
| **Hugging Face / Transformers** | Pre-trained models, NLP, embeddings |
| **LLMs** | Large language models (cloud and local) |
| **Ollama** | Local LLM hosting (when appropriate) |
| **RAG** | Retrieval-Augmented Generation for knowledge-grounded AI |
| **Vector Databases** | Embedding storage and similarity search |
| **AI Agents** | Autonomous/semi-autonomous task completion |

### Databases
| Technology | Use Case |
|-----------|----------|
| **SQL Server** | Enterprise applications, Azure integration |
| **PostgreSQL** | Open-source relational database |
| **MySQL** | Web applications, lightweight deployments |
| **SQLite** | Embedded, local, and mobile databases |

### Cloud (Microsoft Azure)
| Service | Use Case |
|---------|----------|
| **Azure App Service** | Web application hosting |
| **Azure SQL** | Managed SQL database |
| **Azure Storage** | Blob, file, queue, and table storage |
| **Azure Functions** | Serverless compute |
| **Azure AI Services** | Cognitive services, AI APIs (when appropriate) |

### Development & DevOps
| Tool | Use Case |
|------|----------|
| **Git** | Version control |
| **GitHub / GitLab** | Repository hosting, CI/CD, issue tracking |
| **Docker** | Containerisation |
| **CI/CD** | Automated build, test, and deployment |
| **Automated Testing** | Unit, integration, and system tests |

---

## Technology Selection Criteria

When selecting technology for a project, evaluate:

| Criterion | Question |
|-----------|----------|
| **Requirements** | Does this technology meet the functional and non-functional requirements? |
| **Budget** | Can the project afford the licensing, hosting, and operational costs? |
| **Team Capability** | Does the team have (or can it acquire) the skills to use this technology effectively? |
| **Security** | Does the technology have a good security track record and appropriate security features? |
| **Scalability** | Can the technology scale to meet anticipated growth? |
| **Maintenance** | Is the technology actively maintained? Is there a community and documentation? |
| **Deployment Environment** | Is the technology compatible with the target deployment environment? |
| **Maturity** | Is the technology sufficiently mature and stable for production use? |
| **Vendor Lock-In** | Does this technology create unacceptable vendor dependency? |

**Rule:** Do not select technology simply because it is new or impressive. Every technology choice must be justified by project requirements.

---

## Coding Standards

### General
- Write clean, readable, and maintainable code
- Follow established conventions for the language/framework
- Use meaningful names for variables, functions, classes, and files
- Keep functions and methods focused (single responsibility)
- Comment complex logic; avoid commenting the obvious
- Handle errors explicitly — do not swallow exceptions

### C# / .NET
- Follow Microsoft C# coding conventions
- Use dependency injection
- Implement interface-based design for testability
- Use async/await for I/O-bound operations
- Validate all inputs, especially API endpoints

### Angular / TypeScript
- Use Angular CLI for project structure
- Use strict TypeScript configuration
- Implement lazy loading for feature modules
- Use reactive forms for complex forms
- Follow the Angular style guide

### Python (AI/ML)
- Follow PEP 8 style guidelines
- Use type hints
- Use virtual environments for dependency isolation
- Document functions with docstrings
- Use requirements.txt or pyproject.toml for dependency management
- Log experiment parameters and results

### SQL
- Use parameterised queries (never concatenate user input)
- Use migrations for schema changes
- Index appropriately for query performance
- Follow naming conventions consistently

---

## Security Standards

- Never store secrets (passwords, API keys, tokens) in source code or configuration files committed to version control
- Use environment variables or secret management tools for sensitive configuration
- Implement authentication and authorisation for all APIs
- Use HTTPS for all communications
- Validate and sanitise all user inputs
- Apply the principle of least privilege for data access
- Conduct security reviews before deployment
- Keep dependencies updated to patch known vulnerabilities

---

*Mugil Soft Solutions — Knowledge Base Document*
