from typing import List
from features.syllabus_generator.schema import ExecutorInput
from services.logger import setup_logger
from app.features.syllabus_generator.tools import SyllabusBuilder
from app.api.error_utilities import LoaderError, ToolExecutorError
from pydantic import ValidationError

logger = setup_logger()


def executor(
    input_args: ExecutorInput,
    verbose: bool = True,
):
    logger.error(f"here {list(input_args.items())}")
    """Execute the syllabus generation process."""
    try:
        if verbose:
            logger.debug(
                f"Subject: {input_args.subject}, Grade Level: {input_args.grade_level}, Course Overview: {input_args.course_overview}"
            )

        logger.info("second", str(input_args))
        input_args = ExecutorInput(**input_args)

        sb = SyllabusBuilder(
            input_args.subject,
            input_args.grade_level,
            input_args.course_overview,
            input_args.customisation,
            input_args.options,
            verbose=verbose,
        )
        syllabus = sb.create_syllabus()

        # updated_syllabus = sb.apply_customisation(syllabus)
        # print(updated_syllabus)

    except LoaderError as e:
        error_message = f"Error in RAGPipeline -> {e}"
        logger.error(error_message)
        raise ToolExecutorError(error_message)

    except ValidationError as e:
        error_message = f"Error validating input: {e}"
        logger.error(error_message)
        raise ValueError(error_message)

    except ValueError as e:
        error_message = f"Error creating syllabus: {e}"
        logger.error(error_message)
        raise ValueError(error_message)

    except Exception as e:
        error_message = f"Error in executor: {e}"
        logger.error(error_message)
        raise ValueError(error_message)

    return syllabus
