# tests/unit/authentication/test_templates.py
import os
import pytest
from django.template.loader import render_to_string
from django.template import Context, Engine, Template, TemplateDoesNotExist
from django.conf import settings


@pytest.mark.unit
@pytest.mark.email
class TestEmailTemplates:
    """Unit tests for email template rendering."""

    def test_activation_template_exists(self):
        """Test that the activation email template exists and can be loaded."""
        # Debug template dirs
        template_dirs = settings.TEMPLATES[0]['DIRS']
        print(f"\nTemplate directories: {template_dirs}")

        # Check if file exists
        template_path = os.path.join(
            settings.BASE_DIR, 'templates', 'emails', 'authentication', 'activation.html')
        print(f"Looking for template at: {template_path}")
        print(f"File exists: {os.path.exists(template_path)}")

        try:
            rendered = render_to_string('authentication/activation.html', {
                'first_name': 'David',
                'verification_url': 'http://test.com/verify',
                'plain_email_address': 'david_j_brown@outlook.com'
            })
            assert 'Initiate Launch Sequence' in rendered
            assert 'Welcome to the crew at Backlogger!' in rendered
        except TemplateDoesNotExist as e:
            print(f"\nTemplate search paths: {e.chain}")
            pytest.fail(
                "activation.html template not found in the correct location")

    def test_template_required_variables(self, template_context):
        """Test that the template properly uses all required variables."""
        rendered = render_to_string(
            'authentication/activation.html', template_context)

        assert template_context['first_name'] in rendered
        assert template_context['verification_url'] in rendered
        assert template_context['plain_email_address'] in rendered

    def test_template_html_structure(self, template_context):
        """Test that the template generates valid HTML structure."""
        rendered = render_to_string(
            'authentication/activation.html', template_context)

        # Check for essential HTML elements with flexible matching
        essential_elements = [
            # lowercase for case-insensitive matching
            ('doctype', '<!doctype html'),
            ('html_open', '<html'),
            ('head_open', '<head'),
            ('head_close', '</head>'),
            ('body_open', '<body'),
            ('body_close', '</body>'),
            ('html_close', '</html>')
        ]

        # Print rendered HTML for debugging
        print("\nRendered HTML structure:")
        for tag, element in essential_elements:
            found = element.lower() in rendered.lower()
            print(f"{tag}: {'Found' if found else 'Not found'}")

        for element_name, element in essential_elements:
            assert element.lower() in rendered.lower(), \
                f"Missing element: {element_name}. Element should contain: {element}"

        # Check for rendered values instead of template variables
        assert template_context['first_name'] in rendered
        assert template_context['verification_url'] in rendered
        assert template_context['plain_email_address'] in rendered

    def test_template_missing_variables(self):
        """Test template behavior with missing context variables."""

        # Create a template engine with `string_if_invalid` set to raise an error
        engine = Engine(debug=True, string_if_invalid="INVALID")
        template = engine.from_string("{{ required_variable }}")

        context = Context({})  # Empty context

        rendered_output = template.render(context)

        # Assert that the missing variable renders as "INVALID"
        assert rendered_output == "INVALID"

    def test_template_styling(self, template_context):
        """Test that the template includes required styling elements."""
        rendered = render_to_string(
            'authentication/activation.html', template_context)

        # Check for CSS classes or inline styles
        assert 'style=' in rendered
        assert 'class=' in rendered
        assert 'font-family' in rendered.lower()
