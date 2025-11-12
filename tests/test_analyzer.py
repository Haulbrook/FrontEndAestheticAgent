"""Tests for analyzer modules"""

import pytest
from agent.analyzer.color_analyzer import ColorAnalyzer
from agent.analyzer.layout_analyzer import LayoutAnalyzer
from agent.analyzer.typography_analyzer import TypographyAnalyzer


class TestColorAnalyzer:
    """Test color analysis functionality"""

    def test_extract_hex_colors(self):
        analyzer = ColorAnalyzer()
        html = "<div style='color: #FF0000; background: #00FF00;'>Test</div>"
        result = analyzer.analyze(html)

        assert result['total_colors'] >= 2
        assert any(c['color'] in ['#FF0000', '#00FF00'] for c in result['dominant_colors'])

    def test_detect_color_scheme(self):
        analyzer = ColorAnalyzer()
        css = """
        .class1 { color: #333; }
        .class2 { background: #666; }
        .class3 { border: 1px solid #999; }
        """
        result = analyzer.analyze("", css)

        assert 'color_scheme' in result
        assert result['color_scheme'] in ['minimal_dark', 'minimal_light', 'monochromatic', 'balanced']


class TestLayoutAnalyzer:
    """Test layout analysis functionality"""

    def test_detect_flexbox(self):
        analyzer = LayoutAnalyzer()
        css = """
        .container {
            display: flex;
            justify-content: center;
        }
        """
        result = analyzer.analyze("", css)

        assert result['layout_systems']['flexbox']['detected'] is True

    def test_detect_grid(self):
        analyzer = LayoutAnalyzer()
        css = """
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
        }
        """
        result = analyzer.analyze("", css)

        assert result['layout_systems']['grid']['detected'] is True

    def test_analyze_structure(self):
        analyzer = LayoutAnalyzer()
        html = """
        <html>
            <header class="navbar">Header</header>
            <main>Content</main>
            <footer>Footer</footer>
        </html>
        """
        result = analyzer.analyze(html)

        assert result['structure']['has_header'] is True
        assert result['structure']['has_footer'] is True


class TestTypographyAnalyzer:
    """Test typography analysis functionality"""

    def test_extract_fonts(self):
        analyzer = TypographyAnalyzer()
        css = """
        body {
            font-family: 'Inter', sans-serif;
        }
        h1 {
            font-family: 'Playfair Display', serif;
        }
        """
        result = analyzer.analyze("", css)

        assert result['fonts']['total_unique'] >= 2
        assert 'Inter' in result['fonts']['custom_fonts']

    def test_detect_web_fonts(self):
        analyzer = TypographyAnalyzer()
        html = '<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet">'
        result = analyzer.analyze(html)

        assert result['web_fonts']['google_fonts'] is True

    def test_analyze_headings(self):
        analyzer = TypographyAnalyzer()
        html = """
        <html>
            <h1>Title</h1>
            <h2>Subtitle</h2>
            <h3>Section</h3>
        </html>
        """
        result = analyzer.analyze(html)

        assert result['headings']['uses_semantic_headings'] is True
        assert result['headings']['heading_count']['h1'] == 1
        assert result['headings']['heading_count']['h2'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
