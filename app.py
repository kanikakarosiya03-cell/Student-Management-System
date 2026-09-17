"""
School Management System — Premium Streamlit Edition
======================================================
A privacy-first, SaaS-style School Management System built on top of the
original CLI-based OOP application (Student / Teacher / abstract Person
classes with JSON persistence).

Run with:
    python -m streamlit run app.py
"""

# =============================================================================
# IMPORTS
# =============================================================================
import json
import re
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

import streamlit as st
import pandas as pd


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="School Manager | Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# CSS — PREMIUM DARK THEME
# =============================================================================
def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --bg: #0b0d12;
            --surface: #12151c;
            --surface-2: #171b24;
            --border: #262b36;
            --text-primary: #f5f6f8;
            --text-secondary: #c3c8d1;
            --text-muted: #8a90a0;
            --accent: #7c6cf0;
            --accent-soft: rgba(124, 108, 240, 0.14);
            --success: #34d399;
            --success-soft: rgba(52, 211, 153, 0.12);
            --warning: #fbbf24;
            --warning-soft: rgba(251, 191, 36, 0.12);
            --error: #f87171;
            --error-soft: rgba(248, 113, 113, 0.12);
        }

        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", -apple-system, sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at top left, #10131a 0%, #0b0d12 45%, #090a0e 100%);
            color: var(--text-primary);
        }

        section[data-testid="stSidebar"] {
            background: #0d0f15;
            border-right: 1px solid var(--border);
        }

        section[data-testid="stSidebar"] * {
            color: var(--text-secondary);
        }

        h1, h2, h3, h4 {
            color: var(--text-primary) !important;
            letter-spacing: -0.01em;
        }

        p, span, label, li {
            color: var(--text-secondary);
        }

        /* Buttons */
        .stButton > button {
            background: var(--surface-2);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.5rem 1.1rem;
            font-weight: 500;
            transition: all 0.15s ease-in-out;
        }
        .stButton > button:hover {
            border-color: var(--accent);
            color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent);
        }
        .stFormSubmitButton > button, button[kind="primary"] {
            background: var(--accent) !important;
            color: white !important;
            border: none !important;
        }
        .stFormSubmitButton > button:hover, button[kind="primary"]:hover {
            filter: brightness(1.1);
            box-shadow: 0 0 16px var(--accent-soft);
        }

        /* Inputs */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div, textarea {
            background-color: var(--surface-2) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
        }

        /* Cards */
        .app-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.4rem 1.6rem;
            transition: border-color 0.15s ease-in-out, transform 0.15s ease-in-out;
        }
        .app-card:hover {
            border-color: rgba(124, 108, 240, 0.45);
            transform: translateY(-1px);
        }

        .kpi-label {
            color: var(--text-muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.3rem;
        }
        .kpi-value {
            color: var(--text-primary);
            font-size: 2rem;
            font-weight: 700;
        }

        .hero {
            background: linear-gradient(135deg, rgba(124,108,240,0.16) 0%, rgba(18,21,28,0.4) 70%);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem 2.2rem;
            margin-bottom: 1.6rem;
        }
        .hero h1 {
            margin-bottom: 0.3rem;
            font-size: 2.1rem;
        }
        .hero p {
            color: var(--text-secondary);
            font-size: 1rem;
            margin-bottom: 0;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: var(--success-soft);
            color: var(--success);
            border: 1px solid rgba(52, 211, 153, 0.35);
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 6px var(--success);
        }

        .section-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0.2rem 0 0.8rem 0;
        }

        .badge-accent {
            background: var(--accent-soft);
            color: var(--accent);
            padding: 0.15rem 0.55rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .empty-state {
            text-align: center;
            padding: 2.6rem 1.5rem;
            background: var(--surface);
            border: 1px dashed var(--border);
            border-radius: 16px;
        }
        .empty-state .icon {
            font-size: 2.4rem;
            margin-bottom: 0.4rem;
        }
        .empty-state h4 {
            margin-bottom: 0.2rem;
        }
        .empty-state p {
            color: var(--text-muted);
            margin-bottom: 0;
        }

        .privacy-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        }

        .footer-note {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.82rem;
            padding: 1.5rem 0 0.5rem 0;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
        }

        hr { border-color: var(--border); }

        [data-testid="stMetricValue"] { color: var(--text-primary); }
        [data-testid="stMetricLabel"] { color: var(--text-muted); }

        .stTabs [data-baseweb="tab"] { color: var(--text-secondary); }
        .stTabs [aria-selected="true"] { color: var(--accent) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# DATA LAYER — LOAD / SAVE WITH GRACEFUL ERROR HANDLING
# =============================================================================
DATA_FILE = "School_data.json"
DEFAULT_DATA = {"students": [], "teachers": []}


def load_data() -> dict:
    """Load JSON data, handling missing / empty / corrupted files gracefully."""
    path = Path(DATA_FILE)
    if not path.exists():
        return {"students": [], "teachers": []}
    try:
        content = path.read_text().strip()
        if not content:
            return {"students": [], "teachers": []}
        parsed = json.loads(content)
        if "students" not in parsed:
            parsed["students"] = []
        if "teachers" not in parsed:
            parsed["teachers"] = []
        return parsed
    except (json.JSONDecodeError, OSError):
        st.session_state["_data_corrupt_warning"] = True
        return {"students": [], "teachers": []}


def save_data(data: dict) -> None:
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        st.error(f"✕ Could not save data: {e}")


# =============================================================================
# CLASSES — OOP CORE (preserved & refactored for UI use, no input()/print())
# =============================================================================
class Person(ABC):
    """Abstract base class shared by Student and Teacher."""

    def __init__(self, data: dict):
        self.data = data

    @abstractmethod
    def register(self, **kwargs):
        """Returns (success: bool, message: str)."""
        raise NotImplementedError

    @abstractmethod
    def find(self, identifier: str):
        """Exact-match lookup. Returns the record dict or None."""
        raise NotImplementedError

    @staticmethod
    def validate_email(email: str) -> bool:
        if not email:
            return False
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return re.match(pattern, email.strip()) is not None

    @staticmethod
    def validate_name(name: str) -> bool:
        if not name or not name.strip():
            return False
        return bool(re.match(r"^[A-Za-z][A-Za-z .'\-]{1,59}$", name.strip()))

    @staticmethod
    def validate_age(age, min_age: int, max_age: int) -> bool:
        try:
            age_int = int(age)
        except (TypeError, ValueError):
            return False
        return min_age <= age_int <= max_age


class Student(Person):
    MIN_AGE, MAX_AGE = 3, 100

    def person(self):
        return "student"

    def register(self, name, age, email, roll_no):
        name = (name or "").strip()
        email = (email or "").strip()
        roll_no = (roll_no or "").strip()

        if not name or not roll_no:
            return False, "Please fill in all required fields."
        if not self.validate_name(name):
            return False, "Please enter a valid name (letters only, 2-60 characters)."
        if not self.validate_age(age, self.MIN_AGE, self.MAX_AGE):
            return False, f"Age must be a whole number between {self.MIN_AGE} and {self.MAX_AGE}."
        if not self.validate_email(email):
            return False, "Please enter a valid email address."
        if self.find(roll_no) is not None:
            return False, "⚠ Roll number already exists."

        self.data["students"].append({
            "name": name,
            "age": int(age),
            "email": email,
            "roll_no": roll_no,
            "grades": {},
        })
        save_data(self.data)
        return True, f"✓ {name} successfully registered."

    def find(self, roll_no: str):
        if not roll_no:
            return None
        roll_no = roll_no.strip()
        for s in self.data["students"]:
            if s["roll_no"] == roll_no:
                return s
        return None

    def update(self, roll_no, name=None, age=None, email=None):
        student = self.find(roll_no)
        if student is None:
            return False, "No student found with this Roll Number."

        new_name = (name if name is not None else student["name"]).strip()
        new_email = (email if email is not None else student["email"]).strip()
        new_age = age if age is not None else student["age"]

        if not self.validate_name(new_name):
            return False, "Please enter a valid name (letters only, 2-60 characters)."
        if not self.validate_age(new_age, self.MIN_AGE, self.MAX_AGE):
            return False, f"Age must be a whole number between {self.MIN_AGE} and {self.MAX_AGE}."
        if not self.validate_email(new_email):
            return False, "Please enter a valid email address."

        student["name"] = new_name
        student["age"] = int(new_age)
        student["email"] = new_email
        save_data(self.data)
        return True, "✓ Student details updated successfully."

    def delete(self, roll_no):
        student = self.find(roll_no)
        if student is None:
            return False, "No student found with this Roll Number."
        self.data["students"].remove(student)
        save_data(self.data)
        return True, "✓ Student record deleted."

    def upsert_grade(self, roll_no, subject, marks):
        student = self.find(roll_no)
        if student is None:
            return False, "No student found with this Roll Number."
        subject = (subject or "").strip()
        if not subject:
            return False, "Please enter a subject name."
        try:
            marks_val = float(marks)
        except (TypeError, ValueError):
            return False, "Marks must be a number."
        if not (0 <= marks_val <= 100):
            return False, "Marks must be between 0 and 100."
        is_update = subject in student["grades"]
        student["grades"][subject] = marks_val
        save_data(self.data)
        verb = "updated" if is_update else "added"
        return True, f"✓ Grade for {subject} {verb} successfully."

    def delete_grade(self, roll_no, subject):
        student = self.find(roll_no)
        if student is None:
            return False, "No student found with this Roll Number."
        if subject in student["grades"]:
            del student["grades"][subject]
            save_data(self.data)
            return True, f"✓ Grade for {subject} removed."
        return False, "Subject not found for this student."

    @staticmethod
    def average(student) -> float:
        grades = student.get("grades", {})
        return sum(grades.values()) / len(grades) if grades else 0.0

    def all(self):
        return self.data["students"]


class Teacher(Person):
    MIN_AGE, MAX_AGE = 18, 100

    def person(self):
        return "teacher"

    def register(self, name, age, email, emp_id, subject):
        name = (name or "").strip()
        email = (email or "").strip()
        emp_id = (emp_id or "").strip()
        subject = (subject or "").strip()

        if not name or not emp_id or not subject:
            return False, "Please fill in all required fields."
        if not self.validate_name(name):
            return False, "Please enter a valid name (letters only, 2-60 characters)."
        if not self.validate_age(age, self.MIN_AGE, self.MAX_AGE):
            return False, f"Age must be a whole number between {self.MIN_AGE} and {self.MAX_AGE}."
        if not self.validate_email(email):
            return False, "Please enter a valid email address."
        if self.find(emp_id) is not None:
            return False, "⚠ Employee ID already exists."

        self.data["teachers"].append({
            "name": name,
            "age": int(age),
            "email": email,
            "emp_id": emp_id,
            "subject": subject,
        })
        save_data(self.data)
        return True, f"✓ {name} successfully registered."

    def find(self, emp_id: str):
        if not emp_id:
            return None
        emp_id = emp_id.strip()
        for t in self.data["teachers"]:
            if t["emp_id"] == emp_id:
                return t
        return None

    def update(self, emp_id, name=None, age=None, email=None, subject=None):
        teacher = self.find(emp_id)
        if teacher is None:
            return False, "No teacher found with this Employee ID."

        new_name = (name if name is not None else teacher["name"]).strip()
        new_email = (email if email is not None else teacher["email"]).strip()
        new_age = age if age is not None else teacher["age"]
        new_subject = (subject if subject is not None else teacher["subject"]).strip()

        if not self.validate_name(new_name):
            return False, "Please enter a valid name (letters only, 2-60 characters)."
        if not self.validate_age(new_age, self.MIN_AGE, self.MAX_AGE):
            return False, f"Age must be a whole number between {self.MIN_AGE} and {self.MAX_AGE}."
        if not self.validate_email(new_email):
            return False, "Please enter a valid email address."
        if not new_subject:
            return False, "Please enter a subject."

        teacher["name"] = new_name
        teacher["age"] = int(new_age)
        teacher["email"] = new_email
        teacher["subject"] = new_subject
        save_data(self.data)
        return True, "✓ Teacher details updated successfully."

    def delete(self, emp_id):
        teacher = self.find(emp_id)
        if teacher is None:
            return False, "No teacher found with this Employee ID."
        self.data["teachers"].remove(teacher)
        save_data(self.data)
        return True, "✓ Teacher record deleted."

    def all(self):
        return self.data["teachers"]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def init_session_state():
    defaults = {
        "page": "Dashboard",
        "students_sub": "🔍 Find Student",
        "teachers_sub": "🔍 Find Teacher",
        "found_student_roll": "",
        "found_teacher_emp": "",
        "confirm_delete_student": False,
        "confirm_delete_teacher": False,
        "confirm_delete_grade": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def go_to(page, **extra):
    st.session_state["page"] = page
    for k, v in extra.items():
        st.session_state[k] = v
    st.rerun()


def kpi_card(label, value):
    st.markdown(
        f"""
        <div class="app-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(icon, title, message, button_label=None, button_target=None, **extra):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="icon">{icon}</div>
            <h4>{title}</h4>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if button_label and button_target:
        st.write("")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button(button_label, use_container_width=True, key=f"empty_{title}"):
                go_to(button_target, **extra)


def status_pill():
    st.markdown(
        '<span class="status-pill"><span class="status-dot"></span>System Online</span>',
        unsafe_allow_html=True,
    )


# =============================================================================
# SIDEBAR
# =============================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🎓 School Manager")
        st.caption("Navigation")

        nav_items = [
            ("Dashboard", "🏠 Dashboard"),
            ("Students", "👨‍🎓 Students"),
            ("Teachers", "👨‍🏫 Teachers"),
            ("Academics", "📚 Academics"),
            ("Analytics", "📊 Analytics"),
            ("Settings", "⚙️ Settings"),
        ]
        current = st.session_state["page"]
        labels = [label for _, label in nav_items]
        keys = [key for key, _ in nav_items]
        try:
            idx = keys.index(current)
        except ValueError:
            idx = 0

        choice = st.radio(
            "Go to",
            options=labels,
            index=idx,
            label_visibility="collapsed",
        )
        selected_key = keys[labels.index(choice)]
        if selected_key != current:
            st.session_state["page"] = selected_key
            st.rerun()

        st.markdown("---")
        status_pill()
        st.caption(f"Local time · {datetime.now().strftime('%H:%M')}")


# =============================================================================
# DASHBOARD (privacy-first: aggregated stats only, no PII)
# =============================================================================
def render_dashboard(student_mgr: Student, teacher_mgr: Teacher):
    st.markdown(
        """
        <div class="hero">
            <h1>School Management System</h1>
            <p>Manage students, teachers and academic performance — all in one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    students = student_mgr.all()
    teachers = teacher_mgr.all()
    total_grades = sum(len(s["grades"]) for s in students)
    all_marks = [m for s in students for m in s["grades"].values()]
    overall_avg = sum(all_marks) / len(all_marks) if all_marks else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total Students", len(students))
    with c2:
        kpi_card("Total Teachers", len(teachers))
    with c3:
        kpi_card("Total Grade Records", total_grades)
    with c4:
        kpi_card("Overall Average", f"{overall_avg:.1f}")

    st.write("")
    st.markdown('<div class="section-title">Quick Actions</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("➕ Register Student", use_container_width=True):
            go_to("Students", students_sub="➕ Register Student")
    with q2:
        if st.button("➕ Register Teacher", use_container_width=True):
            go_to("Teachers", teachers_sub="➕ Register Teacher")
    with q3:
        if st.button("📝 Add Grade", use_container_width=True):
            go_to("Academics")
    with q4:
        if st.button("🔍 Search Student", use_container_width=True):
            go_to("Students", students_sub="🔍 Find Student")

    st.write("")
    st.markdown('<div class="section-title">Privacy Notice</div>', unsafe_allow_html=True)
    st.info(
        "For privacy, individual student and teacher records are never listed here. "
        "Use **Students → Find Student** or **Teachers → Find Teacher** with the exact "
        "Roll Number or Employee ID to look up a specific record."
    )


# =============================================================================
# STUDENT PAGES (search-to-access privacy model)
# =============================================================================
def render_student_profile_card(student: Student, record: dict):
    avg = Student.average(record)
    st.markdown(
        f"""
        <div class="app-card">
            <div class="badge-accent">Roll No: {record['roll_no']}</div>
            <h3 style="margin-top:0.6rem;">{record['name']}</h3>
            <p style="margin-bottom:0.2rem;">✉️ {record['email']}</p>
            <p style="margin-bottom:0;">🎂 Age: {record['age']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div class="section-title">Academic Performance</div>', unsafe_allow_html=True)
    grades = record.get("grades", {})
    if grades:
        df = pd.DataFrame(
            [{"Subject": subj, "Marks": marks} for subj, marks in grades.items()]
        )
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col_b:
            chart_df = df.set_index("Subject")
            st.bar_chart(chart_df, use_container_width=True)
        st.metric("Average Marks", f"{avg:.1f}")
    else:
        empty_state("📚", "No grades yet", "This student has no recorded grades.")

    st.write("")
    with st.expander("✏️ Edit student details"):
        with st.form(f"edit_student_{record['roll_no']}"):
            e1, e2 = st.columns(2)
            with e1:
                new_name = st.text_input("Student Name", value=record["name"])
                new_age = st.number_input(
                    "Age", min_value=Student.MIN_AGE, max_value=Student.MAX_AGE,
                    value=int(record["age"]),
                )
            with e2:
                new_email = st.text_input("Email", value=record["email"])
                st.text_input("Roll Number", value=record["roll_no"], disabled=True)
            submitted = st.form_submit_button("Save Changes", use_container_width=True)
            if submitted:
                ok, msg = student.update(record["roll_no"], name=new_name, age=new_age, email=new_email)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(f"✕ {msg}")

    with st.expander("🗑️ Delete student record"):
        st.warning(
            f"**Delete Student?**\n\nThis action will permanently remove "
            f"**{record['name']}** (Roll No: {record['roll_no']}). This cannot be undone."
        )
        d1, d2 = st.columns(2)
        with d1:
            if st.button("Cancel", key=f"cancel_del_stu_{record['roll_no']}", use_container_width=True):
                st.session_state["confirm_delete_student"] = False
        with d2:
            if st.button("Delete Student", key=f"del_stu_{record['roll_no']}", use_container_width=True):
                ok, msg = student.delete(record["roll_no"])
                if ok:
                    st.success(msg)
                    st.session_state["found_student_roll"] = ""
                    st.rerun()
                else:
                    st.error(f"✕ {msg}")


def render_students(student_mgr: Student):
    st.subheader("👨‍🎓 Students")

    sub_options = ["🔍 Find Student", "➕ Register Student"]
    idx = sub_options.index(st.session_state["students_sub"]) if st.session_state["students_sub"] in sub_options else 0
    sub = st.radio("Students section", sub_options, index=idx, horizontal=True, label_visibility="collapsed")
    st.session_state["students_sub"] = sub
    st.write("")

    if sub == "🔍 Find Student":
        st.markdown(
            """
            <div class="privacy-box">
                <h4>🔐 Private Records</h4>
                <p>Student records are protected. Enter a valid Roll Number to access a student's information.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        with st.form("find_student_form"):
            roll_no = st.text_input("Enter Roll Number", value=st.session_state["found_student_roll"])
            searched = st.form_submit_button("Search Student", use_container_width=True)

        if searched:
            record = student_mgr.find(roll_no)
            if record is None:
                st.session_state["found_student_roll"] = ""
                st.error("❌ No record found. Please check the Roll Number and try again.")
            else:
                st.session_state["found_student_roll"] = roll_no.strip()

        if st.session_state["found_student_roll"]:
            record = student_mgr.find(st.session_state["found_student_roll"])
            if record is None:
                st.session_state["found_student_roll"] = ""
            else:
                st.write("")
                render_student_profile_card(student_mgr, record)

    else:  # Register Student
        st.markdown('<div class="section-title">Register a New Student</div>', unsafe_allow_html=True)
        if not student_mgr.all():
            st.caption("Your student database is currently empty — this will be the first record.")
        with st.form("register_student_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Student Name")
                age = st.number_input("Age", min_value=3, max_value=100, value=15)
            with c2:
                email = st.text_input("Email")
                roll_no = st.text_input("Roll Number")
            submitted = st.form_submit_button("Register Student", use_container_width=True)

        if submitted:
            ok, msg = student_mgr.register(name=name, age=age, email=email, roll_no=roll_no)
            if ok:
                st.success(msg)
            else:
                st.warning(msg) if "already exists" in msg else st.error(f"✕ {msg}" if not msg.startswith("✕") else msg)


# =============================================================================
# TEACHER PAGES (search-to-access privacy model)
# =============================================================================
def render_teacher_profile_card(teacher: Teacher, record: dict):
    st.markdown(
        f"""
        <div class="app-card">
            <div class="badge-accent">Employee ID: {record['emp_id']}</div>
            <h3 style="margin-top:0.6rem;">{record['name']}</h3>
            <p style="margin-bottom:0.2rem;">✉️ {record['email']}</p>
            <p style="margin-bottom:0.2rem;">🎂 Age: {record['age']}</p>
            <p style="margin-bottom:0;">📘 Subject: {record['subject']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    with st.expander("✏️ Edit teacher details"):
        with st.form(f"edit_teacher_{record['emp_id']}"):
            e1, e2 = st.columns(2)
            with e1:
                new_name = st.text_input("Teacher Name", value=record["name"])
                new_age = st.number_input(
                    "Age", min_value=Teacher.MIN_AGE, max_value=Teacher.MAX_AGE,
                    value=int(record["age"]),
                )
            with e2:
                new_email = st.text_input("Email", value=record["email"])
                new_subject = st.text_input("Subject", value=record["subject"])
            st.text_input("Employee ID", value=record["emp_id"], disabled=True)
            submitted = st.form_submit_button("Save Changes", use_container_width=True)
            if submitted:
                ok, msg = teacher.update(
                    record["emp_id"], name=new_name, age=new_age,
                    email=new_email, subject=new_subject,
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(f"✕ {msg}")

    with st.expander("🗑️ Delete teacher record"):
        st.warning(
            f"**Delete Teacher?**\n\nThis action will permanently remove "
            f"**{record['name']}** (Employee ID: {record['emp_id']}). This cannot be undone."
        )
        d1, d2 = st.columns(2)
        with d1:
            if st.button("Cancel", key=f"cancel_del_teach_{record['emp_id']}", use_container_width=True):
                st.session_state["confirm_delete_teacher"] = False
        with d2:
            if st.button("Delete Teacher", key=f"del_teach_{record['emp_id']}", use_container_width=True):
                ok, msg = teacher.delete(record["emp_id"])
                if ok:
                    st.success(msg)
                    st.session_state["found_teacher_emp"] = ""
                    st.rerun()
                else:
                    st.error(f"✕ {msg}")


def render_teachers(teacher_mgr: Teacher):
    st.subheader("👨‍🏫 Teachers")

    sub_options = ["🔍 Find Teacher", "➕ Register Teacher"]
    idx = sub_options.index(st.session_state["teachers_sub"]) if st.session_state["teachers_sub"] in sub_options else 0
    sub = st.radio("Teachers section", sub_options, index=idx, horizontal=True, label_visibility="collapsed")
    st.session_state["teachers_sub"] = sub
    st.write("")

    if sub == "🔍 Find Teacher":
        st.markdown(
            """
            <div class="privacy-box">
                <h4>🔐 Private Records</h4>
                <p>Teacher records are protected. Enter a valid Employee ID to access a teacher's information.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        with st.form("find_teacher_form"):
            emp_id = st.text_input("Enter Employee ID", value=st.session_state["found_teacher_emp"])
            searched = st.form_submit_button("Search Teacher", use_container_width=True)

        if searched:
            record = teacher_mgr.find(emp_id)
            if record is None:
                st.session_state["found_teacher_emp"] = ""
                st.error("❌ No record found. Please check the Employee ID and try again.")
            else:
                st.session_state["found_teacher_emp"] = emp_id.strip()

        if st.session_state["found_teacher_emp"]:
            record = teacher_mgr.find(st.session_state["found_teacher_emp"])
            if record is None:
                st.session_state["found_teacher_emp"] = ""
            else:
                st.write("")
                render_teacher_profile_card(teacher_mgr, record)

    else:  # Register Teacher
        st.markdown('<div class="section-title">Register a New Teacher</div>', unsafe_allow_html=True)
        if not teacher_mgr.all():
            st.caption("Your teacher database is currently empty — this will be the first record.")
        with st.form("register_teacher_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Teacher Name")
                age = st.number_input("Age", min_value=18, max_value=100, value=30)
                subject = st.text_input("Subject")
            with c2:
                email = st.text_input("Email")
                emp_id = st.text_input("Employee ID")
            submitted = st.form_submit_button("Register Teacher", use_container_width=True)

        if submitted:
            ok, msg = teacher_mgr.register(name=name, age=age, email=email, emp_id=emp_id, subject=subject)
            if ok:
                st.success(msg)
            else:
                st.warning(msg) if "already exists" in msg else st.error(f"✕ {msg}" if not msg.startswith("✕") else msg)


# =============================================================================
# ACADEMICS / GRADE MANAGEMENT (requires Roll Number verification)
# =============================================================================
def render_academics(student_mgr: Student):
    st.subheader("📚 Academics — Manage Grades")

    st.markdown(
        """
        <div class="privacy-box">
            <h4>🔐 Private Records</h4>
            <p>Grades are private academic information. Enter a Roll Number to verify the student before viewing or editing grades.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    with st.form("academics_find_form"):
        roll_no = st.text_input("Enter Roll Number", value=st.session_state["found_student_roll"])
        searched = st.form_submit_button("Verify Student", use_container_width=True)

    if searched:
        record = student_mgr.find(roll_no)
        if record is None:
            st.session_state["found_student_roll"] = ""
            st.error("❌ No record found. Please check the Roll Number and try again.")
        else:
            st.session_state["found_student_roll"] = roll_no.strip()

    if not st.session_state["found_student_roll"]:
        return

    record = student_mgr.find(st.session_state["found_student_roll"])
    if record is None:
        st.session_state["found_student_roll"] = ""
        return

    st.success(f"Verified: **{record['name']}** (Roll No: {record['roll_no']})")
    st.write("")

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="section-title">Add / Update Grade</div>', unsafe_allow_html=True)
        with st.form("grade_form", clear_on_submit=True):
            subject = st.text_input("Subject")
            marks = st.number_input("Marks", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            submitted = st.form_submit_button("Save Grade", use_container_width=True)
        if submitted:
            ok, msg = student_mgr.upsert_grade(record["roll_no"], subject, marks)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(f"✕ {msg}")

    with c2:
        st.markdown('<div class="section-title">Existing Grades</div>', unsafe_allow_html=True)
        grades = record.get("grades", {})
        if grades:
            for subj, mk in grades.items():
                gc1, gc2 = st.columns([3, 1])
                with gc1:
                    st.write(f"**{subj}** — {mk:.1f}")
                with gc2:
                    if st.button("Remove", key=f"rm_grade_{subj}", use_container_width=True):
                        ok, msg = student_mgr.delete_grade(record["roll_no"], subj)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(f"✕ {msg}")
            st.metric("Current Average", f"{Student.average(record):.1f}")
        else:
            empty_state("📝", "No grades yet", "Add the first grade using the form on the left.")


# =============================================================================
# ANALYTICS (aggregate only — no personally identifiable information)
# =============================================================================
def render_analytics(student_mgr: Student, teacher_mgr: Teacher):
    st.subheader("📊 Analytics")

    students = student_mgr.all()
    teachers = teacher_mgr.all()

    if not students and not teachers:
        empty_state("📊", "No data yet", "Analytics will appear once students and teachers are registered.")
        return

    ages = [s["age"] for s in students]
    averages = [Student.average(s) for s in students if s.get("grades")]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        kpi_card("Total Students", len(students))
    with m2:
        kpi_card("Average Age", f"{(sum(ages)/len(ages)):.1f}" if ages else "—")
    with m3:
        kpi_card("Highest Average", f"{max(averages):.1f}" if averages else "—")
    with m4:
        kpi_card("Lowest Average", f"{min(averages):.1f}" if averages else "—")

    st.write("")

    # Subject performance
    st.markdown('<div class="section-title">Subject Performance (class-wide average)</div>', unsafe_allow_html=True)
    subject_totals = {}
    for s in students:
        for subj, mk in s.get("grades", {}).items():
            subject_totals.setdefault(subj, []).append(mk)
    if subject_totals:
        subj_df = pd.DataFrame(
            [{"Subject": subj, "Average Marks": sum(vals) / len(vals)} for subj, vals in subject_totals.items()]
        ).set_index("Subject")
        st.bar_chart(subj_df, use_container_width=True)
    else:
        empty_state("📚", "No grade data yet", "Subject performance will appear once grades are recorded.")

    st.write("")

    # Grade distribution
    st.markdown('<div class="section-title">Grade Distribution</div>', unsafe_allow_html=True)
    if averages:
        bins = {"90-100": 0, "80-89": 0, "70-79": 0, "60-69": 0, "Below 60": 0}
        for avg in averages:
            if avg >= 90:
                bins["90-100"] += 1
            elif avg >= 80:
                bins["80-89"] += 1
            elif avg >= 70:
                bins["70-79"] += 1
            elif avg >= 60:
                bins["60-69"] += 1
            else:
                bins["Below 60"] += 1
        dist_df = pd.DataFrame(
            [{"Range": k, "Students": v} for k, v in bins.items()]
        ).set_index("Range")
        st.bar_chart(dist_df, use_container_width=True)
    else:
        empty_state("📈", "No grade data yet", "Grade distribution will appear once grades are recorded.")

    st.write("")

    # Teacher subject distribution (subject names are not PII)
    st.markdown('<div class="section-title">Teachers by Subject</div>', unsafe_allow_html=True)
    if teachers:
        subj_count = {}
        for t in teachers:
            subj_count[t["subject"]] = subj_count.get(t["subject"], 0) + 1
        tdf = pd.DataFrame(
            [{"Subject": k, "Teachers": v} for k, v in subj_count.items()]
        ).set_index("Subject")
        st.bar_chart(tdf, use_container_width=True)
    else:
        empty_state("👨‍🏫", "No teachers yet", "Register a teacher to see this chart.")


# =============================================================================
# SETTINGS
# =============================================================================
def render_settings():
    st.subheader("⚙️ Settings")
    st.write("")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="app-card">
                <div class="kpi-label">Application</div>
                <div class="kpi-value" style="font-size:1.3rem;">School Management System</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(
            """
            <div class="app-card">
                <div class="kpi-label">Technology</div>
                <div class="kpi-value" style="font-size:1.3rem;">Python + Streamlit</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="app-card">
                <div class="kpi-label">Storage</div>
                <div class="kpi-value" style="font-size:1.3rem;">Local JSON Database</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(
            """
            <div class="app-card">
                <div class="kpi-label">Version</div>
                <div class="kpi-value" style="font-size:1.3rem;">1.0</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown('<div class="section-title">Privacy Model</div>', unsafe_allow_html=True)
    st.info(
        "This application uses a **search-to-access** model: student and teacher "
        "records are never listed in bulk. Every lookup requires an exact Roll Number "
        "(students) or Employee ID (teachers)."
    )


# =============================================================================
# FOOTER
# =============================================================================
def render_footer():
    st.markdown(
        """
        <div class="footer-note">
            School Management System · Built with Python &amp; Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# MAIN
# =============================================================================
def main():
    inject_css()
    init_session_state()

    data = load_data()
    if st.session_state.pop("_data_corrupt_warning", False):
        st.warning("⚠ The data file appeared to be corrupted and has been reset for this session.")

    student_mgr = Student(data)
    teacher_mgr = Teacher(data)

    render_sidebar()

    page = st.session_state["page"]
    if page == "Dashboard":
        render_dashboard(student_mgr, teacher_mgr)
    elif page == "Students":
        render_students(student_mgr)
    elif page == "Teachers":
        render_teachers(teacher_mgr)
    elif page == "Academics":
        render_academics(student_mgr)
    elif page == "Analytics":
        render_analytics(student_mgr, teacher_mgr)
    elif page == "Settings":
        render_settings()

    render_footer()


if __name__ == "__main__":
    main()