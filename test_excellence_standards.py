#!/usr/bin/env python3
"""
Test Script: Demonstrate Excellence-First Attitude

This script shows the bot's new perfectionist standards:
- Rejects mediocre designs (< 70/100)
- Only learns from sophisticated templates
- Provides demanding critiques
- Focuses on ornate details and immersive experiences
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.learner.design_excellence import DesignExcellence
from agent.generator.design_generator import DesignGenerator


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def main():
    """Main testing function."""
    print_header("✨ Testing Excellence-First Design Standards")

    excellence = DesignExcellence()

    # Test 1: Show Excellence Criteria
    print_header("TEST 1: Excellence Criteria & Philosophy")

    print("🎯 The Bot's New Attitude:\n")
    print("  • Quality over quantity - Never settle for mediocre")
    print("  • Sophistication over simplicity - Embrace refined complexity")
    print("  • Immersive over functional - Create memorable experiences")
    print("  • Ornate details over broad strokes - Obsess over refinement")
    print("  • Self-critique - Continuous improvement mindset\n")

    print("📊 Quality Thresholds:")
    print(f"  • Minimum Quality: {excellence.MINIMUM_QUALITY}/100 (Below this = REJECTED)")
    print(f"  • Excellent Quality: {excellence.EXCELLENT_QUALITY}/100 (Getting excited)")
    print(f"  • Masterpiece Quality: {excellence.MASTERPIECE_QUALITY}/100 (Reference-worthy)\n")

    # Test 2: Show What We Avoid vs. Pursue
    print_header("TEST 2: Cookie-Cutter vs. Sophisticated")

    print("🚫 What We Avoid (Cookie-Cutter Red Flags):\n")
    avoid = excellence.sophistication_markers['avoid']
    for key, desc in list(avoid.items())[:5]:
        print(f"  ⊘ {desc}")

    print("\n✨ What We Pursue (Sophistication Markers):\n")
    pursue = excellence.sophistication_markers['pursue']
    for key, desc in list(pursue.items())[:5]:
        print(f"  ★ {desc}")

    # Test 3: Generate Sophisticated Design Guide
    print_header("TEST 3: Sophisticated Design Guide Generation")

    generator = DesignGenerator()
    guide = generator.generate_complete_design_guide()

    print("📋 Excellence Principles (New!):\n")
    for principle in guide['excellence_principles'][:4]:
        print(f"  {principle}")

    print("\n⚠️  Anti-Patterns to Avoid:\n")
    for anti in guide['anti_patterns'][:4]:
        print(f"  {anti}")

    print("\n✨ Micro-Interactions (Delight Users):\n")
    hover_effects = guide['micro_interactions']['hover_effects']
    for effect in hover_effects[:3]:
        print(f"  • {effect}")

    print("\n🎨 Ornate Details (Refined Touches):\n")
    decorative = guide['ornate_details']['decorative_elements']
    for detail in decorative[:3]:
        print(f"  • {detail}")

    print("\n🌊 Immersive Techniques (Create Flow):\n")
    storytelling = guide['immersive_techniques']['storytelling']
    for technique in storytelling[:3]:
        print(f"  • {technique}")

    # Test 4: Self-Critique Example
    print_header("TEST 4: Self-Critique & Improvement Mindset")

    # Simulate a generated design
    simulated_design = {
        'colors': {'total_colors': 6, 'color_scheme': 'balanced'},
        'layout': {
            'layout_systems': {'grid': {'detected': True}, 'flexbox': {'detected': True}},
            'responsive': {'has_media_queries': True, 'responsive_score': 75}
        },
        'typography': {
            'fonts': {'total_unique': 2, 'custom_fonts': ['Inter', 'Playfair Display']},
            'headings': {'uses_semantic_headings': True}
        },
        'style': {
            'modern_features': {
                'css_variables': True,
                'animations': True,
                'transforms': True,
                'modernity_score': 80
            }
        },
        'frameworks': {'css_frameworks': []},
        'quality_score': 75
    }

    critique = excellence.generate_self_critique(simulated_design)
    assessment = critique['self_assessment']

    print("🤖 Bot evaluates its own work:\n")
    print(f"  Overall Score: {assessment['overall_score']}/100")
    print(f"  Excellence Level: {assessment['excellence_level']}")
    print(f"  Self-Confidence: {critique['confidence']}%")
    print(f"  Verdict: {assessment['verdict']}\n")

    if assessment['strengths']:
        print("  ✓ Strengths:")
        for strength in assessment['strengths'][:2]:
            print(f"    • {strength}")

    if assessment['refinement_opportunities']:
        print("\n  🔧 Self-Identified Improvements:")
        for improvement in assessment['refinement_opportunities'][:3]:
            print(f"    • {improvement}")

    # Test 5: Evaluation Examples
    print_header("TEST 5: Design Evaluation Examples")

    # Example 1: Mediocre design (would be rejected)
    print("📊 Example 1: Basic Bootstrap Template\n")
    mediocre = {
        'colors': {'total_colors': 3, 'color_scheme': 'unknown'},
        'layout': {
            'layout_systems': {'grid': {'detected': False}, 'flexbox': {'detected': True}},
            'responsive': {'has_media_queries': True, 'responsive_score': 60}
        },
        'typography': {
            'fonts': {'total_unique': 1},
            'headings': {'uses_semantic_headings': False}
        },
        'style': {'modern_features': {'modernity_score': 35}},
        'frameworks': {'css_frameworks': ['Bootstrap'], 'confidence_scores': {'Bootstrap': 95}},
        'quality_score': 45
    }

    eval_mediocre = excellence.evaluate_design(mediocre)
    print(f"  Score: {eval_mediocre['overall_score']}/100")
    print(f"  Level: {eval_mediocre['excellence_level']}")
    print(f"  Decision: {'✓ ACCEPT' if excellence.should_learn_from(mediocre) else '⊘ REJECT'}")
    print(f"  Verdict: {eval_mediocre['verdict']}")

    if eval_mediocre['critical_issues']:
        print(f"\n  Critical Issues:")
        for issue in eval_mediocre['critical_issues'][:2]:
            print(f"    🚨 {issue}")

    # Example 2: Excellent design (would be learned from eagerly)
    print("\n📊 Example 2: Sophisticated Custom Design\n")
    excellent = {
        'colors': {'total_colors': 8, 'color_scheme': 'vibrant', 'palette_characteristics': {'is_vibrant': True}},
        'layout': {
            'layout_systems': {'grid': {'detected': True}, 'flexbox': {'detected': True}},
            'responsive': {'has_media_queries': True, 'responsive_score': 90},
            'sections': {'total_sections': 8}
        },
        'typography': {
            'fonts': {'total_unique': 3, 'custom_fonts': ['Inter', 'Playfair Display', 'Fira Code']},
            'headings': {'uses_semantic_headings': True}
        },
        'style': {
            'modern_features': {
                'css_variables': True,
                'animations': True,
                'transforms': True,
                'transitions': True,
                'custom_properties': True,
                'modernity_score': 95
            }
        },
        'frameworks': {'css_frameworks': [], 'animation_libraries': ['Animate.css']},
        'quality_score': 88
    }

    eval_excellent = excellence.evaluate_design(excellent)
    print(f"  Score: {eval_excellent['overall_score']}/100")
    print(f"  Level: {eval_excellent['excellence_level']}")
    print(f"  Decision: {'★ LEARN EAGERLY' if excellence.should_learn_from(excellent) else '⊘ REJECT'}")
    print(f"  Priority: {excellence.get_learning_priority(excellent)}")
    print(f"  Verdict: {eval_excellent['verdict']}")

    if eval_excellent['strengths']:
        print(f"\n  Strengths:")
        for strength in eval_excellent['strengths']:
            print(f"    ✨ {strength}")

    # Summary
    print_header("✅ Excellence Standards Active!")

    print("📊 Summary of New Capabilities:\n")
    print("  1. ✓ Quality Filters - Rejects templates below 70/100")
    print("  2. ✓ Excellence Evaluation - Multi-criteria sophisticated scoring")
    print("  3. ✓ Self-Critique - Bot evaluates its own work")
    print("  4. ✓ Micro-Interactions Guide - Detailed delight recommendations")
    print("  5. ✓ Ornate Details Focus - Refined, sophisticated touches")
    print("  6. ✓ Immersive Techniques - Creating memorable experiences")
    print("  7. ✓ Anti-Patterns - Actively avoids cookie-cutter designs")
    print("  8. ✓ Continuous Improvement - Never satisfied, always refining\n")

    print("🎯 The Bot's New Mindset:")
    print("  'Good is the enemy of great. I pursue excellence,")
    print("   not mediocrity. Every design should be portfolio-worthy.'\n")


if __name__ == "__main__":
    main()
