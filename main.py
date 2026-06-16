import flet as ft
import flet.canvas as cv
import math
import os
import random

# ── SHARED CONSTANTS ──────────────────────────────────────────────────────────
ACCENT_COLOR   = "#F2A51B"
DIVIDER_COLOR  = "#B97012"
IC_BADGE       = "#F2A51B"
IC_BOOK        = "#C7D0D6"
IC_GROUPS      = "#7FA6B8"
IC_EMAIL       = "#D88C20"
IC_PHONE       = "#9FB8B5"
IC_INSTA       = "#E6B35A"
TEXT_COLOR     = "#FFF7EA"
SUBTLE_COLOR   = ft.Colors.with_opacity(0.78, "#FFF7EA")
BG_COLOR       = "#080706"
CARD_BG        = ft.Colors.with_opacity(0.18, "#0B0A08")
PANEL_BG       = ft.Colors.with_opacity(0.30, "#080706")
BORDER_COLOR   = ft.Colors.with_opacity(0.20, "#F2A51B")
MINE_BG_IMAGE  = "mine_background.png"

HEADER_SIZE    = 28
SUBHEADER_SIZE = 20
CONTENT_SIZE   = 14

# ── CONSTELLATION BACKGROUND (built ONCE, reused every page) ──────────────────
def _build_background_shapes():
    shapes = []
    TOTAL_NODES  = 320
    MAX_DISTANCE = 150
    nodes        = []

    for i in range(TOTAL_NODES):
        if i < int(TOTAL_NODES * 0.65):
            x_pos = int(random.gauss(960, 320))
            y_pos = int(random.gauss(350, 200))
        else:
            x_pos = int(random.gauss(150, 180))
            y_pos = int(random.gauss(150, 150))
        nodes.append({
            "x": max(0, min(1920, x_pos)),
            "y": max(0, min(1080, y_pos)),
            "radius": random.uniform(1.0, 2.5),
        })

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            n1, n2 = nodes[i], nodes[j]
            dist = math.hypot(n1["x"] - n2["x"], n1["y"] - n2["y"])
            if dist < MAX_DISTANCE:
                opacity = max(0.01, min(0.20, 1.0 - dist / MAX_DISTANCE))
                shapes.append(cv.Line(
                    x1=n1["x"], y1=n1["y"], x2=n2["x"], y2=n2["y"],
                    paint=ft.Paint(
                        color=ft.Colors.with_opacity(opacity, DIVIDER_COLOR),
                        stroke_width=0.8,
                    ),
                ))

    for node in nodes:
        shapes.append(cv.Circle(
            x=node["x"], y=node["y"], radius=node["radius"],
            paint=ft.Paint(
                color=ft.Colors.with_opacity(random.uniform(0.4, 0.85), ACCENT_COLOR),
                style=ft.PaintingStyle.FILL,
            ),
        ))
    return shapes

# Pre-compute once at import time — all pages share this


def build_background():
    return ft.Stack(
        expand=True,
        controls=[
            ft.Container(expand=True, bgcolor=BG_COLOR),
            ft.Image(
                src=MINE_BG_IMAGE,
                fit=ft.BoxFit.COVER,
                width=float("inf"),
                height=float("inf"),
                opacity=0.58,
            ),
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1.0, -1.0),
                    end=ft.Alignment(1.0, 1.0),
                    colors=[
                        ft.Colors.with_opacity(0.74, "#050403"),
                        ft.Colors.with_opacity(0.46, "#11100E"),
                        ft.Colors.with_opacity(0.82, "#050403"),
                    ],
                ),
            ),
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.18, "#D88208"),
            ),
        ],
    )


