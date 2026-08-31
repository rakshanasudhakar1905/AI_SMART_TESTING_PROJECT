def generate_test_cases(requirement):

    requirement = requirement.strip()

    test_cases = [

        {
            "id": "TC001",
            "type": "Positive",
            "test_case": f"Verify that the system successfully handles: {requirement}",
            "expected": "System should accept valid input and produce the expected result."
        },

        {
            "id": "TC002",
            "type": "Negative",
            "test_case": f"Verify system behavior when invalid input is provided for: {requirement}",
            "expected": "System should reject invalid input and display an appropriate error."
        },

        {
            "id": "TC003",
            "type": "Negative",
            "test_case": f"Verify system behavior when incorrect data is provided for: {requirement}",
            "expected": "System should validate the data and prevent incorrect processing."
        },

        {
            "id": "TC004",
            "type": "Edge",
            "test_case": f"Verify the minimum or empty input condition for: {requirement}",
            "expected": "System should handle minimum or empty input without crashing."
        },

        {
            "id": "TC005",
            "type": "Edge",
            "test_case": f"Verify the maximum boundary condition for: {requirement}",
            "expected": "System should correctly handle maximum boundary values."
        },

        {
            "id": "TC006",
            "type": "Boundary",
            "test_case": f"Verify values immediately below the allowed boundary for: {requirement}",
            "expected": "System should correctly validate values below the boundary."
        },

        {
            "id": "TC007",
            "type": "Boundary",
            "test_case": f"Verify values immediately above the allowed boundary for: {requirement}",
            "expected": "System should correctly validate values above the boundary."
        },

        {
            "id": "TC008",
            "type": "Security",
            "test_case": f"Verify unauthorized access handling for: {requirement}",
            "expected": "System should prevent unauthorized access."
        }

    ]

    return test_cases
