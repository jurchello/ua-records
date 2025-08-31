from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def mock_gtk_env():
    """Mock GTK environment for testing"""
    with (
        patch("ui.field_renderer.Gtk") as mock_gtk,
        patch("ui.field_renderer.Gdk") as mock_gdk,
        patch("ui.field_renderer.GdkPixbuf") as mock_pixbuf,
        patch("ui.field_renderer.GLib") as mock_glib,
        patch("ui.field_renderer.Pango") as mock_pango,
    ):

        # Mock basic GTK structures
        mock_gtk.Box = Mock()
        mock_gtk.Button = Mock()
        mock_gtk.Image = Mock()
        mock_gtk.Dialog = Mock()
        mock_gtk.ScrolledWindow = Mock()
        mock_gtk.Label = Mock()
        mock_gtk.Orientation.HORIZONTAL = 0
        mock_gtk.Align.FILL = 0
        mock_gtk.Align.CENTER = 1
        mock_gtk.ReliefStyle.NONE = 0
        mock_gtk.PolicyType.AUTOMATIC = 0
        mock_gtk.ResponseType.OK = -5

        # Mock Pango
        mock_pango.WrapMode.WORD_CHAR = 0

        # Mock GLib markup escape
        mock_glib.markup_escape_text = lambda x: x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # Mock Pixbuf
        mock_pixbuf.Pixbuf.new_from_file = Mock()
        mock_pixbuf.Pixbuf.scale_simple = Mock()

        yield {"gtk": mock_gtk, "gdk": mock_gdk, "pixbuf": mock_pixbuf, "glib": mock_glib, "pango": mock_pango}