# ── TOP NAV ───────────────────────────────────────────────────────────────────
def build_top_nav(page: ft.Page, active_key: str):
    def go(route):
        def handler(e):
            page.go(route)
        return handler

    def nav_button(label, icon, route):
        is_active = active_key == route.strip("/")
        return ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(icon, size=15,
                            color=TEXT_COLOR if is_active else ACCENT_COLOR),
                    ft.Text(label, size=13, weight=ft.FontWeight.W_500,
                            color=TEXT_COLOR if is_active else ACCENT_COLOR),
                ],
                spacing=5,
                tight=True,
            ),
            on_click=go(route),
            style=ft.ButtonStyle(
                padding=ft.Padding(10, 6, 10, 6),
                bgcolor=ft.Colors.with_opacity(0.12, ACCENT_COLOR) if is_active
                        else ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.with_opacity(0.08, ACCENT_COLOR),
            ),
        )

    return ft.Container(
        bgcolor=ft.Colors.with_opacity(0.95, BG_COLOR),
        # ── taller navbar ──
        padding=ft.Padding(20, 14, 20, 14),
        border=ft.border.Border(
            bottom=ft.border.BorderSide(1, BORDER_COLOR)
        ),
        content=ft.Row(
            controls=[
                # ── UNAM logo replacing text ──
                ft.TextButton(
                    content=ft.Row([
                        ft.Image(
                            src="unam_logo.png",
                            width=70, height=70,
                            fit=ft.BoxFit.CONTAIN,
                            error_content=ft.Text(
                                "UNAM", size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ACCENT_COLOR,
                            ),
                        ),
                        ft.Column([
                            ft.Text("Waarde Akawa", size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_COLOR),
                            ft.Text("Computer Programming I · 2026",
                                    size=10, color=SUBTLE_COLOR),
                        ], spacing=1, tight=True),
                    ], spacing=10, tight=True),
                    on_click=go("/home"),
                    style=ft.ButtonStyle(overlay_color=ft.Colors.TRANSPARENT),
                ),
                ft.Row(
                    controls=[
                        nav_button("Home",       ft.Icons.HOME,        "/home"),
                        nav_button("Timeline",   ft.Icons.TIMELINE,    "/timeline"),
                        nav_button("GitHub",     ft.Icons.CODE,        "/github"),
                        nav_button("MATLAB Hub", ft.Icons.SCHOOL,      "/matlab"),
                        nav_button("Demos",      ft.Icons.PLAY_CIRCLE, "/demos"),
                        nav_button("Blog",       ft.Icons.ARTICLE,     "/blog"),
                        nav_button("Contact",    ft.Icons.MAIL,        "/contact"),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.END,
                    wrap=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


# ── FULL-PAGE SHELL ───────────────────────────────────────────────────────────
def page_shell(page: ft.Page, active_key: str, body: ft.Control):
    nav = build_top_nav(page, active_key)
    scrollable = ft.Column(
        controls=[
            ft.Container(content=body, padding=ft.Padding(30, 30, 30, 40), expand=True)
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
    page_col = ft.Column(
        controls=[nav, scrollable],
        expand=True,
        spacing=0,
    )
    return ft.Stack(
        controls=[build_background(), page_col],
        expand=True,
    )


# ── HELPER WIDGETS ────────────────────────────────────────────────────────────
def math_module_card(title, description, top_formula,
                     bottom_formula=None, plain_suffix=""):
    formula_controls = []
    if bottom_formula:
        formula_controls += [
            ft.Text(top_formula, size=14, color="#F1D19C",
                    weight=ft.FontWeight.BOLD),
            ft.Container(width=160, height=1, bgcolor=DIVIDER_COLOR,
                         margin=ft.Margin(top=2, bottom=2)),
            ft.Text(bottom_formula, size=14, color="#F1D19C",
                    weight=ft.FontWeight.BOLD),
        ]
    else:
        formula_controls.append(
            ft.Text(top_formula, size=14, color="#F1D19C", italic=True)
        )
    if plain_suffix:
        formula_controls.append(
            ft.Text(plain_suffix, size=12, color=SUBTLE_COLOR)
        )

    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
            ft.Text(description, size=CONTENT_SIZE, color=TEXT_COLOR),
            ft.Container(
                content=ft.Column(
                    formula_controls,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=12,
                bgcolor=ft.Colors.with_opacity(0.15, BG_COLOR),
                border=ft.Border.all(1, BORDER_COLOR),
                border_radius=6,
            ),
        ], spacing=10),
        padding=20,
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=10,
        col={"sm": 12, "md": 6, "lg": 4},
    )


def blog_post_preview(title, description):
    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=SUBHEADER_SIZE,
                    weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
            ft.Text(description, size=CONTENT_SIZE, color=TEXT_COLOR),
            ft.TextButton("Read full post…",
                          style=ft.ButtonStyle(color=ACCENT_COLOR)),
        ], spacing=5),
        margin=ft.Margin(bottom=20),
        padding=15,
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=10,
    )


def cert_card(img_path):
    return ft.Container(
        content=ft.Image(src=img_path, border_radius=10, fit=ft.BoxFit.COVER),
        padding=10,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10,
                            color=ft.Colors.with_opacity(0.26, ft.Colors.BLACK)),
        col={"sm": 12, "md": 6},
    )


def skill_chip(label, icon, color):
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, size=16, color=color),
            ft.Text(label, size=13, color=TEXT_COLOR,
                    weight=ft.FontWeight.W_500),
        ], spacing=6, tight=True),
        padding=ft.Padding(12, 8, 12, 8),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.25, color)),
        border_radius=20,
        bgcolor=ft.Colors.with_opacity(0.08, color),
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE BODIES
# ══════════════════════════════════════════════════════════════════════════════

