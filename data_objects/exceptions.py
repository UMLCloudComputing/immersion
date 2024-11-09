# All custom exceptions used are defined here
# Author: Gurpreet Singh
# © UML Cloud Computing Club 2024

"""
Error Codes:
    - Key Provided Validation - 200
    - OrgID Valdiation        - 201
    - API Key Validation        - 202
"""

class KeyNotProvidedError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.errors = "Code 200"

class OrgIDValidationError(Exception):
    def __init__(self, message, ) -> None:
        super().__init__(message)
        self.errors = "Code 201"

class KeyValidationError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.errors = "Code 202"

