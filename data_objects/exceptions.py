# File for all custom exceptions used
# Author: Gurpreet Singh
# © UML Cloud Computing Club 2024

class KeyValidationError(Exception):
    def __init__(self, message, errors) -> None:
        super().__init__(message)
        
        self.errors = errors