# ── HOME ──────────────────────────────────────────────────────────────────────
def home_body():
    profile_section = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"sm": 12, "md": 5},
                content=ft.Container(
                    width=280, height=340,
                    border_radius=20,
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.42, ACCENT_COLOR)),
                    padding=10,
                    content=ft.Image(src="Waarde.jpeg", fit=ft.BoxFit.COVER,
                                     border_radius=14),
                ),
            ),
            ft.Container(
                col={"sm": 12, "md": 7},
                padding=ft.Padding(left=15, right=15, top=10, bottom=10),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Column(spacing=4, controls=[
                            ft.Text("Waarde Akawa", size=36,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_COLOR),
                            ft.Text("Mining Engineering Student | GitHub Manager",
                                    size=16, color=ACCENT_COLOR,
                                    weight=ft.FontWeight.W_500),
                        ]),
                        ft.Divider(color=DIVIDER_COLOR, height=10, thickness=1),
                        ft.Column(spacing=8, controls=[
                            ft.Text("Project Brief", size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_COLOR),
                            ft.Text(
                                "Serving as the GitHub Manager for Group 10 in the "
                                "Mobile App Development For Computer Programming I, "
                                "I manage repository coordination, version control, "
                                "merge documentation, and technical evidence for "
                                "Blast Assist, our Safety Blasting Arrangement App "
                                "for mining calculations, GIS logging, and community alerts.",
                                size=15, color=SUBTLE_COLOR,
                            ),
                        ]),
                        ft.Column(spacing=5, controls=[
                            ft.Row([
                                ft.Icon(ft.Icons.BADGE, color=IC_BADGE, size=16),
                                ft.Text("Student Number: 225087111",
                                        size=14, color=SUBTLE_COLOR),
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.BOOK_ROUNDED, color=IC_BOOK, size=16),
                                ft.Text("Module: Computer Programming I",
                                        size=14, color=SUBTLE_COLOR),
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.GROUPS_3, color=IC_GROUPS, size=16),
                                ft.Text("Assigned Team: Group 10 (Blast Assist)",
                                        size=14, color=SUBTLE_COLOR),
                            ]),
                        ]),
                    ],
                ),
            ),
            
        ],
        spacing=30,
        run_spacing=30,
    )

    # ── SKILLS & TECH SECTION (the area indicated in the image) ──
    skills_section = ft.Container(
        margin=ft.Margin(top=40, bottom=0, left=0, right=0),
        content=ft.Column([
            ft.Row([
                ft.Container(
                    width=4, height=30, bgcolor=ACCENT_COLOR,
                    border_radius=2,
                    margin=ft.Margin(right=12, top=0, left=0, bottom=0),
                ),
                ft.Text("Skills & Technologies",
                        size=SUBHEADER_SIZE + 2,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_COLOR),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=6),
            ft.Text(
                "A snapshot of the tools, frameworks, and languages I apply across "
                "the Blast Assist project and my academic coursework at UNAM.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            ft.Container(height=18),

            # Row 1 — Languages
            ft.Text("Languages", size=13, color=ACCENT_COLOR,
                    weight=ft.FontWeight.W_600),
            ft.Container(height=6),
            ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
                skill_chip("Python",      ft.Icons.CODE,            "#7FA6B8"),
                skill_chip("JavaScript",  ft.Icons.JAVASCRIPT,      "#F2A51B"),
                skill_chip("JSX / React", ft.Icons.WIDGETS,         "#C7D0D6"),
                skill_chip("MATLAB",      ft.Icons.CALCULATE,       "#E6B35A"),
            ]),
            ft.Container(height=16),

            # Row 2 — Frameworks & Tools
            ft.Text("Frameworks & Tools", size=13, color=ACCENT_COLOR,
                    weight=ft.FontWeight.W_600),
            ft.Container(height=6),
            ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
                skill_chip("Flet",          ft.Icons.DESKTOP_WINDOWS, "#7FA6B8"),
                skill_chip("React Native",  ft.Icons.PHONE_ANDROID,   "#C7D0D6"),
                skill_chip("Expo",          ft.Icons.ROCKET_LAUNCH,   "#D88C20"),
                skill_chip("Firebase",      ft.Icons.LOCAL_FIRE_DEPARTMENT, "#F2A51B"),
                skill_chip("AsyncStorage",  ft.Icons.CLOUD_SYNC,      "#9FB8B5"),
                skill_chip("Git & GitHub",  ft.Icons.MERGE_TYPE,      "#E6B35A"),
            ]),
            ft.Container(height=16),

            # Row 3 — Engineering domains
            ft.Text("Engineering Domains", size=13, color=ACCENT_COLOR,
                    weight=ft.FontWeight.W_600),
            ft.Container(height=6),
            ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
                skill_chip("Civil Engineering",        ft.Icons.DOMAIN,          "#C7D0D6"),
                skill_chip("Blasting Safety Systems",  ft.Icons.BUILD_CIRCLE,    "#F2A51B"),
                skill_chip("NoSQL / Firestore",        ft.Icons.STORAGE,         "#7FA6B8"),
                skill_chip("System Architecture",      ft.Icons.ACCOUNT_TREE,    "#D88C20"),
                skill_chip("Cross-Platform Dev",       ft.Icons.DEVICES,         "#9FB8B5"),
            ]),

            ft.Container(height=30),
            ft.Divider(color=DIVIDER_COLOR, thickness=1),

            # Quick-stats bar
            ft.Container(height=10),
            ft.ResponsiveRow(
                controls=[
                    _stat_card("8",   "MATLAB Courses",   ft.Icons.SCHOOL,           "#E6B35A"),
                    _stat_card("15%", "CA Weighting",     ft.Icons.GRADE,            "#F2A51B"),
                    _stat_card("16",  "Team Members",     ft.Icons.GROUPS_3,         "#9FB8B5"),
                    _stat_card("5",   "Sprint Phases",    ft.Icons.TIMELINE,         "#7FA6B8"),
                ],
                spacing=15, run_spacing=15,
            ),
        ]),
        padding=ft.Padding(30, 28, 30, 28),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=14,
        bgcolor=PANEL_BG,
    )

    return ft.Column(
        expand=True,
        controls=[
            profile_section, 
            skills_section,
            ft.Container(expand=True),
            ft.Divider(color=DIVIDER_COLOR, height=60),
            ft.Column(
                [
                    ft.Text(
                        "© 2026 Waarde Akawa | Mobile App Development For Computer Programming ",
                        color=SUBTLE_COLOR,
                        size=12, italic=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=float("inf"),
            ),
            ft.Container(height=20),
        ], 
        spacing=0
    )



def _stat_card(value, label, icon, color):
    return ft.Container(
        col={"xs": 6, "sm": 6, "md": 3},
        content=ft.Column([
            ft.Icon(icon, size=28, color=color),
            ft.Text(value, size=32, weight=ft.FontWeight.BOLD,
                    color=TEXT_COLOR),
            ft.Text(label, size=12, color=SUBTLE_COLOR,
                    text_align=ft.TextAlign.CENTER),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        padding=20,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, color)),
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.07, color),
    )


# ── TIMELINE ─────────────────────────────────────────────────────────────────
def timeline_body():
    entries = [
        ("Weeks 1–2: Initiation & Architecture",
         "Helped align repository setup with the SRS structure, team roles, "
         "and the Blast Assist requirements baseline.",
         ft.Icons.ASSIGNMENT_TURNED_IN, "#F2A51B", "SRS BASELINE"),
        ("Weeks 3–5: UI/UX & Frontend Scaffolding",
         "Tracked frontend updates for the engineer dashboard, community alerts, "
         "and mobile screens while keeping evidence organized in GitHub.",
         ft.Icons.DASHBOARD_CUSTOMIZE, "#7FA6B8", "UI EVIDENCE"),
        ("Weeks 6–8: Core Route & Navigation Engineering",
         "Supported version control for calculator, GIS mapping, history, and "
         "notification features described in the SRS.",
         ft.Icons.ALT_ROUTE, "#E6B35A", "FEATURE TRACKING"),
        ("Weeks 9–10: Optimization & Offline Queue Strategy",
         "Reviewed repository updates for offline-first behavior, Firebase syncing, "
         "and blast calculation history records.",
         ft.Icons.CLOUD_SYNC, "#9FB8B5", "SYNC EVIDENCE"),
        ("Weeks 11–12+: Deployment & Quality Assurance",
         "Collected commit history, screenshots, and review notes to support final "
         "submission evidence against the SRS system benchmarks.",
         ft.Icons.VERIFIED, "#D88C20", "PRODUCTION QA"),
    ]

    cards = [
        ft.Container(
            padding=20,
            margin=ft.Margin(bottom=15, top=0, left=0, right=0),
            border=ft.Border.all(1, BORDER_COLOR),
            border_radius=12,
            bgcolor=CARD_BG,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Icon(icon_node, color=node_color, size=24),
                        margin=ft.Margin(right=10, top=2, left=0, bottom=0),
                    ),
                    ft.Column(expand=True, spacing=8, controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(title, size=18,
                                        weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                                ft.Container(
                                    content=ft.Text(badge_text, size=11,
                                                    color=TEXT_COLOR,
                                                    weight=ft.FontWeight.W_600),
                                    bgcolor=ft.Colors.with_opacity(0.18, ACCENT_COLOR),
                                    padding=10, border_radius=15,
                                ),
                            ],
                        ),
                        ft.Text(desc, size=CONTENT_SIZE, color=SUBTLE_COLOR),
                    ]),
                ],
            ),
        )
        
        for title, desc, icon_node, node_color, badge_text in entries
    ]

    return ft.Column(controls=[
        ft.Text("Project Timeline", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "As the GitHub Manager of Group 10, I supported the technical "
                "development of Blast Assist by maintaining repository structure, "
                "tracking contributions, coordinating merges, and keeping the code "
                "evidence aligned with the SRS requirements for calculations, GIS "
                "logging, Firebase data storage, and community safety notifications.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=25, top=10),
        ),
        
        *cards,
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "© 2026 Waarde Akawa | Mobile App Development For Computer Programming ",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ], spacing=0)


