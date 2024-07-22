import streamlit as st
from langchain_google_vertexai import VertexAI
import os

class CourseObjectivesGenerator:
    def __init__(self):
        self.llm = None
        self.init_llm()
        
    def init_llm(self):
        """
        Initialize the LLM.
        """
        self.llm = VertexAI(
            model_name="textembedding-gecko@003",
            temperature=0.7,
            max_output_tokens=150,
            project=" ",
            location=" "
        )
    
    def generate_course_objectives(self, course_title, course_description):
        """
        Generate course objectives using the LLM based on the provided course title and description.
        """
        prompt_template = """
        You are an expert educator. Generate a detailed list of course objectives for the following course:
        Course Title: {course_title}
        Course Description: {course_description}
        Ensure the objectives clearly outline the learning goals and outcomes expected by the end of the course.
        """
        prompt = prompt_template.format(course_title=course_title, course_description=course_description)
        
        try:
            response = self.llm(prompt)
            return response
        except Exception as e:
            return {"error": str(e)}

def main():
    st.title("Course Objectives Generator")
    st.write("Welcome to the Course Objectives Generator!")

    course_title = st.text_input("Enter the course title:")
    course_description = st.text_area("Enter the course description:")

    if st.button("Generate Course Objectives"):
        objectives_generator = CourseObjectivesGenerator()
        objectives = objectives_generator.generate_course_objectives(course_title, course_description)

        if 'error' in objectives:
            st.error(objectives['error'])
        else:
            st.write("Generated Course Objectives:")
            st.json(objectives)

if __name__ == "__main__":
    main()
