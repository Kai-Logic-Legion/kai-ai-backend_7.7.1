from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from app.services.logger import setup_logger
import os
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCSkuWtue2pCRrqkDcpimzpm5IeO_dkGWQ'


logger = setup_logger(__name__)

def read_text_file(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_file_path = os.path.join(script_dir, file_path)

    with open(absolute_file_path, "r") as file:
        return file.read()

class CourseObjectivesBuilder:
    def __init__(
        self,
        course_title: str,
        course_description: str,
        prompt: str = "",
        model=None,
        parser=None,
        verbose=False
    ):
        default_config = {
            "model": GoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=os.environ.get('GOOGLE_API_KEY')),
            "parser": JsonOutputParser(),
            "prompt": read_text_file("prompt/course_objectives_prompt.txt"),
        }

        self.prompt = prompt or default_config["prompt"]
        self.model = model or default_config["model"]
        self.parser = parser or default_config["parser"]
        self.course_title = course_title
        self.course_description = course_description
        self.verbose = verbose

        if course_title is None:
            raise ValueError("Course title must be provided")
        if course_description is None:
            raise ValueError("Course description must be provided")

    def create_prompt_temp(self):
        """
        Creates a prompt template with the provided configuration.
        """
        prompt = PromptTemplate(
            template=self.prompt,
            input_variables=["course_title", "course_description"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )
        return prompt

    def compile(self):
        """
        Compiles the prompt template with the model and parser into a chain.
        """
        prompt = self.create_prompt_temp()
        chain = prompt | self.model | self.parser

        if self.verbose:
            logger.info("Chain compilation complete")

        return chain

    def generate_course_objectives(self):
        """
        Generates course objectives using the compiled chain.
        """
        if self.verbose:
            logger.info(
                f"Generating course objectives. Title: {self.course_title}, Description: {self.course_description}"
            )

        chain = self.compile()

        response = chain.invoke(
            {
                "course_title": self.course_title,
                "course_description": self.course_description,
            }
        )
        return response

def executor(course_title: str, course_description: str, verbose=True, **kwargs):
    try:
        if verbose:
            logger.debug(f"Course Title: {course_title}, Course Description: {course_description}")

        # Create and return the course objectives
        output = CourseObjectivesBuilder(
            course_title, course_description, verbose=verbose
        ).generate_course_objectives()
        print(output)

    except Exception as e:
        error_message = f"Error in executor: {e}"
        logger.error(error_message)
        raise ValueError(error_message)

    return output

if __name__ == "__main__":
    executor(course_title="Introduction to Python", course_description="A basic course on Python programming.")
