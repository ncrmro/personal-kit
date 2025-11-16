#!/usr/bin/env python3
"""
Persona Kit - Create markdown-based personas for AI agents and review websites

Usage:
    persona-kit init <project-name>
    persona-kit persona create <persona-name>
    persona-kit persona list
    persona-kit review <url> --persona <persona-name>
    persona-kit check
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional
import datetime

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from typer.core import TyperGroup

console = Console()

BANNER = """
██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗ █████╗ 
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║██╔══██╗
██████╔╝█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║███████║
██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║██╔══██║
██║     ███████╗██║  ██║███████║╚██████╔╝██║ ╚████║██║  ██║
╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
██╗  ██╗██╗████████╗
██║ ██╔╝██║╚══██╔══╝
█████╔╝ ██║   ██║   
██╔═██╗ ██║   ██║   
██║  ██╗██║   ██║   
╚═╝  ╚═╝╚═╝   ╚═╝   
"""

TAGLINE = "Create markdown-based personas and review websites"

class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        show_banner()
        super().format_help(ctx, formatter)

app = typer.Typer(
    name="persona-kit",
    help="Create markdown-based personas and review websites using Playwright MCP",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)

# Create sub-commands for personas
persona_app = typer.Typer(help="Manage personas")
app.add_typer(persona_app, name="persona")

def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_magenta", "magenta", "bright_blue", "blue", "cyan", "bright_cyan"]
    
    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)
    
    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()

@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'persona-kit --help' for usage information[/dim]"))
        console.print()

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (or use '.' for current directory)"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory"),
):
    """
    Initialize a new Persona Kit project.
    
    Creates the necessary directory structure and templates for managing personas.
    
    Examples:
        persona-kit init my-project
        persona-kit init .
        persona-kit init --here
    """
    show_banner()
    
    if project_name == ".":
        here = True
        project_name = None
    
    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)
    
    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)
    
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()
    else:
        project_path = Path(project_name).resolve()
        if project_path.exists():
            console.print(f"[red]Error:[/red] Directory '{project_name}' already exists")
            raise typer.Exit(1)
        project_path.mkdir(parents=True)
    
    console.print(f"[cyan]Initializing Persona Kit project:[/cyan] {project_name}")
    
    # Create directory structure
    personas_dir = project_path / ".personas"
    personas_dir.mkdir(exist_ok=True)
    
    reviews_dir = project_path / ".reviews"
    reviews_dir.mkdir(exist_ok=True)
    
    # Create README
    readme_path = project_path / "README.md"
    if not readme_path.exists():
        readme_content = f"""# {project_name}

A Persona Kit project for creating and managing AI personas.

## Getting Started

### Create a Persona

```bash
persona-kit persona create security-expert
```

### List Personas

```bash
persona-kit persona list
```

### Review a Website

```bash
persona-kit review https://example.com --persona security-expert
```

## Directory Structure

- `.personas/` - Markdown-based persona definitions
- `.reviews/` - Website review outputs
"""
        readme_path.write_text(readme_content)
    
    # Create example persona
    example_persona = personas_dir / "example-persona.md"
    if not example_persona.exists():
        persona_template = """# Example Persona

## Role
UX Designer and Accessibility Expert

## Background
You are an experienced UX designer with 10+ years of experience in web accessibility and inclusive design. You specialize in WCAG compliance and user-centered design principles.

## Expertise
- Web Content Accessibility Guidelines (WCAG) 2.1 Level AA
- Inclusive design patterns
- User experience best practices
- Color contrast and visual hierarchy
- Keyboard navigation and screen reader compatibility

## Review Focus
When reviewing websites, you focus on:
- Accessibility compliance (WCAG standards)
- Visual design and hierarchy
- Navigation patterns
- Color contrast and readability
- Mobile responsiveness
- User flow and interaction design

## Communication Style
- Professional and constructive
- Data-driven with specific examples
- Actionable recommendations
- Prioritized by severity (Critical, Important, Recommended)