# ── GITHUB ────────────────────────────────────────────────────────────────────
def github_body():
    return ft.Column(controls=[
        ft.Text("GitHub Evidence & Documentation", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "As the Group 10 GitHub Manager, I organized the repository workflow, "
                "tracked commits, reviewed merge activity, and kept our development "
                "evidence connected to the SRS for Blast Assist. My role focused on "
                "clear version control, branch discipline, and reliable documentation "
                "of the team's technical progress.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=20, top=10),
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Blast Assist Repository Impact Summary",
                        size=SUBHEADER_SIZE, weight=ft.FontWeight.BOLD,
                        color=ACCENT_COLOR),
                ft.Text(
                    "Problem Statement: Blasting teams need a dependable digital system "
                    "for calculation records, GIS-tagged blast logs, Firebase data, and "
                    "community alert evidence.\n\n"
                    "Individual Resolution: As GitHub Manager, I helped keep the project "
                    "repository organized so calculator logic, safety notification work, "
                    "and SRS documentation could be traced through commits, branches, "
                    "and review records.",
                    size=CONTENT_SIZE, color=TEXT_COLOR,
                ),
            ]),
            padding=20,
            bgcolor=CARD_BG,
            border_radius=10,
            margin=ft.Margin(bottom=20),
        ),
        ft.Divider(height=10, thickness=1,
                   color=BORDER_COLOR),
        ft.Text("Project Repository", size=SUBHEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.ElevatedButton(
                "View Production Repository on GitHub",
                icon=ft.Icons.CODE,
                style=ft.ButtonStyle(
                    color=BG_COLOR, bgcolor=ACCENT_COLOR,
                    padding=20,
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                url="https://github.com/waardeakawa-sys/UNAM-I36991CP-GROUP-10-TOOLBOX.git",
            ),
            padding=ft.Padding(left=40, right=40),
        ),
        ft.Container(height=20),
        ft.Text("Verifiable Pull Request & Code Review Logs",
                size=SUBHEADER_SIZE, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.ResponsiveRow([
            ft.Container(
                content=ft.Column(controls=[
                    ft.ListTile(
                leading=ft.Icon(ft.Icons.CALL_MERGE, color="#9FB8B5"),
                        title=ft.Text("Repository Branch and Merge Evidence",
                                      color=TEXT_COLOR,
                                      weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(
                            "Tracked Blast Assist feature branches and merge records",
                            color=ACCENT_COLOR),
                    ),
                    ft.Container(
                        content=ft.Image(src="github_contr.png",
                                         border_radius=4, fit=ft.BoxFit.COVER),
                        padding=ft.Padding(left=16, right=16, bottom=16),
                    ),
                ], spacing=0),
                col={"sm": 12, "md": 6},
                bgcolor=CARD_BG,
                border_radius=8,
            ),
            ft.Container(
                content=ft.Column(controls=[
                    ft.ListTile(
                leading=ft.Icon(ft.Icons.RATE_REVIEW, color=ACCENT_COLOR),
                        title=ft.Text("Feature: Blast Assist Screen Updates",
                                      color=TEXT_COLOR,
                                      weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(
                            "Documented UI and SRS-aligned implementation updates",
                            color=ACCENT_COLOR),
                    ),
                    ft.Container(
                        content=ft.Image(src="report.png", height=275,
                                         border_radius=4, fit=ft.BoxFit.COVER),
                        padding=ft.Padding(left=16, right=16, bottom=16),
                    ),
                ], spacing=0),
                col={"sm": 12, "md": 6},
                bgcolor=CARD_BG,
                border_radius=8,
            ),
        ], spacing=15),
        ft.Container(height=15),
        ft.Container(
            content=ft.Column(controls=[
                ft.ListTile(
                leading=ft.Icon(ft.Icons.HISTORY, color="#7FA6B8"),
                    title=ft.Text("Development Commit History Screenshots",
                                  color=TEXT_COLOR, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(
                        "Chronological stream of verified code repository updates",
                        color=ACCENT_COLOR),
                ),
                ft.Container(
                    content=ft.Image(src="history.png",
                                     border_radius=4, fit=ft.BoxFit.COVER),
                    padding=ft.Padding(left=16, right=16, bottom=16),
                ),
            ], spacing=0),
            bgcolor=CARD_BG,
            border_radius=8,
        ),
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "© 2026 Waarde Akawa | Mobile App Development For Computer Programming ",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ], spacing=10)


# ── MATLAB ────────────────────────────────────────────────────────────────────
def matlab_body():
    images = [
        "matlab1.png", "matlab2.png", "matlab3.png", "matlab4.png",
        "matlab5.png", "matlab6.png", "matlab7.png", "matlab8.png",
    ]
    labels = {
        "matlab1.png": "Simulink Onramp",
        "matlab2.png": "MATLAB Onramp",
        "matlab3.png": "Machine Learning Onramp",
        "matlab4.png": "MATLAB Desktop Tools and Troubleshooting Scripts",
        "matlab5.png": "Explore Data with MATLAB Plots",
        "matlab6.png": "Calculations with Vectors and Matrices",
        "matlab7.png": "Make and Manipulate Matrices",
        "matlab8.png": "Simulink Fundamentals",
    }

    return ft.Column(controls=[
        ft.Text("MATLAB Academic Hub", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "Verified course completions from the MathWorks Learning Center. "
                "All 8 self-paced certificates were earned as part of the Computer "
                "Programming I module requirements for Semester 1, 2026.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=20, top=10),
        ),
        ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"xs": 12, "sm": 6, "md": 3},
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            cert_card(img),
                            ft.Text(labels.get(img, "MATLAB Course"),
                                    size=14, weight=ft.FontWeight.W_500,
                                    color=TEXT_COLOR,
                                    text_align=ft.TextAlign.CENTER),
                        ],
                    ),
                )
                for img in images
            ],
            spacing=10, run_spacing=20,
        ),
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "© 2026 Waarde Akawa | Mobile App Development For Computer Programming ",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ])


