# Documentation Index

Welcome to the **Azure Container Apps Blue-Green Deployment Demo** documentation. This index will help you navigate all available resources.

> **Note**: Most documentation is in the `/copilot` folder to keep the root clean.

## 📚 Documentation Structure

### 🚀 Getting Started

1. **[README.md](./README.md)** - Start here!
   - Project overview and key features
   - Quick start guide (local and Azure)
   - Architecture diagram
   - Environment variables reference
   - Testing instructions

### 📖 Deployment Guides

2. **[DEPLOYMENT.md](./copilot/DEPLOYMENT.md)** - Complete deployment guide
   - Local development workflow
   - Blue-green deployment steps
   - CI/CD workflow documentation
   - Rollback procedures (saved images vs. query Azure)
   - Troubleshooting section

3. **[QUICKREF.md](./copilot/QUICKREF.md)** - Quick reference card
   - Common commands at a glance
   - Local deployment commands
   - CI/CD workflow triggers
   - Azure CLI queries for rollback
   - Decision tree: when to track images vs. query Azure

### 🔧 Technical Reference

4. **[ref.md](./copilot/ref.md)** - Azure Developer CLI reference
   - Revision-based deployment strategy (PR #5694)
   - Parameters and environment variables
   - Conditional deployment patterns
   - Traffic management

### 📊 Project Documentation

5. **[PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md)** - Executive summary
   - Mission and objectives
   - What was built (application, infrastructure, CI/CD)
   - Key technical solutions (ACR auth, rollback, etc.)
   - Key learnings (13 critical patterns)
   - Production readiness checklist
   - Blog post topics

6. **[EVOLUTION.md](./copilot/EVOLUTION.md)** - Solution evolution timeline
   - Phase-by-phase development journey
   - Problems encountered and solutions found
   - Architecture evolution diagrams
   - Image tracking vs. query Azure comparison
   - Lessons learned table
   - Success metrics

### 📝 Blog and Presentation Material

7. **[blog.md](./copilot/blog.md)** - Blog post draft (if created)
   - Long-form article about the solution
   - Suitable for tech blogs or Azure community

### 🤖 Development Context

8. **[.github/copilot-instructions.md](./.github/copilot-instructions.md)** - Copilot workspace context
   - Project goals and constraints
   - Development guidelines
   - Key implementation details
   - Project status

## 🎯 Documentation by Use Case

### "I'm new and want to understand the project"
→ Start with [README.md](./README.md) then read [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md)

### "I want to deploy this locally"
→ Follow [README.md](./README.md) Quick Start → Then [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) Local Workflow

### "I want to set up CI/CD"
→ Read [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) CI/CD Workflow section → Check [QUICKREF.md](./copilot/QUICKREF.md) for commands

### "I need to troubleshoot deployment issues"
→ Check [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) Troubleshooting → Reference [QUICKREF.md](./copilot/QUICKREF.md)

### "I want to understand the technical decisions"
→ Read [EVOLUTION.md](./copilot/EVOLUTION.md) → Then [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md) Key Learnings

### "I need specific azd commands"
→ Jump to [QUICKREF.md](./copilot/QUICKREF.md) → Or reference [ref.md](./copilot/ref.md)

### "I want to write about this project"
→ Read [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md) → Review [EVOLUTION.md](./copilot/EVOLUTION.md) for story arc

### "I want to implement something similar"
→ Study [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) → Review [ref.md](./copilot/ref.md) → Check [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md) Key Learnings

## 📁 File Organization

```
aca-blue-green/
├── Documentation
│   ├── README.md                    # Project overview and quick start ⭐ (ROOT)
│   ├── DOC_INDEX.md                 # This file (ROOT)
│   └── copilot/                     # Detailed documentation folder
│       ├── DEPLOYMENT.md            # Complete deployment guide ⭐
│       ├── QUICKREF.md              # Quick reference card ⭐
│       ├── PROJECT_SUMMARY.md       # Executive summary
│       ├── EVOLUTION.md             # Solution evolution timeline
│       ├── ref.md                   # azd revision-based deployment reference
│       └── blog.md                  # Blog post material (if exists)
│
├── Application Code
│   ├── app.py                       # FastAPI application
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Container image definition
│   └── .dockerignore                # Docker ignore patterns
│
├── Infrastructure (Bicep)
│   ├── infra/
│   │   ├── main.bicep              # Provision-time infrastructure
│   │   ├── web.bicep               # Deploy-time container app
│   │   ├── web.parameters.json     # Deployment parameters
│   │   └── modules/
│   │       └── container-apps-environment.bicep  # Public environment
│   └── azure.yaml                   # azd configuration
│
├── CI/CD Workflows
│   └── .github/
│       ├── workflows/
│       │   ├── azure-dev.yml       # Main deployment workflow
│       │   └── rollback.yml        # Manual rollback workflow
│       └── copilot-instructions.md  # Copilot workspace context
│
└── Configuration
    └── .azure/<env>/
        └── .env                     # Environment variables
```

## 🔖 Quick Links by Topic

### Deployment
- [Local Deployment](./copilot/DEPLOYMENT.md#local-workflow)
- [Azure Deployment](./README.md#2-azure-deployment-with-azd)
- [Blue-Green Workflow](./copilot/DEPLOYMENT.md#blue-green-deployment-workflow)
- [Traffic Switching](./copilot/DEPLOYMENT.md#switch-production-traffic-to-green)
- [Rollback Procedures](./copilot/DEPLOYMENT.md#rollback-options)

### CI/CD
- [GitHub Actions Setup](./copilot/DEPLOYMENT.md#cicd-workflow)
- [Main Deployment Workflow](./copilot/DEPLOYMENT.md#main-deployment-workflow-azure-devyml)
- [Rollback Workflow](./copilot/DEPLOYMENT.md#rollback-workflow-rollbackyml)
- [Workflow Triggers](./copilot/QUICKREF.md#cicd-workflows)

### Technical Details
- [Architecture](./README.md#-architecture)
- [Key Features](./README.md#-key-features)
- [How It Works](./README.md#-how-it-works)
- [Environment Variables](./README.md#environment-variables)
- [Traffic Routing Logic](./README.md#traffic-routing-logic)
- [Infrastructure Highlights](./README.md#infrastructure-highlights)

### Reference
- [azd Commands](./copilot/QUICKREF.md#local-deployment)
- [Azure CLI Queries](./copilot/QUICKREF.md#azure-cli-commands-for-querying)
- [Troubleshooting](./copilot/DEPLOYMENT.md#troubleshooting)
- [Decision Trees](./copilot/QUICKREF.md#decision-tree-image-tracking-vs-query-azure)

### Learning Resources
- [Key Learnings](./copilot/PROJECT_SUMMARY.md#-key-learnings)
- [Solution Evolution](./copilot/EVOLUTION.md)
- [Lessons Learned](./copilot/EVOLUTION.md#lessons-learned-summary)
- [Success Metrics](./copilot/EVOLUTION.md#success-metrics-)

## 📋 Recommended Reading Order

### For Developers (Hands-On)
1. [README.md](./README.md) - Understand the project
2. [QUICKREF.md](./copilot/QUICKREF.md) - Bookmark for commands
3. [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) - Follow deployment steps
4. [ref.md](./copilot/ref.md) - Understand azd patterns

### For Architects (Design)
1. [README.md](./README.md) - Architecture overview
2. [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md) - Technical solutions
3. [EVOLUTION.md](./copilot/EVOLUTION.md) - Design decisions
4. [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) - Implementation patterns

### For DevOps Engineers (Operations)
1. [QUICKREF.md](./copilot/QUICKREF.md) - Commands reference
2. [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) - CI/CD workflows
3. [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md) - Key learnings
4. [README.md](./README.md) - Troubleshooting

### For Content Creators (Writing)
1. [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md) - Executive summary
2. [EVOLUTION.md](./copilot/EVOLUTION.md) - Story and journey
3. [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) - Technical details
4. [README.md](./README.md) - Feature highlights

## 🎯 Documentation Coverage

| Topic | Coverage | Location |
|-------|----------|----------|
| Project Overview | ✅ Complete | README.md |
| Quick Start | ✅ Complete | README.md |
| Local Deployment | ✅ Complete | DEPLOYMENT.md |
| CI/CD Workflows | ✅ Complete | DEPLOYMENT.md |
| Troubleshooting | ✅ Complete | DEPLOYMENT.md |
| Command Reference | ✅ Complete | QUICKREF.md |
| azd Patterns | ✅ Complete | ref.md |
| Technical Solutions | ✅ Complete | PROJECT_SUMMARY.md |
| Evolution Timeline | ✅ Complete | EVOLUTION.md |
| Key Learnings | ✅ Complete | PROJECT_SUMMARY.md |

## 💡 Tips for Using This Documentation

1. **Bookmark [QUICKREF.md](./copilot/QUICKREF.md)** - It's your go-to for quick commands
2. **Read [EVOLUTION.md](./copilot/EVOLUTION.md)** to understand "why" decisions were made
3. **Keep [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) open** when deploying
4. **Reference [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md)** for the big picture
5. **Use DOC_INDEX.md** (this file) to navigate effectively

## 🔄 Document Updates

All documentation is current as of the final project state. Key files:
- ✅ README.md - Updated with CI/CD workflows and key patterns (ROOT)
- ✅ DEPLOYMENT.md - Complete with rollback workflows (copilot/)
- ✅ QUICKREF.md - Comprehensive command reference (copilot/)
- ✅ PROJECT_SUMMARY.md - Executive summary with all learnings (copilot/)
- ✅ EVOLUTION.md - Complete solution evolution timeline (copilot/)
- ✅ DOC_INDEX.md - This comprehensive index (ROOT)

## 📞 Need Help?

If you can't find what you're looking for:

1. Check the [QUICKREF.md](./copilot/QUICKREF.md) for quick answers
2. Search [DEPLOYMENT.md](./copilot/DEPLOYMENT.md) Troubleshooting section
3. Review [EVOLUTION.md](./copilot/EVOLUTION.md) for context on design decisions
4. Read [PROJECT_SUMMARY.md](./copilot/PROJECT_SUMMARY.md) Key Learnings section

---

**Documentation Status**: ✅ **COMPLETE**

*Comprehensive documentation for production-ready Azure Container Apps blue-green deployment* 📚