## Output Format
Provide reviews in markdown format with:
- Executive summary
- Findings organized by category
- Specific issues with screenshots/examples
- Recommendations with priority levels
- Compliance checklist
"""
        example_persona.write_text(persona_template)
    
    console.print(f"[green]✓[/green] Created directory structure")
    console.print(f"[green]✓[/green] Created example persona at [cyan].personas/example-persona.md[/cyan]")
    
    # Success message
    success_panel = Panel(
        f"[green]Project initialized successfully![/green]\n\n"
        f"Next steps:\n"
        f"1. {'You are in the project directory' if here else f'cd {project_name}'}\n"
        f"2. Create a persona: [cyan]persona-kit persona create my-persona[/cyan]\n"
        f"3. Review a website: [cyan]persona-kit review https://example.com --persona my-persona[/cyan]",
        title="Success",
        border_style="green"
    )
    console.print()
    console.print(success_panel)

@persona_app.command("create")
def create_persona(
    persona_name: str = typer.Argument(..., help="Name for the new persona (e.g., 'security-expert')"),
):
    """
    Create a new persona from a template.
    
    Examples:
        persona-kit persona create security-expert
        persona-kit persona create ux-designer
    """
    show_banner()
    
    # Check if we're in a persona-kit project
    personas_dir = Path.cwd() / ".personas"
    if not personas_dir.exists():
        console.print("[red]Error:[/red] Not in a Persona Kit project. Run [cyan]persona-kit init[/cyan] first.")
        raise typer.Exit(1)
    
    # Sanitize persona name
    persona_file = persona_name.lower().replace(" ", "-")
    if not persona_file.endswith(".md"):
        persona_file += ".md"
    
    persona_path = personas_dir / persona_file
    
    if persona_path.exists():
        console.print(f"[yellow]Warning:[/yellow] Persona '{persona_name}' already exists at {persona_path}")
        overwrite = typer.confirm("Do you want to overwrite it?")
        if not overwrite:
            console.print("[yellow]Operation cancelled[/yellow]")
            raise typer.Exit(0)
    
    # Create persona from template
    persona_template = f"""# {persona_name.replace('-', ' ').title()}

## Role
[Describe the role/profession of this persona]

## Background
[Describe the background, experience, and qualifications of this persona]

## Expertise
- [Area of expertise 1]
- [Area of expertise 2]
- [Area of expertise 3]

## Review Focus
When reviewing websites, this persona focuses on:
- [Focus area 1]
- [Focus area 2]
- [Focus area 3]

## Communication Style
- [Communication style trait 1]
- [Communication style trait 2]
- [Communication style trait 3]

