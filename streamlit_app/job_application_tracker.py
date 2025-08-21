import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class JobApplicationTracker:
    def __init__(self, data_path: str = "data/user_data/applications.json"):
        self.data_path = Path(data_path)
        self.applications = self.load_applications()
    
    def load_applications(self) -> List[Dict]:
        """Load applications from JSON file"""
        if self.data_path.exists():
            try:
                with open(self.data_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_applications(self):
        """Save applications to JSON file"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, 'w') as f:
            json.dump(self.applications, f, indent=2)
    
    def add_application(self, user_id: str, job_data: Dict, resume_match: float) -> Dict:
        """Add a new job application"""
        application = {
            "id": len(self.applications) + 1,
            "user_id": user_id,
            "job_id": job_data.get("id", f"job_{len(self.applications) + 1}"),
            "job_title": job_data.get("title", "Unknown Position"),
            "company": job_data.get("company", "Unknown Company"),
            "location": job_data.get("location", "Not specified"),
            "job_type": job_data.get("type", "Full-time"),
            "application_date": datetime.now().isoformat(),
            "status": "Applied",  # Applied, Interviewing, Rejected, Offered, Accepted
            "resume_match": float(resume_match),
            "next_followup": (datetime.now() + timedelta(days=7)).isoformat(),
            "salary_range": job_data.get("salary_range", "Not specified"),
            "notes": "",
            "history": [
                {
                    "date": datetime.now().isoformat(),
                    "status": "Applied",
                    "notes": "Application submitted",
                    "action": "submitted"
                }
            ]
        }
        
        self.applications.append(application)
        self.save_applications()
        return application
    
    def get_user_applications(self, user_id: str) -> List[Dict]:
        """Get all applications for a specific user"""
        return [app for app in self.applications if app.get("user_id") == user_id]
    
    def get_application(self, application_id: int) -> Optional[Dict]:
        """Get a specific application by ID"""
        for app in self.applications:
            if app.get("id") == application_id:
                return app
        return None
    
    def update_application_status(self, application_id: int, status: str, notes: str = "", action: str = "updated"):
        """Update application status and add to history"""
        for app in self.applications:
            if app.get("id") == application_id:
                app["status"] = status
                if notes:
                    app["notes"] = notes
                
                app["history"].append({
                    "date": datetime.now().isoformat(),
                    "status": status,
                    "notes": notes,
                    "action": action
                })
                
                # Update next follow-up date based on status
                if status == "Interviewing":
                    app["next_followup"] = (datetime.now() + timedelta(days=3)).isoformat()
                elif status == "Applied":
                    app["next_followup"] = (datetime.now() + timedelta(days=7)).isoformat()
                
                self.save_applications()
                return True
        return False
    
    def add_note(self, application_id: int, note: str):
        """Add a note to an application"""
        for app in self.applications:
            if app.get("id") == application_id:
                app["notes"] = note
                app["history"].append({
                    "date": datetime.now().isoformat(),
                    "status": app["status"],
                    "notes": note,
                    "action": "note_added"
                })
                self.save_applications()
                return True
        return False
    
    def get_upcoming_followups(self, user_id: str, days_ahead: int = 7) -> List[Dict]:
        """Get applications with upcoming follow-ups"""
        user_apps = self.get_user_applications(user_id)
        today = datetime.now().date()
        
        upcoming = []
        for app in user_apps:
            if "next_followup" in app:
                try:
                    followup_date = datetime.fromisoformat(app["next_followup"]).date()
                    days_until = (followup_date - today).days
                    
                    if 0 <= days_until <= days_ahead:
                        app_copy = app.copy()
                        app_copy["days_until_followup"] = days_until
                        app_copy["followup_date"] = followup_date.strftime("%Y-%m-%d")
                        upcoming.append(app_copy)
                except (ValueError, TypeError):
                    continue
        
        return sorted(upcoming, key=lambda x: x.get("days_until_followup", 999))
    
    def get_applications_by_status(self, user_id: str) -> Dict[str, List[Dict]]:
        """Get applications grouped by status"""
        user_apps = self.get_user_applications(user_id)
        status_groups = {}
        
        for app in user_apps:
            status = app.get("status", "Unknown")
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(app)
        
        return status_groups
    
    def get_application_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics about applications"""
        user_apps = self.get_user_applications(user_id)
        
        if not user_apps:
            return {
                "total": 0,
                "by_status": {},
                "avg_match_score": 0,
                "recent_activity": 0
            }
        
        # Count by status
        status_counts = {}
        for app in user_apps:
            status = app.get("status", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate average match score
        match_scores = [app.get("resume_match", 0) for app in user_apps if app.get("resume_match")]
        avg_match = sum(match_scores) / len(match_scores) if match_scores else 0
        
        # Count applications from last 30 days
        recent_count = 0
        thirty_days_ago = datetime.now() - timedelta(days=30)
        for app in user_apps:
            try:
                app_date = datetime.fromisoformat(app.get("application_date", ""))
                if app_date >= thirty_days_ago:
                    recent_count += 1
            except (ValueError, TypeError):
                continue
        
        return {
            "total": len(user_apps),
            "by_status": status_counts,
            "avg_match_score": round(avg_match * 100, 1),
            "recent_activity": recent_count
        }

def render_application_tracker():
    """Render the job application tracker interface"""
    st.markdown('<h1 class="main-header">📋 Job Application Tracker</h1>', unsafe_allow_html=True)
    
    # Check if user is authenticated
    if "user_authenticated" not in st.session_state or not st.session_state.user_authenticated:
        st.warning("Please log in to access the application tracker")
        return
    
    user_id = st.session_state.get("user_id")
    tracker = JobApplicationTracker()
    
    # Display application statistics
    stats = tracker.get_application_stats(user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Applications", stats["total"])
    
    with col2:
        st.metric("Avg Match Score", f"{stats['avg_match_score']}%")
    
    with col3:
        st.metric("Recent Activity (30d)", stats["recent_activity"])
    
    with col4:
        active_apps = stats["by_status"].get("Interviewing", 0) + stats["by_status"].get("Applied", 0)
        st.metric("Active Applications", active_apps)
    
    # Status distribution chart
    if stats["by_status"]:
        fig = px.pie(
            values=list(stats["by_status"].values()),
            names=list(stats["by_status"].keys()),
            title="Application Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["All Applications", "By Status", "Upcoming Follow-ups", "Add New"])
    
    with tab1:
        render_all_applications(tracker, user_id)
    
    with tab2:
        render_applications_by_status(tracker, user_id)
    
    with tab3:
        render_upcoming_followups(tracker, user_id)
    
    with tab4:
        render_add_application(tracker, user_id)

def render_all_applications(tracker: JobApplicationTracker, user_id: str):
    """Render all applications in a table"""
    applications = tracker.get_user_applications(user_id)
    
    if not applications:
        st.info("No applications found. Start by adding your first job application!")
        return
    
    # Create DataFrame for display
    app_data = []
    for app in applications:
        try:
            app_date = datetime.fromisoformat(app.get("application_date", "")).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            app_date = "Unknown"
        
        app_data.append({
            "ID": app.get("id"),
            "Position": app.get("job_title", "Unknown"),
            "Company": app.get("company", "Unknown"),
            "Status": app.get("status", "Unknown"),
            "Match %": f"{app.get('resume_match', 0) * 100:.1f}%",
            "Applied": app_date,
            "Location": app.get("location", "Not specified"),
            "Type": app.get("job_type", "Full-time")
        })
    
    df = pd.DataFrame(app_data)
    
    # Add filtering options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=df["Status"].unique(),
            default=df["Status"].unique()
        )
    
    with col2:
        company_filter = st.multiselect(
            "Filter by Company",
            options=df["Company"].unique(),
            default=df["Company"].unique()
        )
    
    with col3:
        match_threshold = st.slider("Minimum Match %", 0, 100, 0)
    
    # Apply filters
    filtered_df = df[
        (df["Status"].isin(status_filter)) &
        (df["Company"].isin(company_filter)) &
        (df["Match %"].str.replace('%', '').astype(float) >= match_threshold)
    ]
    
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Match %": st.column_config.ProgressColumn(
                "Match %",
                format="%f%%",
                min_value=0,
                max_value=100,
            )
        }
    )
    
    # Application details expander
    if not filtered_df.empty:
        selected_id = st.selectbox("Select application to view details:", filtered_df["ID"].tolist())
        render_application_details(tracker, selected_id)

