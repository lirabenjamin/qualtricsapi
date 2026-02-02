"""
Display Logic Mixin
Handles conditional display and skip logic for survey questions
"""

import requests
from typing import Dict, List, Any, Optional, Union


class DisplayLogicMixin:
    """
    Mixin providing display logic and conditional display operations.

    Display logic allows questions to be shown or hidden based on
    respondent answers, enabling adaptive survey experiences.
    """

    # Supported operators for conditions
    OPERATORS = {
        'Selected': 'Selected',
        'NotSelected': 'NotSelected',
        'Displayed': 'Displayed',
        'NotDisplayed': 'NotDisplayed',
        'EqualTo': 'EqualTo',
        'NotEqualTo': 'NotEqualTo',
        'GreaterThan': 'GreaterThan',
        'LessThan': 'LessThan',
        'GreaterOrEqual': 'GreaterOrEqual',
        'LessOrEqual': 'LessOrEqual',
        'Contains': 'Contains',
        'DoesNotContain': 'DoesNotContain',
        'MatchesRegex': 'MatchesRegex',
        'Empty': 'Empty',
        'NotEmpty': 'NotEmpty'
    }

    def _build_condition(
        self,
        question_id: str,
        operator: str,
        choice_locator: Optional[str] = None,
        value: Optional[Union[str, int, float]] = None,
        logic_type: str = 'Question'
    ) -> Dict[str, Any]:
        """
        Build a single display logic condition.

        Args:
            question_id: The question ID to check (e.g., 'QID1')
            operator: The comparison operator (see OPERATORS)
            choice_locator: Choice identifier for multi-choice questions (e.g., 'q://QID1/SelectableChoice/1')
            value: Value for comparison operators
            logic_type: Type of logic ('Question', 'EmbeddedField', etc.)

        Returns:
            Dictionary representing the condition
        """
        condition = {
            'Type': 'Expression',
            'LogicType': logic_type
        }

        if logic_type == 'Question':
            condition['QuestionID'] = question_id
            condition['QuestionIsInLoop'] = 'no'

            if choice_locator:
                condition['ChoiceLocator'] = choice_locator
                condition['QuestionIDFromLocator'] = question_id
                condition['LeftOperand'] = choice_locator
                condition['Operator'] = operator
            else:
                condition['LeftOperand'] = f'q://{question_id}/SelectableChoice'
                condition['Operator'] = operator
                if value is not None:
                    condition['RightOperand'] = str(value)

        elif logic_type == 'EmbeddedField':
            condition['LeftOperand'] = f'ed://{question_id}'
            condition['Operator'] = operator
            if value is not None:
                condition['RightOperand'] = str(value)

        return condition

    def add_display_logic(
        self,
        survey_id: str,
        question_id: str,
        source_question_id: str,
        operator: str,
        choice_locator: Optional[str] = None,
        value: Optional[Union[str, int, float]] = None
    ) -> bool:
        """
        Add display logic to a question with a single condition.

        The target question will only display when the condition is met.

        Args:
            survey_id: The survey ID
            question_id: The question ID to add display logic to
            source_question_id: The question ID to evaluate
            operator: The operator for comparison (e.g., 'Selected', 'EqualTo')
            choice_locator: For multi-choice, the choice to check
            value: Value for comparison (for EqualTo, GreaterThan, etc.)

        Returns:
            True if successful

        Example:
            # Show Q2 only if choice 1 of Q1 is selected
            api.add_display_logic(
                survey_id,
                question_id="QID2",
                source_question_id="QID1",
                operator="Selected",
                choice_locator="q://QID1/SelectableChoice/1"
            )
        """
        if operator not in self.OPERATORS:
            raise ValueError(f"Invalid operator '{operator}'. Valid operators: {list(self.OPERATORS.keys())}")

        condition = self._build_condition(
            question_id=source_question_id,
            operator=operator,
            choice_locator=choice_locator,
            value=value
        )

        display_logic = {
            'Type': 'BooleanExpression',
            'inPage': False,
            '0': {
                'Type': 'If',
                '0': condition
            }
        }

        # Get current question data first
        current_question = self.get_question(survey_id, question_id)

        # Update question with display logic - MUST include DataExportTag
        question_data = {
            'QuestionText': current_question.get('QuestionText', ''),
            'DataExportTag': current_question.get('DataExportTag', f'Q{question_id}'),
            'QuestionType': current_question.get('QuestionType'),
            'Selector': current_question.get('Selector'),
            'DisplayLogic': display_logic
        }

        # Include SubSelector if present
        if current_question.get('SubSelector'):
            question_data['SubSelector'] = current_question['SubSelector']

        # Include Choices if present
        if current_question.get('Choices'):
            question_data['Choices'] = current_question['Choices']

        # Include Answers if present (for matrix questions)
        if current_question.get('Answers'):
            question_data['Answers'] = current_question['Answers']

        # Include ChoiceOrder if present
        if current_question.get('ChoiceOrder'):
            question_data['ChoiceOrder'] = current_question['ChoiceOrder']

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to add display logic: {response.text}")

    def add_display_logic_multiple(
        self,
        survey_id: str,
        question_id: str,
        conditions: List[Dict[str, Any]],
        conjunction: str = 'AND'
    ) -> bool:
        """
        Add display logic with multiple conditions combined with AND/OR.

        Args:
            survey_id: The survey ID
            question_id: The question ID to add display logic to
            conditions: List of condition dictionaries, each containing:
                - source_question_id: The question to evaluate
                - operator: The comparison operator
                - choice_locator: (optional) Choice identifier
                - value: (optional) Value for comparison
            conjunction: How to combine conditions ('AND' or 'OR')

        Returns:
            True if successful

        Example:
            # Show Q3 if Q1 choice 1 is selected AND Q2 > 5
            api.add_display_logic_multiple(
                survey_id,
                question_id="QID3",
                conditions=[
                    {
                        "source_question_id": "QID1",
                        "operator": "Selected",
                        "choice_locator": "q://QID1/SelectableChoice/1"
                    },
                    {
                        "source_question_id": "QID2",
                        "operator": "GreaterThan",
                        "value": 5
                    }
                ],
                conjunction="AND"
            )
        """
        if conjunction not in ['AND', 'OR']:
            raise ValueError("conjunction must be 'AND' or 'OR'")

        if not conditions:
            raise ValueError("At least one condition is required")

        # Build all conditions
        built_conditions = {}
        for i, cond in enumerate(conditions):
            if cond.get('operator') not in self.OPERATORS:
                raise ValueError(f"Invalid operator '{cond.get('operator')}' in condition {i}")

            built_conditions[str(i)] = self._build_condition(
                question_id=cond['source_question_id'],
                operator=cond['operator'],
                choice_locator=cond.get('choice_locator'),
                value=cond.get('value')
            )
            if i > 0:
                # Qualtrics API requires "And" or "Or" (capitalized first letter only)
                built_conditions[str(i)]['Conjunction'] = conjunction.capitalize()

        # Build the expression
        if_block = {
            'Type': 'If'
        }
        if_block.update(built_conditions)

        display_logic = {
            'Type': 'BooleanExpression',
            'inPage': False,
            '0': if_block
        }

        # Get current question data first
        current_question = self.get_question(survey_id, question_id)

        # Update question with display logic - MUST include DataExportTag
        question_data = {
            'QuestionText': current_question.get('QuestionText', ''),
            'DataExportTag': current_question.get('DataExportTag', f'Q{question_id}'),
            'QuestionType': current_question.get('QuestionType'),
            'Selector': current_question.get('Selector'),
            'DisplayLogic': display_logic
        }

        # Include SubSelector if present
        if current_question.get('SubSelector'):
            question_data['SubSelector'] = current_question['SubSelector']

        # Include Choices if present
        if current_question.get('Choices'):
            question_data['Choices'] = current_question['Choices']

        # Include Answers if present (for matrix questions)
        if current_question.get('Answers'):
            question_data['Answers'] = current_question['Answers']

        # Include ChoiceOrder if present
        if current_question.get('ChoiceOrder'):
            question_data['ChoiceOrder'] = current_question['ChoiceOrder']

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to add display logic: {response.text}")

    def skip_if(
        self,
        survey_id: str,
        question_id: str,
        source_question_id: str,
        operator: str,
        choice_locator: Optional[str] = None,
        value: Optional[Union[str, int, float]] = None,
        skip_to: str = 'EndOfBlock'
    ) -> bool:
        """
        Helper method to add skip logic - skip a question if condition is met.

        This is the inverse of display logic - the question is hidden when
        the condition is true.

        Args:
            survey_id: The survey ID
            question_id: The question ID to potentially skip
            source_question_id: The question ID to evaluate
            operator: The operator for comparison
            choice_locator: For multi-choice, the choice to check
            value: Value for comparison
            skip_to: Where to skip to (currently supports hiding the question)

        Returns:
            True if successful

        Example:
            # Skip Q2 if "No" (choice 2) is selected in Q1
            api.skip_if(
                survey_id,
                question_id="QID2",
                source_question_id="QID1",
                operator="Selected",
                choice_locator="q://QID1/SelectableChoice/2"
            )
        """
        # For skip logic, we invert the operator or use NotSelected
        inverse_operators = {
            'Selected': 'NotSelected',
            'NotSelected': 'Selected',
            'EqualTo': 'NotEqualTo',
            'NotEqualTo': 'EqualTo',
            'GreaterThan': 'LessOrEqual',
            'LessThan': 'GreaterOrEqual',
            'GreaterOrEqual': 'LessThan',
            'LessOrEqual': 'GreaterThan',
            'Contains': 'DoesNotContain',
            'DoesNotContain': 'Contains',
            'Empty': 'NotEmpty',
            'NotEmpty': 'Empty',
            'Displayed': 'NotDisplayed',
            'NotDisplayed': 'Displayed'
        }

        inverted_operator = inverse_operators.get(operator, operator)

        return self.add_display_logic(
            survey_id=survey_id,
            question_id=question_id,
            source_question_id=source_question_id,
            operator=inverted_operator,
            choice_locator=choice_locator.replace(f'/{choice_locator.split("/")[-1]}', f'/{choice_locator.split("/")[-1]}') if choice_locator and operator in ['Selected', 'NotSelected'] else choice_locator,
            value=value
        )

    def show_only_if(
        self,
        survey_id: str,
        question_id: str,
        source_question_id: str,
        operator: str,
        choice_locator: Optional[str] = None,
        value: Optional[Union[str, int, float]] = None
    ) -> bool:
        """
        Helper method to show a question only when a condition is met.

        This is a semantic alias for add_display_logic for clearer code.

        Args:
            survey_id: The survey ID
            question_id: The question ID to conditionally show
            source_question_id: The question ID to evaluate
            operator: The operator for comparison
            choice_locator: For multi-choice, the choice to check
            value: Value for comparison

        Returns:
            True if successful

        Example:
            # Show follow-up only if user selected "Yes" (choice 1)
            api.show_only_if(
                survey_id,
                question_id="QID2",
                source_question_id="QID1",
                operator="Selected",
                choice_locator="q://QID1/SelectableChoice/1"
            )
        """
        return self.add_display_logic(
            survey_id=survey_id,
            question_id=question_id,
            source_question_id=source_question_id,
            operator=operator,
            choice_locator=choice_locator,
            value=value
        )

    def get_display_logic(
        self,
        survey_id: str,
        question_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get the display logic for a question.

        Args:
            survey_id: The survey ID
            question_id: The question ID

        Returns:
            Dictionary with display logic or None if no logic set
        """
        question = self.get_question(survey_id, question_id)
        return question.get('DisplayLogic')

    def delete_display_logic(
        self,
        survey_id: str,
        question_id: str
    ) -> bool:
        """
        Remove display logic from a question.

        Args:
            survey_id: The survey ID
            question_id: The question ID

        Returns:
            True if successful
        """
        # Get current question data first
        current_question = self.get_question(survey_id, question_id)

        # Update question without display logic - MUST include DataExportTag
        question_data = {
            'QuestionText': current_question.get('QuestionText', ''),
            'DataExportTag': current_question.get('DataExportTag', f'Q{question_id}'),
            'QuestionType': current_question.get('QuestionType'),
            'Selector': current_question.get('Selector'),
            'DisplayLogic': None
        }

        # Include SubSelector if present
        if current_question.get('SubSelector'):
            question_data['SubSelector'] = current_question['SubSelector']

        # Include Choices if present
        if current_question.get('Choices'):
            question_data['Choices'] = current_question['Choices']

        # Include Answers if present (for matrix questions)
        if current_question.get('Answers'):
            question_data['Answers'] = current_question['Answers']

        # Include ChoiceOrder if present
        if current_question.get('ChoiceOrder'):
            question_data['ChoiceOrder'] = current_question['ChoiceOrder']

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to delete display logic: {response.text}")

    def add_embedded_data_logic(
        self,
        survey_id: str,
        question_id: str,
        field_name: str,
        operator: str,
        value: Optional[Union[str, int, float]] = None
    ) -> bool:
        """
        Add display logic based on embedded data field.

        Args:
            survey_id: The survey ID
            question_id: The question ID to add display logic to
            field_name: The embedded data field name
            operator: The operator for comparison
            value: Value for comparison

        Returns:
            True if successful

        Example:
            # Show Q1 only if user_type is "premium"
            api.add_embedded_data_logic(
                survey_id,
                question_id="QID1",
                field_name="user_type",
                operator="EqualTo",
                value="premium"
            )
        """
        if operator not in self.OPERATORS:
            raise ValueError(f"Invalid operator '{operator}'. Valid operators: {list(self.OPERATORS.keys())}")

        condition = self._build_condition(
            question_id=field_name,
            operator=operator,
            value=value,
            logic_type='EmbeddedField'
        )

        display_logic = {
            'Type': 'BooleanExpression',
            'inPage': False,
            '0': {
                'Type': 'If',
                '0': condition
            }
        }

        # Get current question data first
        current_question = self.get_question(survey_id, question_id)

        # Update question with display logic - MUST include DataExportTag
        question_data = {
            'QuestionText': current_question.get('QuestionText', ''),
            'DataExportTag': current_question.get('DataExportTag', f'Q{question_id}'),
            'QuestionType': current_question.get('QuestionType'),
            'Selector': current_question.get('Selector'),
            'DisplayLogic': display_logic
        }

        # Include SubSelector if present
        if current_question.get('SubSelector'):
            question_data['SubSelector'] = current_question['SubSelector']

        # Include Choices if present
        if current_question.get('Choices'):
            question_data['Choices'] = current_question['Choices']

        # Include Answers if present (for matrix questions)
        if current_question.get('Answers'):
            question_data['Answers'] = current_question['Answers']

        # Include ChoiceOrder if present
        if current_question.get('ChoiceOrder'):
            question_data['ChoiceOrder'] = current_question['ChoiceOrder']

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to add embedded data logic: {response.text}")