# ── DEMOS ─────────────────────────────────────────────────────────────────────
def demos_body(page: ft.Page):
    return ft.Column(
        controls=[
            ft.Column(
                [
                    ft.Text("Blast Assist System Demonstrations", size=HEADER_SIZE,
                            weight=ft.FontWeight.W_800, color=TEXT_COLOR,
                            style=ft.TextStyle(letter_spacing=0.5)),
                    # Changed color to a lighter, readable golden-tinted white
                    ft.Text("Interactive media updates and core logic validations.", size=14, color=ft.Colors.with_opacity(0.7, TEXT_COLOR)),
                ],
                spacing=4,
            ),
            ft.Container(
                width=float("inf"),
                height=260,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1.0, -1.0),
                    end=ft.Alignment(1.0, 1.0),
                    # Changed gradient to blend from a deep gold-tinted charcoal into pure black
                    colors=["#14110C", "#000000"],
                ),
                # Replaced harsh white border with a very subtle bronze-gold border that matches the theme
                border=ft.Border.all(1, ft.Colors.with_opacity(0.12, ACCENT_COLOR)),
                border_radius=16,
                padding=24,
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text("VIDEO RESOURCE", size=10, weight="bold", color=ACCENT_COLOR),
                                    bgcolor=ft.Colors.with_opacity(0.1, ACCENT_COLOR),
                                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                                    border_radius=20,
                                ),
                                ft.Text("Play Blast Assist Demo Video", color=TEXT_COLOR, size=20, weight="bold"),
                                # Changed color to a crisp, readable opaque tone instead of the dark blue-gray
                                ft.Text("Review system data processing architecture pipelines live.", color=ft.Colors.with_opacity(0.6, TEXT_COLOR), size=13),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.BLACK),
                                            ft.Text("Click here to Watch my project contribution video", color=ft.Colors.BLACK, weight="bold"),
                                        ],
                                        spacing=8,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=ACCENT_COLOR,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.Padding.symmetric(horizontal=20, vertical=12)
                                    ),
                                    url="https://unam164-my.sharepoint.com/:v:/g/personal/225087111_students_unam_na/IQCScx0NhGG4SJao-XrtRHOyAaj6jqKUri00VHj3Y-TZ8PE?e=vD6fIm",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            expand=True,
                            spacing=8,
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED, size=80, color=ACCENT_COLOR),
                            alignment=ft.Alignment(0.0, 0.0),
                            expand=True,
                        ),
                    ],
                ),
            ),
            ft.Container(
                padding=ft.Padding.symmetric(vertical=10),
                content=ft.Divider(height=1, color=ft.Colors.with_opacity(0.08, TEXT_COLOR))
            ),
            ft.Text("Confidence in Concepts: System Mathematics",
                    size=SUBHEADER_SIZE, weight=ft.FontWeight.W_700, color=TEXT_COLOR),
            ft.ResponsiveRow(
                [
                    math_module_card(
                        "Blast Calculation Workflow",
                        "Digital tracking of blast inputs, predicted outputs, and saved history records.",
                        "Workflow: Inputs -> Calculate -> Save History",
                    ),
                    math_module_card(
                        "Burden and Spacing Logic",
                        "SRS-based formulas used to estimate hole burden, spacing, and drilling depth.",
                        "Spacing = 1.15 x Burden",
                        "Depth = Bench Height + Sub-drilling",
                        "Blast Pattern Calculation",
                    ),
                    math_module_card(
                        "GIS Blast Logging",
                        "Coordinate-based records linking each blast calculation to the selected mine location.",
                        "Record Mapping: Coordinates || Landscape || History",
                    ),
                    math_module_card(
                        "Community Safety Alerts",
                        "Notification planning for registered community members within the blast radius.",
                        "Alert Window: Blast Time - 1 Hour",
                        None,
                        "Firebase Cloud Messaging Requirement",
                    ),
                ],
                spacing=24,
                run_spacing=24,
            ),
            
            ft.Divider(color=DIVIDER_COLOR, height=60),
            ft.Column(
                [
                    ft.Text(
                        "© 2026 Waarde Akawa | Mobile App Development For Computer Programming",
                        color=SUBTLE_COLOR,
                        size=12, italic=True,
                        text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=float("inf"), # Forces the alignment container to span the full window width
            ),
            ft.Container(height=20),

        ],
        spacing=24,
    )


