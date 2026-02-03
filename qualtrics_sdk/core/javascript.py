"""
JavaScript Mixin
Handles adding custom JavaScript to questions
"""

import requests
from typing import Dict, Any, Optional


class JavaScriptMixin:
    """Mixin providing custom JavaScript functionality for questions"""

    def add_question_javascript(
        self,
        survey_id: str,
        question_id: str,
        javascript_code: str,
        append: bool = False
    ) -> bool:
        """
        Add custom JavaScript to a question.

        The JavaScript code will execute in the Qualtrics survey context,
        with access to the Qualtrics JavaScript API.

        Args:
            survey_id: The survey ID
            question_id: The question ID to add JavaScript to
            javascript_code: The JavaScript code to add. Can include
                Qualtrics event handlers like addOnload, addOnReady, addOnUnload
            append: If True, append to existing JavaScript. If False, replace it.

        Returns:
            True if successful

        Example:
            >>> # Add custom JavaScript to a question
            >>> api.add_question_javascript(
            ...     survey_id,
            ...     question_id,
            ...     '''
            ...     Qualtrics.SurveyEngine.addOnload(function() {
            ...         console.log('Question loaded!');
            ...     });
            ...     '''
            ... )

            >>> # Add JavaScript to manipulate DOM
            >>> api.add_question_javascript(
            ...     survey_id,
            ...     question_id,
            ...     '''
            ...     Qualtrics.SurveyEngine.addOnReady(function() {
            ...         // Change response option styling
            ...         var choices = this.getChoiceContainer();
            ...         choices.style.backgroundColor = '#f0f0f0';
            ...     });
            ...     '''
            ... )
        """
        # Get current question data
        current_question = self.get_question(survey_id, question_id)

        # Handle JavaScript - append or replace
        if append and current_question.get('QuestionJS'):
            new_js = current_question['QuestionJS'] + '\n\n' + javascript_code
        else:
            new_js = javascript_code

        # Build question data preserving existing fields
        question_data = self._build_question_update_data(current_question)
        question_data['QuestionJS'] = new_js

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to add JavaScript to question: {response.text}")

    def get_question_javascript(
        self,
        survey_id: str,
        question_id: str
    ) -> Optional[str]:
        """
        Get the custom JavaScript code from a question.

        Args:
            survey_id: The survey ID
            question_id: The question ID

        Returns:
            The JavaScript code as a string, or None if no JavaScript is set

        Example:
            >>> js = api.get_question_javascript(survey_id, question_id)
            >>> if js:
            ...     print(f"Question has JavaScript: {len(js)} characters")
        """
        question = self.get_question(survey_id, question_id)
        return question.get('QuestionJS')

    def remove_question_javascript(
        self,
        survey_id: str,
        question_id: str
    ) -> bool:
        """
        Remove all custom JavaScript from a question.

        Args:
            survey_id: The survey ID
            question_id: The question ID

        Returns:
            True if successful

        Example:
            >>> api.remove_question_javascript(survey_id, question_id)
            True
        """
        current_question = self.get_question(survey_id, question_id)

        # Build question data without JavaScript
        question_data = self._build_question_update_data(current_question)
        question_data['QuestionJS'] = ''

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to remove JavaScript from question: {response.text}")

    def add_auto_advance(
        self,
        survey_id: str,
        question_id: str,
        delay_ms: int = 3000
    ) -> bool:
        """
        Add auto-advance JavaScript to a question.

        This makes the question automatically advance to the next page
        after the specified delay. Useful for timed questions or
        displaying information briefly.

        Args:
            survey_id: The survey ID
            question_id: The question ID
            delay_ms: Delay in milliseconds before advancing (default: 3000)

        Returns:
            True if successful

        Example:
            >>> # Auto-advance after 5 seconds
            >>> api.add_auto_advance(survey_id, question_id, delay_ms=5000)

            >>> # Brief 2-second display
            >>> api.add_auto_advance(survey_id, question_id, delay_ms=2000)
        """
        javascript_code = f'''
Qualtrics.SurveyEngine.addOnload(function() {{
    var that = this;
    setTimeout(function() {{
        that.clickNextButton();
    }}, {delay_ms});
}});
'''
        return self.add_question_javascript(survey_id, question_id, javascript_code)

    def add_timer_display(
        self,
        survey_id: str,
        question_id: str,
        duration_seconds: int = 60,
        auto_advance: bool = True,
        timer_position: str = 'top'
    ) -> bool:
        """
        Add a visible countdown timer to a question.

        Displays a countdown timer and optionally auto-advances when time expires.

        Args:
            survey_id: The survey ID
            question_id: The question ID
            duration_seconds: Timer duration in seconds (default: 60)
            auto_advance: Whether to auto-advance when timer expires (default: True)
            timer_position: Where to display timer - 'top' or 'bottom' (default: 'top')

        Returns:
            True if successful

        Example:
            >>> # Add 30-second timer that auto-advances
            >>> api.add_timer_display(survey_id, question_id, duration_seconds=30)

            >>> # Add 2-minute timer without auto-advance
            >>> api.add_timer_display(
            ...     survey_id, question_id,
            ...     duration_seconds=120,
            ...     auto_advance=False
            ... )
        """
        auto_advance_code = 'that.clickNextButton();' if auto_advance else ''
        position_code = 'insertBefore' if timer_position == 'top' else 'appendChild'
        reference_code = ('questionContainer.firstChild' if timer_position == 'top'
                          else 'null')

        javascript_code = f'''
Qualtrics.SurveyEngine.addOnload(function() {{
    var that = this;
    var timeLeft = {duration_seconds};

    // Create timer display
    var timerDiv = document.createElement('div');
    timerDiv.id = 'customTimer';
    timerDiv.style.cssText = 'padding: 10px; margin: 10px 0; background-color: #f5f5f5; ' +
        'border: 1px solid #ddd; border-radius: 4px; font-size: 16px; text-align: center;';

    function updateTimer() {{
        var minutes = Math.floor(timeLeft / 60);
        var seconds = timeLeft % 60;
        timerDiv.innerHTML = 'Time remaining: ' + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;

        if (timeLeft <= 10) {{
            timerDiv.style.backgroundColor = '#ffebee';
            timerDiv.style.borderColor = '#ef5350';
        }}

        if (timeLeft <= 0) {{
            timerDiv.innerHTML = 'Time expired!';
            {auto_advance_code}
        }} else {{
            timeLeft--;
            setTimeout(updateTimer, 1000);
        }}
    }}

    // Insert timer
    var questionContainer = this.getQuestionContainer();
    questionContainer.{position_code}(timerDiv, {reference_code});

    updateTimer();
}});
'''
        return self.add_question_javascript(survey_id, question_id, javascript_code)

    def add_input_validation(
        self,
        survey_id: str,
        question_id: str,
        regex: str,
        error_message: str = "Please enter a valid value"
    ) -> bool:
        """
        Add custom input validation using a regular expression.

        Validates the response against a regex pattern before allowing
        the respondent to proceed.

        Args:
            survey_id: The survey ID
            question_id: The question ID
            regex: Regular expression pattern for validation
            error_message: Error message to display when validation fails

        Returns:
            True if successful

        Example:
            >>> # Validate 5-digit ZIP code
            >>> api.add_input_validation(
            ...     survey_id, question_id,
            ...     regex=r"^\\d{5}$",
            ...     error_message="Please enter a valid 5-digit ZIP code"
            ... )

            >>> # Validate email format
            >>> api.add_input_validation(
            ...     survey_id, question_id,
            ...     regex=r"^[^@]+@[^@]+\\.[^@]+$",
            ...     error_message="Please enter a valid email address"
            ... )
        """
        # Escape backslashes and quotes for JavaScript
        escaped_regex = regex.replace('\\', '\\\\').replace("'", "\\'")
        escaped_message = error_message.replace("'", "\\'").replace('"', '\\"')

        javascript_code = f'''
Qualtrics.SurveyEngine.addOnPageSubmit(function(type) {{
    if (type === 'next') {{
        var inputValue = this.getTextValue();
        var pattern = new RegExp('{escaped_regex}');

        if (inputValue && !pattern.test(inputValue)) {{
            alert('{escaped_message}');
            return false;  // Prevent page submit
        }}
    }}
    return true;
}});
'''
        return self.add_question_javascript(survey_id, question_id, javascript_code)

    def add_iframe(
        self,
        survey_id: str,
        question_id: str,
        iframe_url: str,
        width: str = "100%",
        height: str = "400px",
        position: str = "bottom"
    ) -> bool:
        """
        Add an iframe to a question.

        Embeds external content within the question using an iframe.

        Args:
            survey_id: The survey ID
            question_id: The question ID
            iframe_url: URL to embed in the iframe
            width: Width of the iframe (default: "100%")
            height: Height of the iframe (default: "400px")
            position: Where to insert iframe - 'top' or 'bottom' (default: 'bottom')

        Returns:
            True if successful

        Example:
            >>> # Embed a video
            >>> api.add_iframe(
            ...     survey_id, question_id,
            ...     iframe_url="https://www.youtube.com/embed/VIDEO_ID",
            ...     height="315px"
            ... )

            >>> # Embed external content at top
            >>> api.add_iframe(
            ...     survey_id, question_id,
            ...     iframe_url="https://example.com/content",
            ...     position="top"
            ... )
        """
        position_code = 'insertBefore' if position == 'top' else 'appendChild'
        reference_code = 'questionContainer.firstChild' if position == 'top' else 'null'

        javascript_code = f'''
Qualtrics.SurveyEngine.addOnload(function() {{
    var iframe = document.createElement('iframe');
    iframe.src = '{iframe_url}';
    iframe.style.cssText = 'width: {width}; height: {height}; border: 1px solid #ddd; margin: 10px 0;';
    iframe.frameBorder = '0';
    iframe.allowFullscreen = true;

    var questionContainer = this.getQuestionContainer();
    questionContainer.{position_code}(iframe, {reference_code});
}});
'''
        return self.add_question_javascript(survey_id, question_id, javascript_code)

    def add_next_button_modification(
        self,
        survey_id: str,
        question_id: str,
        button_text: Optional[str] = None,
        hide_button: bool = False,
        show_after_ms: Optional[int] = None,
        custom_style: Optional[str] = None
    ) -> bool:
        """
        Modify the next button behavior or appearance.

        Args:
            survey_id: The survey ID
            question_id: The question ID
            button_text: Custom text for the next button (e.g., "Continue", "Submit")
            hide_button: If True, hide the next button initially
            show_after_ms: If set, show the button after this many milliseconds
            custom_style: Custom CSS style string for the button

        Returns:
            True if successful

        Example:
            >>> # Change button text
            >>> api.add_next_button_modification(
            ...     survey_id, question_id,
            ...     button_text="Continue to Next Section"
            ... )

            >>> # Hide button for 5 seconds then show
            >>> api.add_next_button_modification(
            ...     survey_id, question_id,
            ...     hide_button=True,
            ...     show_after_ms=5000
            ... )

            >>> # Custom styled button
            >>> api.add_next_button_modification(
            ...     survey_id, question_id,
            ...     button_text="Submit Answer",
            ...     custom_style="background-color: #4CAF50; color: white; font-weight: bold;"
            ... )
        """
        js_parts = []

        js_parts.append('''
Qualtrics.SurveyEngine.addOnload(function() {
    var nextButton = document.getElementById('NextButton');
    if (!nextButton) return;
''')

        if button_text:
            js_parts.append(f"    nextButton.value = '{button_text}';")

        if custom_style:
            js_parts.append(f"    nextButton.style.cssText += '{custom_style}';")

        if hide_button:
            js_parts.append("    nextButton.style.display = 'none';")

            if show_after_ms:
                js_parts.append(f'''
    setTimeout(function() {{
        nextButton.style.display = '';
    }}, {show_after_ms});''')

        js_parts.append('});')

        javascript_code = '\n'.join(js_parts)
        return self.add_question_javascript(survey_id, question_id, javascript_code)

    def add_choice_style(
        self,
        survey_id: str,
        question_id: str,
        background_color: Optional[str] = None,
        border_radius: Optional[str] = None,
        hover_color: Optional[str] = None,
        selected_color: Optional[str] = None
    ) -> bool:
        """
        Add custom styling to response choices.

        Modifies the appearance of answer choices in multiple choice questions.

        Args:
            survey_id: The survey ID
            question_id: The question ID
            background_color: Background color for choices (e.g., "#f5f5f5")
            border_radius: Border radius (e.g., "8px")
            hover_color: Background color on hover (e.g., "#e0e0e0")
            selected_color: Background color when selected (e.g., "#bbdefb")

        Returns:
            True if successful

        Example:
            >>> # Style choices with rounded corners and colors
            >>> api.add_choice_style(
            ...     survey_id, question_id,
            ...     background_color="#f5f5f5",
            ...     border_radius="8px",
            ...     hover_color="#e0e0e0",
            ...     selected_color="#bbdefb"
            ... )
        """
        style_parts = []
        if background_color:
            style_parts.append(f'background-color: {background_color}')
        if border_radius:
            style_parts.append(f'border-radius: {border_radius}')

        base_style = '; '.join(style_parts) + ';' if style_parts else ''

        hover_style = f'background-color: {hover_color};' if hover_color else ''
        selected_style = f'background-color: {selected_color};' if selected_color else ''

        javascript_code = f'''
Qualtrics.SurveyEngine.addOnload(function() {{
    var choices = this.getChoices();
    var questionId = this.questionId;

    for (var i = 0; i < choices.length; i++) {{
        var choiceId = choices[i];
        var choiceElement = document.getElementById('QR~' + questionId + '~' + choiceId);
        if (!choiceElement) {{
            choiceElement = document.getElementById(questionId + '-' + choiceId + '-label');
        }}
        var choiceContainer = choiceElement ? choiceElement.closest('label, .ChoiceStructure') : null;

        if (choiceContainer) {{
            choiceContainer.style.cssText += '{base_style} padding: 10px; margin: 5px 0; transition: background-color 0.2s;';

            if ('{hover_style}') {{
                choiceContainer.onmouseover = function() {{
                    if (!this.classList.contains('selected')) {{
                        this.style.backgroundColor = '{hover_color}';
                    }}
                }};
                choiceContainer.onmouseout = function() {{
                    if (!this.classList.contains('selected')) {{
                        this.style.backgroundColor = '{background_color}';
                    }}
                }};
            }}
        }}
    }}

    if ('{selected_style}') {{
        this.questionclick = function(event, element) {{
            var choiceContainers = this.getQuestionContainer().querySelectorAll('.ChoiceStructure, label.SingleAnswer, label.MultipleAnswer');
            choiceContainers.forEach(function(container) {{
                container.style.backgroundColor = '{background_color}';
            }});
            var clicked = element.closest('.ChoiceStructure, label');
            if (clicked) {{
                clicked.style.backgroundColor = '{selected_color}';
            }}
        }};
    }}
}});
'''
        return self.add_question_javascript(survey_id, question_id, javascript_code)

    def _build_question_update_data(self, current_question: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build question update data preserving existing fields.

        This helper method creates a question data dictionary that preserves
        all existing question properties needed for a successful update.

        Args:
            current_question: The current question data from get_question()

        Returns:
            Dictionary with required fields for question update
        """
        question_data = {
            'QuestionText': current_question.get('QuestionText', ''),
            'QuestionType': current_question.get('QuestionType'),
            'Selector': current_question.get('Selector'),
        }

        # Include DataExportTag if present
        if current_question.get('DataExportTag'):
            question_data['DataExportTag'] = current_question['DataExportTag']

        # Include Configuration if present
        if current_question.get('Configuration'):
            question_data['Configuration'] = current_question['Configuration']

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

        # Include AnswerOrder if present
        if current_question.get('AnswerOrder'):
            question_data['AnswerOrder'] = current_question['AnswerOrder']

        # Include DisplayLogic if present
        if current_question.get('DisplayLogic'):
            question_data['DisplayLogic'] = current_question['DisplayLogic']

        # Include Validation if present
        if current_question.get('Validation'):
            question_data['Validation'] = current_question['Validation']

        # Include existing JavaScript if present
        if current_question.get('QuestionJS'):
            question_data['QuestionJS'] = current_question['QuestionJS']

        # Include QuestionDescription if present
        if current_question.get('QuestionDescription'):
            question_data['QuestionDescription'] = current_question['QuestionDescription']

        return question_data
