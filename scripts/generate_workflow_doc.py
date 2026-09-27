"""
Script to generate Mugil_AI_CoFounder_Workflow_and_UseCases.docx
Mugil Soft Solutions — Innovating Today. Empowering Tomorrow.
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, fill_hex):
    """Set shading color for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set padding for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_document():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Palette
    PRIMARY_COLOR = RGBColor(0, 51, 102)     # Deep Navy
    SECONDARY_COLOR = RGBColor(0, 102, 153) # Teal / Slate Blue
    DARK_TEXT = RGBColor(51, 51, 51)        # Charcoal Text
    LIGHT_BG_HEX = "F0F4F8"
    ALT_ROW_HEX = "F9FAFC"
    HEADER_BG_HEX = "003366"

    # Set Base Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = DARK_TEXT

    # --- Title Section ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("Mugil AI Co-Founder")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(28)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY_COLOR

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Technical Workflow Architecture & Operational Use Cases")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(16)
    run_sub.font.italic = True
    run_sub.font.color.rgb = SECONDARY_COLOR

    p_org = doc.add_paragraph()
    p_org.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_org = p_org.add_run("Mugil Soft Solutions — Innovating Today. Empowering Tomorrow.")
    run_org.font.size = Pt(10.5)
    run_org.font.color.rgb = RGBColor(128, 128, 128)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_heading_1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        run = h.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_COLOR
        return h

    def add_heading_2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        run = h.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = SECONDARY_COLOR
        return h

    def add_callout(text, title="NOTE:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, LIGHT_BG_HEX)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run_t = p.add_run(f"📌 {title} ")
        run_t.bold = True
        run_t.font.color.rgb = PRIMARY_COLOR
        run_b = p.add_run(text)
        run_b.font.size = Pt(10.5)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- Section 1: Executive Overview ---
    add_heading_1("1. Executive Overview & System Architecture")

    p = doc.add_paragraph(
        "The Mugil AI Co-Founder system is an autonomous multi-persona AI agent designed for Mugil Soft Solutions. "
        "It acts as a strategic technical and operational co-founder, assisting leadership, product development, engineering, "
        "and growth outreach while enforcing strict AI governance standards aligned with India's DPDP Act 2023."
    )
    p.paragraph_format.space_after = Pt(8)

    add_callout(
        "Every lead generated and every high-risk production action operates under a strict Human-in-the-Loop (HITL) gate. "
        "The system prepares draft outreach and analysis, but explicit founder approval is required before execution.",
        title="Responsible AI Commitment"
    )

    add_heading_2("1.1 Persona Sub-Agent Architecture")
    p = doc.add_paragraph("The engine features 8 specialized sub-agent personas routed by the central AgentRouter:")
    p.paragraph_format.space_after = Pt(6)

    personas = [
        ("Co-Founder & Strategy Orchestrator", "Central routing agent synthesizing strategy, alignment, and sprint planning."),
        ("CTO & Solution Architect", "Defines tech stack, modular clean code architecture, and API specs."),
        ("AI & ML Lead Engineer", "Oversees RAG vector retrieval, LLM model selection, and search grounding."),
        ("Responsible AI & Governance Officer", "Executes 15-point AI risk audits, DPDP Act 2023 compliance, and HITL checks."),
        ("Product Manager", "Manages MoSCoW MVP feature prioritization and development lifecycles."),
        ("Full-Stack Lead Developer", "Generates React/Vite, Node.js, and Python code standards."),
        ("Business & Market Specialist", "Evaluates total addressable market (TAM), unit economics, and value propositions."),
        ("Leads & Growth Specialist", "Searches live web for Ideal Customer Profile (ICP) leads and exports to Google Sheets.")
    ]

    table_p = doc.add_table(rows=1, cols=2)
    table_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_p.rows[0].cells
    hdr_cells[0].text = "Sub-Agent Persona"
    hdr_cells[1].text = "Core Role & Responsibility"
    for cell in hdr_cells:
        set_cell_background(cell, HEADER_BG_HEX)
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    for i, (name, role) in enumerate(personas):
        row_cells = table_p.add_row().cells
        bg = ALT_ROW_HEX if i % 2 == 1 else "FFFFFF"
        row_cells[0].text = name
        row_cells[1].text = role
        for cell in row_cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Section 2: Technical Workflows ---
    add_heading_1("2. Technical Workflow Specifications")

    add_heading_2("Workflow 1: Multi-Persona RAG Routing & Response Synthesis")
    steps_w1 = [
        ("Step 1: User Query Submission", "User submits a query via CLI command (`cli.py chat`) or programmatic API with an optional sub-agent persona tag (e.g. `/cto`, `/governance`)."),
        ("Step 2: RAG Context Retrieval", "KnowledgeBaseLoader performs term-frequency token matching across 29 indexed workspace documents (Docs, Portfolio, Knowledge Base, Templates, Memory)."),
        ("Step 3: HITL Risk Trigger Evaluation", "AgentRouter checks if query keywords contain high-risk triggers ('deploy to production', 'delete database', 'sign contract', 'price quote')."),
        ("Step 4: LLM / Template Generation", "Initializes Gemini 3.6 Flash with grounded context. If Gemini API is offline, falls back to guided structured offline response templates."),
        ("Step 5: Output Presentation", "Formats Markdown output with clear section headers, context document citations, and HITL warning banners if applicable.")
    ]

    for title, desc in steps_w1:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"• {title}: ")
        run_t.bold = True
        run_t.font.color.rgb = PRIMARY_COLOR
        p.add_run(desc)

    add_heading_2("Workflow 2: Live Lead Search & Google Sheets Synchronization")
    steps_w2 = [
        ("Step 1: Query & ICP Initialization", "User issues lead command (`cli.py leads --query \"...\" --sheet-name \"...\"`). LeadFinder merges query with Mugil's Ideal Customer Profile (ICP)."),
        ("Step 2: Prompt-Level Deduplication", "LeadFinder scans existing JSON lead files in `memory/leads/` and appends an exclusion prompt (`Do NOT include these previously found companies...`) to ensure fresh results."),
        ("Step 3: Web Search Grounding", "Gemini 3.6 Flash executes real-time web search via Google Search Grounding to identify verified target companies, buyer titles, and source URLs."),
        ("Step 4: Persistence & JSON/CSV Export", "Extracted structured leads are written locally to `memory/leads/leads_YYYYMMDD_HHMMSS.json` and `.csv`."),
        ("Step 5: Google Sheets Sync & Row Deduplication", "GoogleSheetsExporter connects via Service Account (`gspread`). It reads existing company names in Column 0 of the target Google Sheet and skips duplicates before appending new rows.")
    ]

    for title, desc in steps_w2:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"• {title}: ")
        run_t.bold = True
        run_t.font.color.rgb = PRIMARY_COLOR
        p.add_run(desc)

    add_heading_2("Workflow 3: AI Governance Gate & Risk Assessment Audit")
    p = doc.add_paragraph(
        "When auditing new software project proposals, GovernanceGateChecker classifies the project into one of 3 Risk Tiers:"
    )

    tiers = [
        ("Tier 1: Low Risk (Autonomous)", "Internal tools, static CLI apps. Requires basic checklists; approved automatically."),
        ("Tier 2: Medium Risk (Standard Review)", "Customer-facing web apps, internal data storage. Requires human sign-off and purpose limitation verification."),
        ("Tier 3: High Risk (Strict HITL Gate)", "Healthtech, fintech, biometric, or mass automated messaging. Mandates Data Protection Impact Assessment (DPIA), user consent logging, and explicit founder approval.")
    ]

    for t_name, t_desc in tiers:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"🔒 {t_name}: ")
        run_t.bold = True
        run_t.font.color.rgb = PRIMARY_COLOR
        p.add_run(t_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Section 3: Detailed Operational Use Cases ---
    add_heading_1("3. Operational Use Cases")

    # Use Case 1
    add_heading_2("Use Case 1: Automated Healthcare ICP Lead Discovery & Google Sheets Export")
    p = doc.add_paragraph()
    p.add_run("Actor: ").bold = True
    p.add_run("Growth & Sales Lead / Founder\n")
    p.add_run("Objective: ").bold = True
    p.add_run("Find verified Indian healthcare companies exploring digital transformation and automatically maintain a CRM lead list in Google Sheets.\n")
    p.add_run("Execution Command:\n").bold = True

    p_cmd = doc.add_paragraph()
    p_cmd.paragraph_format.left_indent = Inches(0.3)
    r_code = p_cmd.add_run(".venv\\Scripts\\python.exe cli.py leads --query \"Healthcare startups in India adopting AI\" --sheet-name \"Mugil AI Healthcare Leads\"")
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(9.5)
    r_code.font.color.rgb = PRIMARY_COLOR

    p_res = doc.add_paragraph()
    p_res.add_run("Workflow Outcome:\n").bold = True
    outcomes_uc1 = [
        "Live web search retrieves 5 verified companies with source URLs and target titles (e.g. Head of Digital Transformation).",
        "LeadFinder checks `memory/leads/` to prevent re-fetching previously found companies.",
        "Generates customized, draft first-touch openers for each company.",
        "GoogleSheetsExporter authenticates via `credentials.json`, checks Column 0 for duplicate company names, appends unique rows, and returns the shareable Google Sheet link."
    ]
    for o in outcomes_uc1:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.3)
        p_item.add_run(f"✓ {o}")

    # Use Case 2
    add_heading_2("Use Case 2: AI Governance Audit for Healthtech Proposal (DPDP Compliance)")
    p = doc.add_paragraph()
    p.add_run("Actor: ").bold = True
    p.add_run("Responsible AI Officer / Lead Engineer\n")
    p.add_run("Objective: ").bold = True
    p.add_run("Audit a proposed AI patient diagnostic assistant against India's DPDP Act 2023 and Mugil's 5 Responsible AI Principles.\n")
    p.add_run("Execution Command:\n").bold = True

    p_cmd2 = doc.add_paragraph()
    p_cmd2.paragraph_format.left_indent = Inches(0.3)
    r_code2 = p_cmd2.add_run(".venv\\Scripts\\python.exe cli.py audit --name \"Smart Clinic Assistant\" --desc \"AI tool processing patient electronic health records\" --domain \"Healthcare\"")
    r_code2.font.name = 'Consolas'
    r_code2.font.size = Pt(9.5)
    r_code2.font.color.rgb = PRIMARY_COLOR

    p_res2 = doc.add_paragraph()
    p_res2.add_run("Workflow Outcome:\n").bold = True
    outcomes_uc2 = [
        "System flags project as Tier 3: High Risk (Human Approval Required).",
        "Identifies 4 key risks: Consent management, purpose limitation, healthcare data privacy, and human oversight controls.",
        "Generates actionable mitigation steps and checklist score prior to sprint commitment."
    ]
    for o in outcomes_uc2:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.3)
        p_item.add_run(f"✓ {o}")

    # Use Case 3
    add_heading_2("Use Case 3: Interactive Technical Architecture Consultation (/cto)")
    p = doc.add_paragraph()
    p.add_run("Actor: ").bold = True
    p.add_run("Full-Stack Lead Developer / Solutions Architect\n")
    p.add_run("Objective: ").bold = True
    p.add_run("Consult the CTO sub-agent persona during an interactive terminal session to get approved technology stack standards.\n")
    p.add_run("Execution Workflow:\n").bold = True

    p_cmd3 = doc.add_paragraph()
    p_cmd3.paragraph_format.left_indent = Inches(0.3)
    r_code3 = p_cmd3.add_run("1. Launch Chat: .venv\\Scripts\\python.exe cli.py chat\n2. Switch Role: /cto\n3. Query: What is our standard full-stack web architecture?")
    r_code3.font.name = 'Consolas'
    r_code3.font.size = Pt(9.5)
    r_code3.font.color.rgb = PRIMARY_COLOR

    p_res3 = doc.add_paragraph()
    p_res3.add_run("Workflow Outcome:\n").bold = True
    outcomes_uc3 = [
        "Switches active persona to CTO & Solution Architect.",
        "Retrieves `technology-standards.md` from workspace knowledge base.",
        "Returns approved stack: React/Vite + Node.js/Python FastAPI + PostgreSQL + Redis with modular clean architecture guidance."
    ]
    for o in outcomes_uc3:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.3)
        p_item.add_run(f"✓ {o}")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Section 4: Configuration & Command Reference ---
    add_heading_1("4. Configuration & Environment Reference")

    table_cfg = doc.add_table(rows=1, cols=3)
    table_cfg.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_cfg.rows[0].cells
    hdr_cells[0].text = "Environment Variable"
    hdr_cells[1].text = "Purpose"
    hdr_cells[2].text = "Default / Example"
    for cell in hdr_cells:
        set_cell_background(cell, HEADER_BG_HEX)
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    config_items = [
        ("GEMINI_API_KEY", "Unlocks Gemini 3.6 Flash & Google Search grounding", "Configured in `.env`"),
        ("GEMINI_MODEL", "Specifies LLM model version", "`gemini-3.6-flash`"),
        ("GOOGLE_APPLICATION_CREDENTIALS", "Path to Service Account JSON for Google Sheets API", "`credentials.json`"),
        ("GSPREAD_CREDENTIALS", "Alternative path for Google Sheets credentials", "`config/credentials.json`")
    ]

    for i, (k, p_text, ex) in enumerate(config_items):
        row_cells = table_cfg.add_row().cells
        bg = ALT_ROW_HEX if i % 2 == 1 else "FFFFFF"
        row_cells[0].text = k
        row_cells[1].text = p_text
        row_cells[2].text = ex
        for cell in row_cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    # Footer
    p_ft = doc.add_paragraph()
    p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ft = p_ft.add_run("Mugil Soft Solutions — Innovating Today. Empowering Tomorrow.")
    r_ft.font.size = Pt(9.5)
    r_ft.font.italic = True
    r_ft.font.color.rgb = RGBColor(128, 128, 128)

    # Save document
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    out_path = docs_dir / "Mugil_AI_CoFounder_Workflow_and_UseCases.docx"
    doc.save(out_path)
    print(f"Document successfully created at: {out_path.resolve()}")


if __name__ == "__main__":
    create_document()
