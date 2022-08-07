import sys


class HousingException(Exception):
    def __init__(self, error_message: Exception):
        super().__init__(error_message)
        self.error_message = HousingException.__get_detailed_error_message(error_message)

    @staticmethod
    def __get_detailed_error_message(error_message: Exception) -> str:
        """Return detailed error traceback

        Args:
            error_message (Exception): Exception Object

        Returns:
            str: Error description
        """
        _, _, exec_tb = sys.exc_info()
        # exc_info() #? (type, value, traceback) return information about the most recent exception caught by an except clause in the current stack frame
        line_no = exec_tb.tb_frame.f_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_detail = (
            f"Error occurred in script: {file_name} at line number: [{line_no}] with error message: {error_message}"
        )
        return error_detail

    def __str__(self) -> str:
        return self.error_message

    def __repr__(self) -> str:
        return HousingException.__name__.str()
