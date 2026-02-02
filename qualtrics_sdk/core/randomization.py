"""
Randomization Mixin
Handles survey randomization features including block, question, and choice randomization
"""

import requests
from typing import Dict, List, Any, Optional


class RandomizationMixin:
    """
    Mixin providing randomization operations for surveys.

    Supports three levels of randomization:
    - Block-level: Randomize the order in which survey blocks are presented
    - Question-level: Randomize question order within a block
    - Choice-level: Randomize answer choices within a question
    """

    def randomize_blocks(
        self,
        survey_id: str,
        block_ids: List[str],
        randomization_type: str = "random",
        evenly_present: bool = False,
        subset_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Set up block-level randomization in the survey flow.

        Randomizes the order in which specified blocks are presented to respondents.

        Args:
            survey_id: The survey ID
            block_ids: List of block IDs to include in randomization
            randomization_type: Type of randomization:
                - "random": Simple random order (default)
                - "balanced": Latin square design for experimental work
            evenly_present: If True, ensures each block order is presented
                           to an equal number of respondents (balanced distribution)
            subset_count: If specified, only show this many blocks from the list
                         (subset randomization). Must be less than len(block_ids).

        Returns:
            Dictionary with the updated survey flow

        Example:
            >>> api.randomize_blocks(
            ...     survey_id,
            ...     block_ids=["BL_001", "BL_002", "BL_003"],
            ...     evenly_present=True
            ... )
        """
        if subset_count is not None and subset_count >= len(block_ids):
            raise ValueError("subset_count must be less than the number of block_ids")

        # Get current survey flow
        survey = self.get_survey(survey_id)
        current_flow = survey.get('SurveyFlow', {'Flow': [], 'Properties': {}})

        # Build the randomizer element
        randomizer_flow = []
        for block_id in block_ids:
            randomizer_flow.append({
                "Type": "Block",
                "ID": block_id,
                "FlowID": f"FL_{block_id}"
            })

        randomizer = {
            "Type": "BlockRandomizer",
            "FlowID": f"FL_Randomizer_{survey_id[:8]}",
            "SubSet": subset_count if subset_count else len(block_ids),
            "EvenPresentation": evenly_present,
            "Flow": randomizer_flow
        }

        # Add Latin square / balanced randomization if requested
        if randomization_type == "balanced":
            randomizer["Randomization"] = "Balanced"

        # Update the survey flow - insert randomizer and remove individual block references
        new_flow = []
        blocks_to_randomize = set(block_ids)
        randomizer_added = False

        for element in current_flow.get('Flow', []):
            if element.get('Type') == 'Block' and element.get('ID') in blocks_to_randomize:
                # Replace first matching block with randomizer
                if not randomizer_added:
                    new_flow.append(randomizer)
                    randomizer_added = True
                # Skip other blocks that are now in the randomizer
            else:
                new_flow.append(element)

        # If no blocks were found in the flow, add randomizer at the beginning
        if not randomizer_added:
            new_flow.insert(0, randomizer)

        # Update the survey flow
        flow_data = {
            "SurveyFlow": {
                "Flow": new_flow,
                "Properties": current_flow.get('Properties', {
                    "Count": len(new_flow)
                })
            }
        }

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers,
            json=flow_data['SurveyFlow']
        )

        if response.status_code == 200:
            return response.json().get('result', flow_data)
        else:
            raise Exception(f"Failed to set block randomization: {response.text}")

    def randomize_questions_in_block(
        self,
        survey_id: str,
        block_id: str,
        randomize: bool = True,
        subset_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Set up question-level randomization within a specific block.

        Randomizes the order of questions presented within the specified block.

        Args:
            survey_id: The survey ID
            block_id: The block ID to randomize questions in
            randomize: If True, enable question randomization; if False, disable it
            subset_count: If specified, only show this many questions from the block
                         (subset randomization). Useful for attention checks or
                         displaying partial question sets.

        Returns:
            Dictionary with the updated block configuration

        Example:
            >>> api.randomize_questions_in_block(
            ...     survey_id,
            ...     block_id="BL_001",
            ...     randomize=True,
            ...     subset_count=5  # Show only 5 random questions from block
            ... )
        """
        # Get current block configuration
        survey = self.get_survey(survey_id)
        blocks = survey.get('Blocks', {})

        if block_id not in blocks:
            raise ValueError(f"Block {block_id} not found in survey")

        block = blocks[block_id]

        # Build the block options
        block_options = block.get('Options', {})

        if randomize:
            block_options['Randomization'] = {
                "Advanced": None,
                "Type": "All",
                "TotalRandSubset": subset_count
            }
            if subset_count:
                block_options['Randomization']['TotalRandSubset'] = subset_count
        else:
            # Remove randomization if it exists
            if 'Randomization' in block_options:
                del block_options['Randomization']

        # Update the block
        block_data = {
            "Type": block.get('Type', 'Standard'),
            "Description": block.get('Description', ''),
            "Options": block_options
        }

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/blocks/{block_id}',
            headers=self.headers,
            json=block_data
        )

        if response.status_code == 200:
            return response.json().get('result', block_data)
        else:
            raise Exception(f"Failed to set question randomization: {response.text}")

    def randomize_question_choices(
        self,
        survey_id: str,
        question_id: str,
        randomize: bool = True,
        anchor_choices: Optional[List[str]] = None,
        anchor_last: bool = False
    ) -> Dict[str, Any]:
        """
        Set up choice-level randomization for a specific question.

        Randomizes the order of answer choices presented for the specified question.
        Supports anchoring specific choices to remain in fixed positions.

        Args:
            survey_id: The survey ID
            question_id: The question ID to randomize choices for
            randomize: If True, enable choice randomization; if False, disable it
            anchor_choices: List of choice keys (e.g., ["1", "5"]) to anchor
                           in their original positions. Useful for "Other" or
                           "None of the above" options.
            anchor_last: If True, anchor the last choice (common for "Other" options).
                        This is a convenience shortcut for anchor_choices.

        Returns:
            Dictionary with the updated question configuration

        Example:
            >>> # Randomize choices but keep "Other" (last choice) at the end
            >>> api.randomize_question_choices(
            ...     survey_id,
            ...     question_id="QID1",
            ...     randomize=True,
            ...     anchor_last=True
            ... )
            >>>
            >>> # Randomize but anchor specific choices
            >>> api.randomize_question_choices(
            ...     survey_id,
            ...     question_id="QID2",
            ...     randomize=True,
            ...     anchor_choices=["1", "6"]  # Keep first and last in place
            ... )
        """
        # Get current question configuration
        question = self.get_question(survey_id, question_id)

        # Verify question has choices
        if 'Choices' not in question:
            raise ValueError(f"Question {question_id} does not have choices to randomize")

        choices = question.get('Choices', {})
        choice_order = question.get('ChoiceOrder', list(choices.keys()))

        # Handle anchor_last convenience option
        if anchor_last and choice_order:
            last_choice = choice_order[-1] if isinstance(choice_order, list) else str(max(int(k) for k in choices.keys()))
            if anchor_choices is None:
                anchor_choices = [last_choice]
            elif last_choice not in anchor_choices:
                anchor_choices.append(last_choice)

        # Build the randomization configuration
        if randomize:
            randomization_config = {
                "Type": "All"
            }

            # Set up anchored choices if specified
            if anchor_choices:
                # In Qualtrics, anchored choices use the "Advanced" randomization
                # with specific choices marked as "Fixed"
                fixed_positions = {}
                for choice_key in anchor_choices:
                    if choice_key in choices or choice_key in [str(k) for k in choices.keys()]:
                        fixed_positions[str(choice_key)] = True

                if fixed_positions:
                    randomization_config["Advanced"] = {
                        "FixedOrder": list(fixed_positions.keys()),
                        "RandomizeAll": "RandomWithFixed"
                    }
        else:
            randomization_config = None

        # Update question data
        question_data = {
            "QuestionText": question.get('QuestionText', ''),
            "QuestionType": question.get('QuestionType', 'MC'),
            "Selector": question.get('Selector', 'SAVR'),
            "Choices": choices,
            "ChoiceOrder": choice_order,
            "Configuration": question.get('Configuration', {}),
            "Validation": question.get('Validation', {}),
            "Language": question.get('Language', [])
        }

        if randomization_config:
            question_data['Randomization'] = randomization_config
        elif 'Randomization' in question:
            # Explicitly remove randomization by not including it
            pass

        # Use the existing update_question method
        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json().get('result', question_data)
        else:
            raise Exception(f"Failed to set choice randomization: {response.text}")

    def get_randomization_settings(self, survey_id: str) -> Dict[str, Any]:
        """
        Get all randomization settings for a survey.

        Returns a summary of all randomization configurations including
        block-level, question-level, and choice-level randomization.

        Args:
            survey_id: The survey ID

        Returns:
            Dictionary with randomization settings organized by type:
            - block_randomization: Survey flow randomizers
            - question_randomization: Per-block question randomization
            - choice_randomization: Per-question choice randomization
        """
        survey = self.get_survey(survey_id)

        result = {
            "block_randomization": [],
            "question_randomization": {},
            "choice_randomization": {}
        }

        # Check survey flow for block randomizers
        flow = survey.get('SurveyFlow', {}).get('Flow', [])
        for element in flow:
            if element.get('Type') == 'BlockRandomizer':
                result["block_randomization"].append({
                    "flow_id": element.get('FlowID'),
                    "blocks": [b.get('ID') for b in element.get('Flow', [])],
                    "subset": element.get('SubSet'),
                    "even_presentation": element.get('EvenPresentation', False)
                })

        # Check blocks for question randomization
        blocks = survey.get('Blocks', {})
        for block_id, block in blocks.items():
            options = block.get('Options', {})
            if 'Randomization' in options:
                result["question_randomization"][block_id] = {
                    "description": block.get('Description', ''),
                    "randomization": options['Randomization']
                }

        # Check questions for choice randomization
        for block_id, block in blocks.items():
            for element in block.get('BlockElements', []):
                if element.get('Type') == 'Question':
                    question_id = element['QuestionID']
                    try:
                        question = self.get_question(survey_id, question_id)
                        if 'Randomization' in question:
                            result["choice_randomization"][question_id] = {
                                "question_text": question.get('QuestionText', '')[:50],
                                "randomization": question['Randomization']
                            }
                    except Exception:
                        # Skip questions that can't be retrieved
                        pass

        return result