def render_applications_by_status(tracker: JobApplicationTracker, user_id: str):
    """Render applications grouped by status"""
    status_groups = tracker.get_applications_by_status(user_id)
    
    if not status_groups:
        st.info("No applications found. Start by adding your first job application!")
        return
    
    for status, applications in status_groups.items():
        with st.expander(f"{status} ({len(applications)})", expanded=True):
            for app in applications:
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{app.get('job_title', 'Unknown')}** at {app.get('company', 'Unknown')}")
                    st.caption(f"Applied: {datetime.fromisoformat(app.get('application_date', '')).strftime('%Y-%m-%d')}")
                
                with col2:
                    match_score = app.get('resume_match', 0) * 100
                    st.metric("Match Score", f"{match_score:.1f}%")
                
                with col3:
                    if st.button("View", key=f"view_{app.get('id')}"):
                        st.session_state.selected_application = app.get('id')
            
            if st.session_state.get('selected_application'):
                render_application_details(tracker, st.session_state.selected_application)

def render_upcoming_followups(tracker: JobApplicationTracker, user_id: str):
    """Render upcoming follow-ups"""
    upcoming = tracker.get_upcoming_followups(user_id, days_ahead=14)
    
    if not upcoming:
        st.success("🎉 No upcoming follow-ups! You're all caught up.")
        return
    
    st.subheader("📅 Upcoming Follow-ups (Next 14 days)")
    
    for app in upcoming:
        days_until = app.get("days_until_followup", 0)
        
        if days_until == 0:
            status = "🔴 Today"
            color = "red"
        elif days_until <= 2:
            status = "🟡 Soon"
            color = "orange"
        else:
            status = "🟢 Upcoming"
            color = "green"
        
        with st.container():
            st.markdown(f"""
            <div style='border-left: 4px solid {color}; padding: 10px; margin: 10px 0;'>
                <h4>{app.get('job_title')} at {app.get('company')}</h4>
                <p><strong>Status:</strong> {app.get('status')} | <strong>Follow-up:</strong> {status} ({days_until} days)</p>
                <p><strong>Date:</strong> {app.get('followup_date')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Mark as Complete", key=f"complete_{app.get('id')}"):
                    tracker.update_application_status(
                        app.get('id'),
                        app.get('status'),
                        "Follow-up completed",
                        "follow_up_completed"
                    )
                    st.rerun()
            
            with col2:
                if st.button("Reschedule", key=f"reschedule_{app.get('id')}"):
                    new_date = st.date_input(
                        "New follow-up date",
                        datetime.now().date() + timedelta(days=7),
                        key=f"date_{app.get('id')}"
                    )
                    if st.button("Confirm", key=f"confirm_{app.get('id')}"):
                        app_obj = tracker.get_application(app.get('id'))
                        if app_obj:
                            app_obj["next_followup"] = new_date.isoformat()
                            tracker.save_applications()
                            st.rerun()

def render_add_application(tracker: JobApplicationTracker, user_id: str):
    """Render form to add new application"""
    st.subheader("➕ Add New Job Application")
    
    with st.form("add_application_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title*", placeholder="e.g., Software Engineer")
            company = st.text_input("Company*", placeholder="e.g., Tech Corp")
            location = st.text_input("Location", placeholder="e.g., Remote, San Francisco")
        
        with col2:
            job_type = st.selectbox(
                "Job Type",
                ["Full-time", "Part-time", "Contract", "Internship", "Remote", "Other"]
            )
            salary_range = st.text_input("Salary Range", placeholder="e.g., $80,000 - $120,000")
            match_score = st.slider("Resume Match Score (%)", 0, 100, 80)
        
        application_date = st.date_input("Application Date", datetime.now().date())
        notes = st.text_area("Notes", placeholder="Any additional notes about this application...")
        
        submitted = st.form_submit_button("Add Application")
        
        if submitted:
            if not job_title or not company:
                st.error("Please fill in required fields (Job Title and Company)")
            else:
                job_data = {
                    "title": job_title,
                    "company": company,
                    "location": location,
                    "type": job_type,
                    "salary_range": salary_range
                }
                
                application = tracker.add_application(
                    user_id,
                    job_data,
                    match_score / 100.0
                )
                
                if notes:
                    tracker.add_note(application["id"], notes)
                
                st.success("✅ Application added successfully!")
                st.balloons()

def render_application_details(tracker: JobApplicationTracker, application_id: int):
    """Render detailed view of a specific application"""
    app = tracker.get_application(application_id)
    
    if not app:
        st.error("Application not found")
        return
    
    st.subheader(f"📄 Application Details: {app.get('job_title')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Company:** {app.get('company')}")
        st.info(f"**Location:** {app.get('location', 'Not specified')}")
        st.info(f"**Type:** {app.get('job_type', 'Full-time')}")
    
    with col2:
        status = app.get('status', 'Applied')
        status_color = {
            'Applied': 'blue',
            'Interviewing': 'orange',
            'Rejected': 'red',
            'Offered': 'green',
            'Accepted': 'darkgreen'
        }.get(status, 'gray')
        
        st.info(f"**Status:** :{status_color}[{status}]")
        st.info(f"**Applied:** {datetime.fromisoformat(app.get('application_date')).strftime('%Y-%m-%d')}")
        st.info(f"**Match Score:** :green[**{app.get('resume_match', 0) * 100:.1f}%**]")
    
    with col3:
        st.info(f"**Salary Range:** {app.get('salary_range', 'Not specified')}")
        if app.get('next_followup'):
            followup_date = datetime.fromisoformat(app['next_followup']).strftime('%Y-%m-%d')
            days_until = (datetime.fromisoformat(app['next_followup']).date() - datetime.now().date()).days
            st.info(f"**Next Follow-up:** {followup_date} ({days_until} days)")
    
    # Notes section
    st.subheader("📝 Notes")
    current_notes = app.get('notes', '')
    new_note = st.text_area("Add or update notes", value=current_notes, height=100)
    
    if st.button("Save Notes") and new_note != current_notes:
        tracker.add_note(application_id, new_note)
        st.success("Notes updated successfully!")
        st.rerun()
    
    # Status update section
    st.subheader("🔄 Update Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📨 Mark as Applied", use_container_width=True):
            tracker.update_application_status(application_id, "Applied", "Application submitted")
            st.rerun()
    
    with col2:
        if st.button("📞 Interviewing", use_container_width=True):
            tracker.update_application_status(application_id, "Interviewing", "Moved to interview stage")
            st.rerun()
    
    with col3:
        if st.button("✅ Offered", use_container_width=True):
            tracker.update_application_status(application_id, "Offered", "Job offer received")
            st.rerun()
    
    col4, col5 = st.columns(2)
    
    with col4:
        if st.button("❌ Rejected", use_container_width=True):
            tracker.update_application_status(application_id, "Rejected", "Application rejected")
            st.rerun()
    
    with col5:
        if st.button("🎉 Accepted", use_container_width=True):
            tracker.update_application_status(application_id, "Accepted", "Offer accepted")
            st.rerun()
    
    # Application history
    st.subheader("📊 Application History")
    
    history = app.get('history', [])
    if history:
        history_df = pd.DataFrame(history)
        history_df['date'] = pd.to_datetime(history_df['date']).dt.strftime('%Y-%m-%d %H:%M')
        history_df = history_df.sort_values('date', ascending=False)
        
        st.dataframe(
            history_df[['date', 'status', 'action', 'notes']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No history recorded for this application.")

def main():
    """Main function for standalone execution"""
    st.set_page_config(
        page_title="Job Application Tracker",
        page_icon="📋",
        layout="wide"
    )
    
    # For standalone testing
    if "user_id" not in st.session_state:
        st.session_state.user_id = "test_user"
        st.session_state.user_authenticated = True
    
    render_application_tracker()

if __name__ == "__main__":
    main()
