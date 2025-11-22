"""Framework detection analyzer that identifies CSS/JS frameworks used in templates"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set


class FrameworkDetector:
    """Detects which frameworks are used in templates"""

    def __init__(self, knowledge_base_path: str = "data/knowledge_base/design_patterns.json"):
        self.kb_path = Path(knowledge_base_path)
        self.framework_patterns = self._load_framework_patterns()

    def _load_framework_patterns(self) -> Dict:
        """Load framework patterns from knowledge base"""
        if not self.kb_path.exists():
            return {}

        try:
            kb_data = json.loads(self.kb_path.read_text())
            return kb_data.get('framework_patterns', {})
        except Exception as e:
            print(f"! Error loading framework patterns: {e}")
            return {}

    def detect_frameworks(self, html_content: str, css_content: str) -> Dict:
        """Detect frameworks used in the template"""
        detected = {
            'css_frameworks': [],
            'component_libraries': [],
            'animation_libraries': [],
            'confidence_scores': {},
            'detected_patterns': {}
        }

        # Detect CSS frameworks
        css_frameworks = self._detect_css_frameworks(html_content, css_content)
        detected['css_frameworks'] = css_frameworks

        # Detect component libraries
        component_libs = self._detect_component_libraries(html_content)
        detected['component_libraries'] = component_libs

        # Detect animation libraries
        anim_libs = self._detect_animation_libraries(html_content, css_content)
        detected['animation_libraries'] = anim_libs

        # Calculate confidence scores
        detected['confidence_scores'] = self._calculate_confidence_scores(
            html_content, css_content, detected
        )

        return detected

    def _detect_css_frameworks(self, html_content: str, css_content: str) -> List[str]:
        """Detect CSS frameworks like Bootstrap, Tailwind, Bulma"""
        detected = set()

        # Bootstrap detection
        bootstrap_patterns = [
            r'class="[^"]*\bcontainer\b',
            r'class="[^"]*\brow\b',
            r'class="[^"]*\bcol-',
            r'class="[^"]*\bbtn\b',
            r'class="[^"]*\bcard\b',
            r'class="[^"]*\bnavbar\b',
            r'class="[^"]*\bmodal\b',
            r'bootstrap\.min\.(css|js)',
        ]
        if self._match_patterns(html_content + css_content, bootstrap_patterns, min_matches=2):
            detected.add('Bootstrap')

        # Tailwind CSS detection
        tailwind_patterns = [
            r'class="[^"]*\b(flex|grid)\b',
            r'class="[^"]*\b(p|m|px|py|mx|my)-\d+',
            r'class="[^"]*\btext-(xs|sm|base|lg|xl|2xl)',
            r'class="[^"]*\bbg-(white|black|gray|red|blue|green)-\d{2,3}',
            r'class="[^"]*\bhover:',
            r'class="[^"]*\bfocus:',
            r'tailwind\.min\.css',
        ]
        if self._match_patterns(html_content + css_content, tailwind_patterns, min_matches=3):
            detected.add('Tailwind CSS')

        # Bulma detection
        bulma_patterns = [
            r'class="[^"]*\bcolumns\b',
            r'class="[^"]*\bcolumn\b',
            r'class="[^"]*\bbutton\b',
            r'class="[^"]*\bsection\b',
            r'class="[^"]*\bhero\b',
            r'bulma\.min\.css',
        ]
        if self._match_patterns(html_content + css_content, bulma_patterns, min_matches=2):
            detected.add('Bulma')

        # Foundation detection
        foundation_patterns = [
            r'class="[^"]*\bgrid-container\b',
            r'class="[^"]*\bgrid-x\b',
            r'class="[^"]*\bcell\b',
            r'foundation\.min\.css',
        ]
        if self._match_patterns(html_content + css_content, foundation_patterns, min_matches=2):
            detected.add('Foundation')

        # Normalize.css detection
        if re.search(r'normalize\.css', html_content + css_content, re.IGNORECASE):
            detected.add('Normalize.css')

        return list(detected)

    def _detect_component_libraries(self, html_content: str) -> List[str]:
        """Detect component libraries like Material-UI, Ant Design"""
        detected = set()

        # Material-UI detection
        material_patterns = [
            r'class="[^"]*\bMui',
            r'@material-ui',
            r'material-icons',
        ]
        if self._match_patterns(html_content, material_patterns):
            detected.add('Material-UI')

        # Ant Design detection
        ant_patterns = [
            r'class="[^"]*\bant-',
            r'antd',
        ]
        if self._match_patterns(html_content, ant_patterns):
            detected.add('Ant Design')

        # Vuetify detection
        vuetify_patterns = [
            r'class="[^"]*\bv-',
            r'vuetify',
        ]
        if self._match_patterns(html_content, vuetify_patterns):
            detected.add('Vuetify')

        # Element Plus detection
        element_patterns = [
            r'class="[^"]*\bel-',
            r'element-plus',
        ]
        if self._match_patterns(html_content, element_patterns):
            detected.add('Element Plus')

        return list(detected)

    def _detect_animation_libraries(self, html_content: str, css_content: str) -> List[str]:
        """Detect animation libraries like Animate.css"""
        detected = set()

        # Animate.css detection
        fp = self.framework_patterns
        anim_lib = fp.get('animation_library', {})
        keyframes = anim_lib.get('keyframes', [])

        # Check for common Animate.css classes
        animate_patterns = [
            r'class="[^"]*\banimate__',
            r'class="[^"]*\banimated\b',
            r'animate\.min\.css',
        ]

        # Check for specific animation keyframes
        for keyframe in keyframes[:10]:  # Check first 10 keyframes
            kf_name = keyframe.get('name', '')
            if kf_name and re.search(rf'\b{re.escape(kf_name)}\b', css_content, re.IGNORECASE):
                detected.add('Animate.css')
                break

        if self._match_patterns(html_content + css_content, animate_patterns):
            detected.add('Animate.css')

        return list(detected)

    def _match_patterns(self, content: str, patterns: List[str], min_matches: int = 1) -> bool:
        """Check if content matches minimum number of patterns"""
        matches = 0
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                matches += 1
                if matches >= min_matches:
                    return True
        return False

    def _calculate_confidence_scores(self, html_content: str, css_content: str, detected: Dict) -> Dict:
        """Calculate confidence scores for detected frameworks"""
        scores = {}

        # Bootstrap confidence
        if 'Bootstrap' in detected['css_frameworks']:
            bootstrap_count = len(re.findall(r'class="[^"]*\b(col-|btn|card|navbar|modal)', html_content))
            scores['Bootstrap'] = min(100, 50 + (bootstrap_count * 5))

        # Tailwind confidence
        if 'Tailwind CSS' in detected['css_frameworks']:
            tailwind_count = len(re.findall(r'class="[^"]*\b(p|m|px|py|mx|my)-\d+', html_content))
            scores['Tailwind CSS'] = min(100, 50 + (tailwind_count * 3))

        # Bulma confidence
        if 'Bulma' in detected['css_frameworks']:
            bulma_count = len(re.findall(r'class="[^"]*\b(columns|column|button)', html_content))
            scores['Bulma'] = min(100, 50 + (bulma_count * 5))

        # Animate.css confidence
        if 'Animate.css' in detected['animation_libraries']:
            anim_count = len(re.findall(r'class="[^"]*\b(animate__|animated)', html_content))
            scores['Animate.css'] = min(100, 50 + (anim_count * 10))

        return scores

    def get_framework_recommendations(self, detected_frameworks: List[str]) -> List[str]:
        """Get recommendations based on detected frameworks"""
        recommendations = []

        if 'Bootstrap' in detected_frameworks:
            recommendations.append("Consider using Bootstrap's utility classes for spacing and display")
            recommendations.append("Use Bootstrap's grid system consistently (container > row > col)")

        if 'Tailwind CSS' in detected_frameworks:
            recommendations.append("Leverage Tailwind's utility-first approach for rapid styling")
            recommendations.append("Use Tailwind's responsive prefixes (sm:, md:, lg:) for mobile-first design")

        if 'Bulma' in detected_frameworks:
            recommendations.append("Use Bulma's flexbox-based columns system")
            recommendations.append("Leverage Bulma's modifier classes (is-*, has-*)")

        if 'Animate.css' in detected_frameworks:
            recommendations.append("Use Animate.css classes for smooth animations")
            recommendations.append("Consider animation delays and durations for better UX")

        if not detected_frameworks:
            recommendations.append("Consider using a CSS framework like Bootstrap or Tailwind for consistency")
            recommendations.append("Add Animate.css for professional animations")

        return recommendations