# ── BLOG ──────────────────────────────────────────────────────────────────────
def blog_body():
    return ft.Column(controls=[
        ft.Text("Technical Engineering Blog", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "A sequence of design analyses explaining our methodologies, "
                "implementation roadmaps, and optimization milestones completed "
                "during the development of Blast Assist for the University of Namibia.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=30, top=10),
        ),

        # ── Blog Post 1 ──────────────────────────────────────────────────────
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "Branching Strategy for a Multi-Role Development Team",
                    size=18, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR,
                ),
                ft.Container(height=10),
                ft.Text(
                    "Managing version control for a 15-member team across 5 sub-roles is no small task. "
                    "As the GitHub Manager for Blast Assist, my primary responsibility was to design and "
                    "enforce a branching strategy that allowed parallel development without breaking the "
                    "main codebase.\n\n"
                    "We adopted a modified Git Flow model where main held only production-ready code, "
                    "develop served as the integration branch for all features, individual feature branches "
                    "were created per task such as the blast calculator and FCM notifications, and hotfix "
                    "branches handled urgent patches directly off main.\n\n"
                    "Each sub-team worked exclusively on their own feature branches. No one was allowed "
                    "to push directly to main or develop. All changes went through Pull Requests with at "
                    "least one peer review before merging.\n\n"
                    "This structure meant that when the Firebase Lead was building Firestore schemas and "
                    "the UI/UX team was designing the community alert screen simultaneously, their work "
                    "never collided. Merge conflicts were isolated to the develop branch, where they could "
                    "be resolved in a controlled environment before reaching production.\n\n"
                    "The biggest lesson: branch protection rules are not optional on a team of this size. "
                    "Enforcing them from day one saved us from at least three potentially breaking merges "
                    "during the notification system integration phase.",
                    size=CONTENT_SIZE, color=TEXT_COLOR,
                ),
            ]),
            padding=ft.Padding(left=20, right=20, top=20, bottom=20),
            border=ft.border.all(1, DIVIDER_COLOR),
            border_radius=10,
            margin=ft.Margin(bottom=20, top=0, left=0, right=0),
        ),

        # ── Blog Post 2 ──────────────────────────────────────────────────────
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "Version Control as a Safety Net in Mining Software",
                    size=18, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR,
                ),
                ft.Container(height=10),
                ft.Text(
                    "In mining software, a calculation error is not just a bug — it is a safety risk. "
                    "Blast Assist computes explosive quantities, hole depth, burden, and spacing values "
                    "that directly inform real-world blasting decisions. This made traceability in our "
                    "version control system a critical engineering requirement, not just a best practice.\n\n"
                    "Every commit in our repository followed a structured convention covering new features, "
                    "bug and formula corrections, documentation updates, code refactoring, and test additions. "
                    "This made the Git log readable as an audit trail. If the burden formula (B = K × d) "
                    "was modified, the commit history showed exactly who changed it, when, and why.\n\n"
                    "We also used semantic versioning tied to GitHub Releases, progressing from an offline "
                    "calculator in the first release, through Firebase authentication and the FCM force "
                    "notification system, all the way to the final production build submission.\n\n"
                    "GitHub Actions was configured to run automated linting and build checks on every PR "
                    "targeting develop. This meant broken code was caught before a single reviewer even "
                    "opened the PR. For a safety-critical application like Blast Assist, this layer of "
                    "automated verification was non-negotiable.",
                    size=CONTENT_SIZE, color=TEXT_COLOR,
                ),
            ]),
            padding=ft.Padding(left=20, right=20, top=20, bottom=20),
            border=ft.border.all(1, DIVIDER_COLOR),
            border_radius=10,
            margin=ft.Margin(bottom=20, top=0, left=0, right=0),
        ),

        # ── Blog Post 3 ──────────────────────────────────────────────────────
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "Coordinating Offline-First Features Across a Distributed Team",
                    size=18, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR,
                ),
                ft.Container(height=10),
                ft.Text(
                    "One of the most technically complex aspects of Blast Assist is its offline-first "
                    "architecture. The app must function in remote mine sites with zero network signal, "
                    "then synchronize all logged blast data to Firebase Firestore once connectivity is "
                    "restored. Coordinating this across a distributed team of 15 developers introduced "
                    "significant version control challenges.\n\n"
                    "The core problem was dependency sequencing. The offline SQLite cache layer had to be "
                    "built before the Firebase sync logic could be tested, which itself had to be stable "
                    "before the UI team could wire up the history tab. If anyone merged incomplete work "
                    "into develop, it blocked two other sub-teams downstream.\n\n"
                    "To solve this, I introduced a dependency map in our repository's README, flowing from "
                    "the SQLite Local Cache through the Firebase Sync Module, into the History UI, and "
                    "finally the Blast Log Display. Each team was required to tag their branch as "
                    "ready-for-integration only when their module met the interface contract defined in "
                    "our shared API spec document. This prevented premature merges that would have "
                    "cascaded into broken builds.\n\n"
                    "The WorkManager and Background Tasks sync modules were the most conflict-prone files "
                    "in the entire project, modified by both the Firebase Lead and Lead Developer teams. "
                    "We resolved this by making those files owned exclusively by one branch at a time, "
                    "with a formal handoff commit marking the transfer.\n\n"
                    "By the time we reached our third release milestone, our develop branch had zero "
                    "unresolved conflicts and every offline calculation log was syncing correctly to "
                    "Firestore within 30 seconds of network restoration — a direct result of disciplined "
                    "version control from the start of the project.",
                    size=CONTENT_SIZE, color=TEXT_COLOR,
                ),
            ]),
            padding=ft.Padding(left=20, right=20, top=20, bottom=20),
            border=ft.border.all(1, DIVIDER_COLOR),
            border_radius=10,
            margin=ft.Margin(bottom=20, top=0, left=0, right=0),
        ),

        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "© 2026 Waarde Akawa | Mobile App Development For Computer Programming",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"),
        ),
        ft.Container(height=20),
    ])