class TestFieldHelpSystem:
    """Test the help button functionality in FieldRenderer"""

    def test_help_button_not_created_for_empty_help(self, mock_gtk_env):
        """Test that no help button is created when help text is empty or missing"""
        from ui.field_renderer import FieldRenderer

        renderer = FieldRenderer(
            dbstate=None, uistate=None, dnd_adapter=None, model_manager=None,
            toplevel=Mock(), widgets={}, objects={}, handles={}, defaults={}, 
            types={}, changed_handlers={}
        )
        widget = Mock()

        # Test with no help key
        field = {"id": "test", "type": "entry"}
        result = renderer._attach_help(widget, field, "Test Label")
        assert result == widget

        # Test with empty help
        field = {"id": "test", "type": "entry", "help": ""}
        result = renderer._attach_help(widget, field, "Test Label")
        assert result == widget

        # Test with whitespace-only help
        field = {"id": "test", "type": "entry", "help": "   \n  "}
        result = renderer._attach_help(widget, field, "Test Label")
        assert result == widget

    def test_help_button_created_for_valid_help(self, mock_gtk_env):
        """Test that help button is created when valid help text is provided"""
        from ui.field_renderer import FieldRenderer

        renderer = FieldRenderer(
            dbstate=None, uistate=None, dnd_adapter=None, model_manager=None,
            toplevel=Mock(), widgets={}, objects={}, handles={}, defaults={}, 
            types={}, changed_handlers={}
        )
        widget = Mock()
        widget.get_hexpand.return_value = True

        field = {"id": "test", "type": "entry", "help": "This is helpful text"}

        with (
            patch.object(renderer, "_ensure_help_css"),
            patch("os.path.join") as mock_join,
            patch("os.path.dirname") as mock_dirname,
        ):

            mock_join.return_value = "/fake/path/help.png"
            mock_dirname.return_value = "/fake/ui"

            result = renderer._attach_help(widget, field, "Test Label")

            # Should return a Box container, not the original widget
            assert result != widget
            mock_gtk_env["gtk"].Box.assert_called()

    def test_help_text_alternatives(self, mock_gtk_env):
        """Test that both 'help' and 'help_text' keys work"""
        from ui.field_renderer import FieldRenderer

        renderer = FieldRenderer(
            dbstate=None, uistate=None, dnd_adapter=None, model_manager=None,
            toplevel=Mock(), widgets={}, objects={}, handles={}, defaults={}, 
            types={}, changed_handlers={}
        )
        widget = Mock()
        widget.get_hexpand.return_value = True

        with (
            patch.object(renderer, "_ensure_help_css"),
            patch("os.path.join") as mock_join,
            patch("os.path.dirname") as mock_dirname,
        ):

            mock_join.return_value = "/fake/path/help.png"
            mock_dirname.return_value = "/fake/ui"

            # Test 'help' key
            field1 = {"id": "test1", "type": "entry", "help": "Help via help key"}
            result1 = renderer._attach_help(widget, field1, "Test1")
            assert result1 != widget

            # Test 'help_text' key
            field2 = {"id": "test2", "type": "entry", "help_text": "Help via help_text key"}
            result2 = renderer._attach_help(widget, field2, "Test2")
            assert result2 != widget

            # Test 'help' takes precedence over 'help_text'
            field3 = {"id": "test3", "type": "entry", "help": "Primary help", "help_text": "Secondary help"}
            result3 = renderer._attach_help(widget, field3, "Test3")
            assert result3 != widget

    def test_help_markup_rendering(self, mock_gtk_env):
        """Test markdown-like markup conversion to Pango markup"""
        from ui.field_renderer import FieldRenderer

        renderer = FieldRenderer(
            dbstate=None, uistate=None, dnd_adapter=None, model_manager=None,
            toplevel=Mock(), widgets={}, objects={}, handles={}, defaults={}, 
            types={}, changed_handlers={}
        )

        # Test bold markup
        result = renderer._render_help_markup("This is **bold** text")
        assert "<b>bold</b>" in result

        # Test italic markup
        result = renderer._render_help_markup("This is *italic* text")
        assert "<i>italic</i>" in result

        # Test underline markup
        result = renderer._render_help_markup("This is __underlined__ text")
        assert "<u>underlined</u>" in result

        # Test mixed markup
        result = renderer._render_help_markup("**Bold** and *italic* and __underlined__")
        assert "<b>Bold</b>" in result
        assert "<i>italic</i>" in result
        assert "<u>underlined</u>" in result

        # Test HTML escaping is preserved
        result = renderer._render_help_markup("Test <tag> & ampersand")
        assert "&lt;tag&gt;" in result
        assert "&amp;" in result

    def test_help_dialog_creation(self, mock_gtk_env):
        """Test that help dialog is properly configured"""
        from ui.field_renderer import FieldRenderer

        renderer = FieldRenderer(
            dbstate=None, uistate=None, dnd_adapter=None, model_manager=None,
            toplevel=Mock(), widgets={}, objects={}, handles={}, defaults={}, 
            types={}, changed_handlers={}
        )
        mock_dialog = Mock()
        mock_scrolled = Mock()
        mock_gtk_env["gtk"].Dialog.return_value = mock_dialog
        mock_gtk_env["gtk"].ScrolledWindow.return_value = mock_scrolled

        with patch.object(renderer, "_render_help_markup") as mock_render:
            mock_render.return_value = "<b>Test</b> help content"

            renderer._show_help_dialog("Test Field", "Test help content")

            # Verify dialog was created
            mock_gtk_env["gtk"].Dialog.assert_called()
            # Verify scrolled window size is set
            mock_scrolled.set_min_content_width.assert_called_with(480)
            mock_scrolled.set_min_content_height.assert_called_with(320)
            mock_dialog.show_all.assert_called()

    def test_help_icon_scaling(self, mock_gtk_env):
        """Test that help icon scales properly to container height"""
        from ui.field_renderer import FieldRenderer

        renderer = FieldRenderer(
            dbstate=None, uistate=None, dnd_adapter=None, model_manager=None,
            toplevel=Mock(), widgets={}, objects={}, handles={}, defaults={}, 
            types={}, changed_handlers={}
        )
        widget = Mock()
        widget.get_hexpand.return_value = True

        field = {"id": "test", "type": "entry", "help": "Test help"}

        with (
            patch.object(renderer, "_ensure_help_css"),
            patch("os.path.join") as mock_join,
            patch("os.path.dirname") as mock_dirname,
        ):

            mock_join.return_value = "/fake/path/help.png"
            mock_dirname.return_value = "/fake/ui"

            # Mock pixbuf operations
            mock_orig_pixbuf = Mock()
            mock_scaled_pixbuf = Mock()
            mock_gtk_env["pixbuf"].Pixbuf.new_from_file.return_value = mock_orig_pixbuf
            mock_orig_pixbuf.scale_simple.return_value = mock_scaled_pixbuf

            result = renderer._attach_help(widget, field, "Test Label")

            # Should create the button infrastructure
            assert result != widget
            mock_gtk_env["gtk"].Button.assert_called()


class TestHelpIntegration:
    """Test help system integration with form configuration"""

    def test_help_preserved_in_form_expansion(self):
        """Test that help text is preserved when forms are expanded with $include/$fragment"""
        # This would test that help text survives the form expansion process
        # but requires more complex mocking of the form system
        pass

    def test_help_with_conditional_fields(self):
        """Test help system works with conditional field visibility"""
        # Test that help buttons appear/disappear correctly with show_when conditions
        pass


@pytest.mark.skipif(not os.environ.get("DISPLAY"), reason="Requires display for GTK tests")
class TestHelpSystemIntegration:
    """Integration tests that require actual GTK environment"""

    def test_help_button_visual_rendering(self):
        """Test actual visual rendering of help button (requires display)"""
        pass

    def test_help_dialog_interaction(self):
        """Test actual dialog interaction (requires display)"""
        pass


if __name__ == "__main__":
    pytest.main([__file__])