## Output Format
[Describe how this persona should structure their reviews]
"""
    
    persona_path.write_text(persona_template)
    
    console.print(f"[green]✓[/green] Created persona: [cyan]{persona_file}[/cyan]")
    console.print(f"[dim]Edit the file to customize the persona: {persona_path}[/dim]")

@persona_app.command("list")
def list_personas():
    """
    List all available personas in the current project.
    """
    show_banner()
    
    personas_dir = Path.cwd() / ".personas"
    if not personas_dir.exists():
        console.print("[red]Error:[/red] Not in a Persona Kit project. Run [cyan]persona-kit init[/cyan] first.")
        raise typer.Exit(1)
    
    personas = sorted(personas_dir.glob("*.md"))
    
    if not personas:
        console.print("[yellow]No personas found.[/yellow] Create one with [cyan]persona-kit persona create <name>[/cyan]")
        return
    
    table = Table(title="Available Personas")
    table.add_column("Name", style="cyan")
    table.add_column("File", style="dim")
    
    for persona_path in personas:
        persona_name = persona_path.stem
        table.add_row(persona_name, str(persona_path))
    
    console.print(table)

@app.command()
def review(
    url: str = typer.Argument(..., help="URL of the website to review"),
    persona: str = typer.Option(..., "--persona", "-p", help="Name of the persona to use for the review"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path (default: .reviews/<persona>-<timestamp>.md)"),
):
    """
    Review a website using a specific persona and Playwright MCP.
    
    This command uses the Playwright MCP server to navigate and analyze a website
    from the perspective of the specified persona.
    
    Examples:
        persona-kit review https://example.com --persona security-expert
        persona-kit review https://example.com -p ux-designer -o my-review.md
    """
    show_banner()
    
    # Check if we're in a persona-kit project
    personas_dir = Path.cwd() / ".personas"
    if not personas_dir.exists():
        console.print("[red]Error:[/red] Not in a Persona Kit project. Run [cyan]persona-kit init[/cyan] first.")
        raise typer.Exit(1)
    
    # Find persona file
    persona_file = persona.lower().replace(" ", "-")
    if not persona_file.endswith(".md"):
        persona_file += ".md"
    
    persona_path = personas_dir / persona_file
    
    if not persona_path.exists():
        console.print(f"[red]Error:[/red] Persona '{persona}' not found at {persona_path}")
        console.print(f"[dim]Available personas:[/dim]")
        for p in sorted(personas_dir.glob("*.md")):
            console.print(f"  - {p.stem}")
        raise typer.Exit(1)
    
    # Load persona
    persona_content = persona_path.read_text()
    
    console.print(f"[cyan]Reviewing:[/cyan] {url}")
    console.print(f"[cyan]Persona:[/cyan] {persona}")
    console.print()
    console.print("[yellow]Note:[/yellow] This is a placeholder implementation.")
    console.print("[yellow]To enable full functionality, you need:[/yellow]")
    console.print("  1. Playwright MCP server running")
    console.print("  2. AI agent integration (Claude, GPT, etc.)")
    console.print()
    console.print("[dim]The actual review would:[/dim]")
    console.print("  - Use Playwright MCP to navigate the website")
    console.print("  - Take screenshots and analyze the page")
    console.print("  - Apply the persona's expertise and perspective")
    console.print("  - Generate a comprehensive review report")
    console.print()
    
    # Generate placeholder review
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    if output is None:
        reviews_dir = Path.cwd() / ".reviews"
        reviews_dir.mkdir(exist_ok=True)
        output = str(reviews_dir / f"{persona}-{timestamp}.md")
    
    review_content = f"""# Website Review: {url}

**Reviewer Persona:** {persona}  
**Review Date:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**URL:** {url}

## Persona Context

{persona_content}

---

## Review Process

*This is a placeholder review. In the full implementation, this section would be automatically generated using:*

1. **Playwright MCP Integration**: Navigate to the website, take screenshots, analyze DOM structure
2. **AI Agent Analysis**: Apply the persona's expertise to review the website
3. **Structured Output**: Generate findings, recommendations, and action items

## Executive Summary

[Would contain high-level overview of findings]

## Detailed Findings

### Category 1
- Finding 1
- Finding 2

### Category 2
- Finding 1
- Finding 2

## Recommendations

1. **Critical**: [High priority items]
2. **Important**: [Medium priority items]
3. **Nice to Have**: [Low priority items]

## Compliance Checklist

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Screenshots

[Screenshots would be embedded here]

---

*Generated by Persona Kit*
"""
    
    Path(output).write_text(review_content)
    console.print(f"[green]✓[/green] Review saved to: [cyan]{output}[/cyan]")

@app.command()
def check():
    """
    Check that all required tools are installed.
    """
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")
    
    # Check Python
    table = Table(title="Tool Status")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Notes", style="dim")
    
    # Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python", f"[green]✓[/green] {python_version}", "Required >= 3.11")
    
    # Git
    git_found = shutil.which("git") is not None
    table.add_row(
        "Git",
        "[green]✓[/green] installed" if git_found else "[yellow]○[/yellow] not found",
        "Optional for version control"
    )
    
    console.print(table)
    console.print()
    console.print("[bold green]Persona Kit is ready to use![/bold green]")
    console.print()
    console.print("[dim]Note: Full review functionality requires:[/dim]")
    console.print("  - Playwright MCP server")
    console.print("  - AI agent integration (Claude Code, GitHub Copilot, etc.)")

def main():
    app()

if __name__ == "__main__":
    main()