# ── CONTACT ───────────────────────────────────────────────────────────────────
def contact_body(page: ft.Page):
    name_field  = ft.TextField(label="Name",    border_color=ACCENT_COLOR,
                                color=TEXT_COLOR, cursor_color=ACCENT_COLOR)
    email_field = ft.TextField(label="Email",   border_color=ACCENT_COLOR,
                                color=TEXT_COLOR)
    msg_field   = ft.TextField(label="Message", multiline=True, min_lines=3,
                                border_color=ACCENT_COLOR, color=TEXT_COLOR)

    return ft.Column(controls=[
        ft.Text("Contact Me", size=32, weight=ft.FontWeight.BOLD,
                color=TEXT_COLOR),
        ft.Container(
            padding=20,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        padding=20,
                        content=ft.Column([
                            ft.Text(
                                "I am always open to new academic collaborations, "
                                "development opportunities, or discussions surrounding "
                                "mining safety systems, GitHub workflow, and civil engineering software. "
                                "Drop me a message below to connect!",
                                size=16, color=TEXT_COLOR,
                                text_align=ft.TextAlign.LEFT,
                            ),
                            ft.Container(height=15),
                            ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.BADGE, color=ACCENT_COLOR, size=18),
                                    ft.Text("Student Number: ", weight=ft.FontWeight.BOLD,
                                            color=TEXT_COLOR, size=15),
                                    ft.Text("225087111",
                                            color=SUBTLE_COLOR, size=15),
                                ], spacing=5),
                                ft.Row([
                                    ft.Icon(ft.Icons.CODE, color=ACCENT_COLOR, size=18),
                                    ft.Text("Role: ", weight=ft.FontWeight.BOLD,
                                            color=TEXT_COLOR, size=15),
                                    ft.Text("GitHub Manager",
                                            color=SUBTLE_COLOR, size=15),
                                ], spacing=5),
                                ft.Row([
                                    ft.Icon(ft.Icons.GROUPS_3, color=ACCENT_COLOR, size=18),
                                    ft.Text("Project: ", weight=ft.FontWeight.BOLD,
                                            color=TEXT_COLOR, size=15),
                                    ft.Text("Group 10 - Blast Assist",
                                            color=SUBTLE_COLOR, size=15),
                                ], spacing=5),
                            ], spacing=10),
                        ])
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 5},
                        padding=30,
                        bgcolor=PANEL_BG,
                        border=ft.Border.all(
                            1, BORDER_COLOR),
                        border_radius=20,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                name_field, email_field, msg_field,
                                ft.ElevatedButton(
                                    "Send Message",
                                    style=ft.ButtonStyle(bgcolor=DIVIDER_COLOR,
                                                         color=TEXT_COLOR),
                                    width=float("inf"),
                                    on_click=lambda _: page.launch_url(
                                        f"mailto:"
                                        f"?subject=Message from {name_field.value}"
                                        f"&body=From: {email_field.value}"
                                        f"%0D%0A%0D%0A{msg_field.value}"
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ),
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "© 2026 Waarde Akawa | Mobile App Development For Computer Programming",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ])


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main(page: ft.Page):
    page.title = "Web Portfolio — Waarde Akawa"
    page.assets_dir = "./assets"
    page.padding = 0
    page.scroll = "none"
    page.bgcolor = BG_COLOR

    def route_change(e):
        page.controls.clear()
        route = page.route or "/home"

        route_map = {
            "/home":     ("home",     home_body()),
            "/timeline": ("timeline", timeline_body()),
            "/github":   ("github",   github_body()),
            "/matlab":   ("matlab",   matlab_body()),
            "/demos":    ("demos",    demos_body(page)),
            "/blog":     ("blog",     blog_body()),
            "/contact":  ("contact",  contact_body(page)),
        }

        key, body = route_map.get(route, route_map["/home"])
        page.add(page_shell(page, key, body))
        page.update()

    page.on_route_change = route_change
    page.go("/home")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        assets_dir="assets",
        host="0.0.0.0",
        port=port,
    )
