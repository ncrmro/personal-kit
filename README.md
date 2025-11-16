# Persona Kit

<div align="center">
    <h1>🎭 Persona Kit</h1>
    <h3><em>Create markdown-based personas for AI agents and review websites</em></h3>
</div>

<p align="center">
    <strong>A toolkit for creating and managing AI personas that can be used as system prompts and for reviewing websites using Playwright MCP.</strong>
</p>

---

## Quick Start

```bash
# Initialize a new project
persona-kit init my-project
cd my-project

# Create a persona
persona-kit persona create security-expert

# List all personas
persona-kit persona list

# Review a website
persona-kit review https://example.com --persona security-expert
```

## What is Persona Kit?

**Persona Kit** is a command-line tool for creating and managing markdown-based personas. These personas can be:

1. **Used as system prompts** for AI agents (Claude, GPT, etc.)
2. **Applied to website reviews** using Playwright MCP integration  
3. **Shared and version-controlled** as simple markdown files

## Installation

```bash
git clone https://github.com/ncrmro/personal-kit.git
cd personal-kit
pip install -e .
```

## Core Features

- 🎭 **Persona Management** - Create, list, and manage markdown-based personas
- 🔍 **Website Reviews** - Review websites from specific persona perspectives
- 📝 **Markdown-Based** - Simple, version-controllable persona definitions
- 🤖 **AI Integration** - Use personas as system prompts for AI agents

## Usage

See the [full documentation](docs/README.md) for detailed usage instructions.

## License

MIT License - see [LICENSE](LICENSE) for details.
