"""
Branch Logic Mixin
Handles survey flow branching — routing respondents to different blocks
based on question answers, embedded data, or other conditions.
"""

import requests
from typing import Dict, List, Any, Optional, Union


class BranchLogicMixin:
    """
    Mixin providing survey flow branch operations.

    Branch logic routes respondents to different blocks based on conditions.
    This is different from display logic (which shows/hides individual questions).
    """

    def _build_branch_condition(
        self,
        source_question_id: str,
        operator: str,
        choice_locator: Optional[str] = None,
        value: Optional[Union[str, int, float]] = None,
        logic_type: str = "Question",
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build a single branch logic condition.

        Args:
            source_question_id: The question ID (or embedded field name) to evaluate
            operator: Comparison operator (Selected, NotSelected, EqualTo, etc.)
            choice_locator: For MC questions, e.g. 'q://QID1/SelectableChoice/1'
            value: Value for comparison operators (EqualTo, GreaterThan, etc.)
            logic_type: 'Question' or 'EmbeddedField'
            description: Human-readable description (auto-generated if omitted)

        Returns:
            Condition dictionary for BranchLogic
        """
        condition = {
            "Type": "Expression",
            "LogicType": logic_type,
        }

        if logic_type == "Question":
            condition["QuestionID"] = source_question_id
            condition["QuestionIsInLoop"] = "no"

            if choice_locator:
                condition["ChoiceLocator"] = choice_locator
                condition["QuestionIDFromLocator"] = source_question_id
                condition["LeftOperand"] = choice_locator
                condition["Operator"] = operator
            elif value is not None:
                locator = f"q://{source_question_id}/ChoiceNumericEntryValue/1"
                condition["ChoiceLocator"] = locator
                condition["QuestionIDFromLocator"] = source_question_id
                condition["LeftOperand"] = locator
                condition["Operator"] = operator
                condition["RightOperand"] = str(value)
            else:
                condition["LeftOperand"] = f"q://{source_question_id}/SelectableChoice"
                condition["Operator"] = operator

        elif logic_type == "EmbeddedField":
            condition["LeftOperand"] = source_question_id
            condition["Operator"] = operator
            if value is not None:
                condition["RightOperand"] = str(value)

        if description:
            condition["Description"] = description

        return condition

    def add_branch(
        self,
        survey_id: str,
        conditions: List[Dict[str, Any]],
        block_ids: List[str],
        description: Optional[str] = None,
        conjunction: str = "AND",
        position: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Add a branch element to the survey flow.

        Routes respondents to specific blocks when the condition(s) are met.

        Args:
            survey_id: The survey ID
            conditions: List of condition dicts, each with:
                - source_question_id: Question ID to evaluate (e.g. 'QID1')
                - operator: 'Selected', 'NotSelected', 'EqualTo', etc.
                - choice_locator: (optional) e.g. 'q://QID1/SelectableChoice/1'
                - value: (optional) comparison value
                - logic_type: (optional) 'Question' (default) or 'EmbeddedField'
            block_ids: Block IDs to show when condition is true
            description: Human-readable label for the branch
            conjunction: 'AND' or 'OR' when multiple conditions
            position: Index in flow to insert branch (default: after last Block element)

        Returns:
            Dictionary with branch details including FlowID

        Example:
            # Branch to Student Block if "Student" (choice 1) selected in Q1
            api.add_branch(
                survey_id,
                conditions=[{
                    "source_question_id": "QID1",
                    "operator": "Selected",
                    "choice_locator": "q://QID1/SelectableChoice/1"
                }],
                block_ids=["BL_abc123"],
                description="Student path"
            )
        """
        if conjunction not in ("AND", "OR"):
            raise ValueError("conjunction must be 'AND' or 'OR'")
        if not conditions:
            raise ValueError("At least one condition is required")
        if not block_ids:
            raise ValueError("At least one block_id is required")

        # Get current flow
        current_flow = self.get_survey_flow(survey_id)
        flow_list = current_flow.get("Flow", [])

        # Build condition expressions
        built = {}
        for i, cond in enumerate(conditions):
            expr = self._build_branch_condition(
                source_question_id=cond["source_question_id"],
                operator=cond["operator"],
                choice_locator=cond.get("choice_locator"),
                value=cond.get("value"),
                logic_type=cond.get("logic_type", "Question"),
                description=cond.get("description"),
            )
            if i > 0:
                expr["Conjunction"] = conjunction.capitalize()
            built[str(i)] = expr

        if_block = {"Type": "If"}
        if_block.update(built)

        branch_logic = {
            "Type": "BooleanExpression",
            "0": if_block,
        }

        # Build inner flow (blocks shown when condition is true)
        inner_flow = []
        for bid in block_ids:
            next_fid = self._get_next_flow_id(flow_list + inner_flow)
            inner_flow.append({
                "Type": "Standard",
                "ID": bid,
                "FlowID": next_fid,
            })

        branch_flow_id = self._get_next_flow_id(flow_list + inner_flow)
        branch_element = {
            "Type": "Branch",
            "FlowID": branch_flow_id,
            "Description": description or "New Branch",
            "BranchLogic": branch_logic,
            "Flow": inner_flow,
        }

        # Remove referenced blocks from top-level flow so they only
        # appear inside the branch (otherwise respondents see them always)
        block_id_set = set(block_ids)
        flow_list = [
            el for el in flow_list
            if el.get("ID") not in block_id_set
        ]

        # Determine insertion position
        if position is not None:
            insert_idx = min(position, len(flow_list))
        else:
            # Default: insert after the last Block/Standard element
            insert_idx = len(flow_list)
            for i, el in enumerate(flow_list):
                if el.get("Type") in ("Block", "Standard"):
                    insert_idx = i + 1

        flow_list.insert(insert_idx, branch_element)

        # Update flow
        update_payload = {
            "FlowID": current_flow.get("FlowID", "FL_1"),
            "Type": current_flow.get("Type", "Root"),
            "Flow": flow_list,
            "Properties": {
                "Count": self._count_flow_elements(flow_list) + 1
            },
        }

        resp = requests.put(
            f"{self.base_url}/survey-definitions/{survey_id}/flow",
            headers=self.headers,
            json=update_payload,
        )

        if resp.status_code == 200:
            return {
                "FlowID": branch_flow_id,
                "Description": description or "New Branch",
                "block_ids": block_ids,
                "success": True,
            }
        else:
            raise Exception(f"Failed to add branch: {resp.text}")

    def add_branch_simple(
        self,
        survey_id: str,
        source_question_id: str,
        choice_number: int,
        block_id: str,
        operator: str = "Selected",
        description: Optional[str] = None,
        position: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Convenience method: branch to a block based on a single MC choice.

        Args:
            survey_id: The survey ID
            source_question_id: The MC question ID (e.g. 'QID1')
            choice_number: Which choice triggers the branch (1-indexed)
            block_id: Block to show when condition is true
            operator: 'Selected' or 'NotSelected' (default: 'Selected')
            description: Human-readable label
            position: Index in flow (default: auto)

        Returns:
            Dictionary with branch details

        Example:
            # If choice 1 of QID1 is selected, show block BL_abc
            api.add_branch_simple(
                survey_id,
                source_question_id="QID1",
                choice_number=1,
                block_id="BL_abc123",
                description="Student path"
            )
        """
        choice_locator = f"q://{source_question_id}/SelectableChoice/{choice_number}"
        return self.add_branch(
            survey_id=survey_id,
            conditions=[{
                "source_question_id": source_question_id,
                "operator": operator,
                "choice_locator": choice_locator,
            }],
            block_ids=[block_id],
            description=description,
            position=position,
        )

    def add_branch_embedded(
        self,
        survey_id: str,
        field_name: str,
        operator: str,
        value: Union[str, int, float],
        block_ids: List[str],
        description: Optional[str] = None,
        position: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Branch based on an embedded data field value.

        Args:
            survey_id: The survey ID
            field_name: Embedded data field name
            operator: 'EqualTo', 'NotEqualTo', 'Contains', etc.
            value: Value to compare against
            block_ids: Block IDs to show when condition is true
            description: Human-readable label
            position: Index in flow (default: auto)

        Returns:
            Dictionary with branch details

        Example:
            api.add_branch_embedded(
                survey_id,
                field_name="condition",
                operator="EqualTo",
                value="treatment",
                block_ids=["BL_treatment"],
                description="Treatment condition"
            )
        """
        return self.add_branch(
            survey_id=survey_id,
            conditions=[{
                "source_question_id": field_name,
                "operator": operator,
                "value": value,
                "logic_type": "EmbeddedField",
            }],
            block_ids=block_ids,
            description=description,
            position=position,
        )
