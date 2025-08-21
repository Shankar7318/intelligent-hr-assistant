import streamlit as st
from datetime import datetime
from src.data_processing.resume_parser import EnhancedResumeParser
from src.ml_models.embedding_model import EmbeddingModel

class CandidatePortal:
    def __init__(self):
        self.resume_parser = EnhancedResumeParser()
        self.embedding_model = EmbeddingModel()
    
    def render_portal(self):
        st.title("🎯 Candidate Portal")
        
        tab1, tab2, tab3 = st.tabs(["Upload Resume", "Profile Analysis", "Job Matching"])
        
        with tab1:
            self.render_upload_resume()
        
        with tab2:
            self.render_profile_analysis()
        
        with tab3:
            self.render_job_matching()
    
    def render_upload_resume(self):
        st.header("📄 Upload Your Resume")
        
        uploaded_file = st.file_uploader(
            "Choose a resume file", 
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_file is not None:
            file_path = f"data/raw_resumes/{uploaded_file.name}"
            os.makedirs("data/raw_resumes", exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Analyzing your resume..."):
                result = self.resume_parser.parse_resume(file_path)
            
            st.success("Resume uploaded and analyzed successfully!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Skills Summary")
                for category, skills in result["skills"].items():
                    if skills:
                        st.write(f"**{category.title()}:**")
                        for skill in skills:
                            st.write(f"- {skill}")
            
            with col2:
                st.subheader("🎓 Education")
                for education in result["education"]:
                    st.write(f"- {education}")
                
                st.subheader("💼 Experience")
                for exp in result["experience"]:
                    st.write(f"- {exp.get('years', 'Unknown')} years experience")
    
    def render_profile_analysis(self):
        st.header("🔍 Profile Analysis")
        st.info("Profile analysis features will be implemented here")
    
    def render_job_matching(self):
        st.header("🤝 Job Matching")
        st.info("Job matching features will be implemented here")

def main():
    portal = CandidatePortal()
    portal.render_portal()

if __name__ == "__main__":
    main()