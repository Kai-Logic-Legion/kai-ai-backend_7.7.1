from app.services.logger import setup_logger
from app.features.syllabus_generator.tools import CourseObjectivesBuilder  

logger = setup_logger()


# TEMPLATE, NEEDS TO BE DISCUSSED AND FORMED ON MONDAY
def executor(
    course_title: str,
    course_description: str,
    verbose=False,
    *args,
    **kwargs,
):
    try:
        if verbose:
            logger.debug(f"Course Title: {course_title}, Course Description: {course_description}")

        course_objectives_builder = CourseObjectivesBuilder(
            course_title=course_title,
            course_description=course_description,
            verbose=verbose
        )

        # Generate course objectives
        output = course_objectives_builder.generate_course_objectives()

        if verbose:
            logger.info("Course objectives generated successfully")
            logger.info(f"Course Objectives: {output}")

    except Exception as e:
        error_message = f"Error in executor: {e}"
        logger.error(error_message)
        raise ValueError(error_message)

    return output

if __name__ == "__main__":
    # Example call to executor
    executor(
        course_title="Linear Algebra",
        course_description="A basic course on the core concepts of Linear Algebra.",
        verbose=True
    )
