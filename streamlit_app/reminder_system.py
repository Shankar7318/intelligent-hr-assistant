import schedule
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class ReminderSystem:
    def __init__(self, applications_path: str = "data/user_data/applications.json"):
        self.applications_path = Path(applications_path)
        self.smtp_settings = self.load_smtp_settings()
    
    def load_smtp_settings(self) -> Dict:
        settings_path = Path("config/smtp_settings.json")
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                return json.load(f)
        return {}
    
    def load_applications(self) -> List[Dict]:
        if self.applications_path.exists():
            with open(self.applications_path, 'r') as f:
                return json.load(f)
        return []
    
    def get_due_reminders(self) -> List[Dict]:
        applications = self.load_applications()
        today = datetime.now().date()
        
        due_reminders = []
        for app in applications:
            if "next_followup" in app:
                followup_date = datetime.fromisoformat(app["next_followup"]).date()
                if followup_date <= today:
                    due_reminders.append(app)
        
        return due_reminders
    
    def send_email_reminder(self, application: Dict, user_email: str):
        if not self.smtp_settings:
            print("SMTP settings not configured. Cannot send email.")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_settings.get('from_email')
            msg['To'] = user_email
            msg['Subject'] = f"Follow-up Reminder: {application['job_title']} at {application['company']}"
            
            body = f"""
            Hello,
            
            This is a reminder to follow up on your job application for {application['job_title']} at {application['company']}.
            
            Application Details:
            - Position: {application['job_title']}
            - Company: {application['company']}
            - Applied on: {application['application_date']}
            - Current Status: {application['status']}
            
            Suggested follow-up actions:
            1. Send a polite email to the hiring manager
            2. Connect with company employees on LinkedIn
            3. Prepare for a potential interview
            
            Best of luck!
            
            Sincerely,
            Your AI HR Assistant
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_settings.get('smtp_server'), self.smtp_settings.get('smtp_port'))
            server.starttls()
            server.login(self.smtp_settings.get('username'), self.smtp_settings.get('password'))
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def process_due_reminders(self):
        due_reminders = self.get_due_reminders()
        
        for reminder in due_reminders:
            user_email = f"{reminder['user_id']}@example.com"
            
            if self.send_email_reminder(reminder, user_email):
                print(f"Sent reminder to {user_email} for {reminder['job_title']}")
                
                applications = self.load_applications()
                for app in applications:
                    if app['id'] == reminder['id']:
                        next_date = datetime.now() + timedelta(days=7)
                        app['next_followup'] = next_date.isoformat()
                
                with open(self.applications_path, 'w') as f:
                    json.dump(applications, f, indent=2)
    
    def start_scheduler(self):
        schedule.every().day.at("09:00").do(self.process_due_reminders)
        
        print("Reminder system started. Checking for due reminders daily at 9:00 AM.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)