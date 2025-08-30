#!/usr/bin/env python3
"""
Comprehensive test runner for ContextEvaluator on the master dataset.
Tests all lexical items from a single comprehensive dataset with feedback evaluation.
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, List
from pathlib import Path
import time

# Add src to path so we can import the evaluator
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

from services.context_evaluator import ContextEvaluator

# Try to import Langfuse, but make it optional
try:
    from langfuse import get_client
    LANGFUSE_AVAILABLE = True
    print("✅ Langfuse available for dataset runs")
except ImportError:
    print("⚠️  Langfuse not available, running without tracking")
    LANGFUSE_AVAILABLE = False


class MasterDatasetEvaluationRunner:
    """Test ContextEvaluator on the master dataset with comprehensive evaluation."""
    
    def __init__(self):
        # Check for required environment variables
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Missing OPENAI_API_KEY environment variable")
            raise ValueError("OPENAI_API_KEY is required")
        
        # Initialize Langfuse if available and enabled
        self.langfuse_client = None
        langfuse_enabled = os.getenv("LANGFUSE_ENABLED", "1").lower() in ("1", "true", "yes", "on")
        
        if LANGFUSE_AVAILABLE and langfuse_enabled:
            if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
                self.langfuse_client = get_client()
                print("✅ Langfuse client initialized for master dataset evaluation")
            else:
                print("⚠️  Langfuse credentials not found, running without tracking")
        elif not langfuse_enabled:
            print("⚠️  Langfuse disabled via LANGFUSE_ENABLED=0, running without tracking")
        else:
            print("⚠️  Langfuse not available, running without tracking")
        
        self.evaluator = ContextEvaluator()
        # Clear cache to ensure fresh evaluations
        self.evaluator.clear_cache()
        print("✅ Initialized ContextEvaluator for master dataset runner (cache cleared)")

    def get_master_dataset_from_langfuse(self) -> List[Dict[str, Any]]:
        """Retrieve the master dataset from Langfuse."""
        if not self.langfuse_client:
            raise ValueError("Langfuse client required to fetch master dataset")
        
        dataset_name = "context-evaluator-master-comprehensive"
        
        try:
            # Get dataset from Langfuse
            dataset = self.langfuse_client.get_dataset(dataset_name)
            
            # Get dataset items
            dataset_items = dataset.items
            test_cases = []
            
            for item in dataset_items:
                test_case = {
                    "input": item.input,
                    "expected_output": item.expected_output,
                    "metadata": item.metadata or {}
                }
                test_cases.append(test_case)
            
            print(f"📁 Retrieved {len(test_cases)} test cases from master dataset")
            return test_cases
            
        except Exception as e:
            print(f"❌ Error retrieving master dataset: {e}")
            raise

    def load_master_dataset_from_files(self) -> List[Dict[str, Any]]:
        """Load master dataset from consolidated local file."""
        consolidated_filepath = os.path.join(os.path.dirname(__file__), "all_lexical_items_comprehensive_test_cases.json")
        
        if not os.path.exists(consolidated_filepath):
            raise FileNotFoundError(f"Consolidated test file not found: {consolidated_filepath}")
        
        print(f"📁 Loading from consolidated file: {consolidated_filepath}")
        with open(consolidated_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_test_cases = []
        for test_case in data["test_cases"]:
            # The consolidated file already has the proper structure
            all_test_cases.append(test_case)
        
        print(f"🎯 Loaded {len(all_test_cases)} test cases from consolidated dataset")
        return all_test_cases

    async def run_master_dataset_evaluation(self) -> Dict[str, Any]:
        """Run evaluation on the master dataset."""
        print("🚀 Running ContextEvaluator evaluation on master dataset...")
        
        # Try to load from Langfuse first, fallback to local files
        try:
            if self.langfuse_client:
                print("🔄 Attempting to load master dataset from Langfuse...")
                test_cases = self.get_master_dataset_from_langfuse()
            else:
                print("📁 Loading master dataset from local files...")
                test_cases = self.load_master_dataset_from_files()
        except Exception as e:
            print(f"⚠️  Failed to load from Langfuse, using local files: {e}")
            test_cases = self.load_master_dataset_from_files()
        
        if not test_cases:
            raise FileNotFoundError("No test cases found. Please generate and upload master dataset first.")
        
        # Create run metadata for master dataset evaluation
        run_name = f"context-evaluator-master-{int(time.time())}"
        run_description = "ContextEvaluator comprehensive accuracy test on master dataset (all lexical items)"
        
        # Group by lexical items for tracking
        lexical_items = {}
        for test_case in test_cases:
            lexical_item = test_case["metadata"].get("lexical_item", "unknown")
            if lexical_item not in lexical_items:
                lexical_items[lexical_item] = []
            lexical_items[lexical_item].append(test_case)
        
        print(f"📋 Master dataset contains {len(lexical_items)} lexical items:")
        for item, cases in lexical_items.items():
            print(f"   {item.upper()}: {len(cases)} cases")
        
        # Get dataset for creating runs
        langfuse_dataset = None
        if self.langfuse_client:
            try:
                langfuse_dataset = self.langfuse_client.get_dataset("context-evaluator-master-comprehensive")
                print("✅ Retrieved master dataset for run creation")
            except Exception as e:
                print(f"⚠️  Could not get dataset for run creation: {e}")
                langfuse_dataset = None
        
        # Track Langfuse upload success
        langfuse_success_count = 0
        langfuse_failure_count = 0
        
        # Run evaluation concurrently
        semaphore = asyncio.Semaphore(5)  # Max 5 concurrent evaluations
        
        async def evaluate_case_with_semaphore(i: int, test_case: Dict[str, Any], dataset_item=None) -> Dict[str, Any]:
            async with semaphore:
                try:
                    result = await self._evaluate_single_case(test_case, dataset_item, run_name)
                    
                    # Print progress every 20 cases
                    if (i + 1) % 20 == 0:
                        lexical_item = test_case["metadata"].get("lexical_item", "unknown")
                        status = "✅" if result['correct'] else "❌"
                        print(f"   {status} Test {i+1}/{len(test_cases)}: {lexical_item.upper()} {result['category']}")
                    
                    return result
                    
                except Exception as e:
                    lexical_item = test_case['metadata'].get('lexical_item', 'unknown')
                    category = test_case['metadata'].get('category', 'unknown')
                    error_message = str(e)
                    
                    # Detect critical parsing/response errors
                    is_critical_error = any(keyword in error_message.lower() for keyword in [
                        'json', 'parse', 'expecting value', 'decode', 'invalid', 'malformed',
                        'timeout', 'connection', 'api', 'rate limit', 'quota'
                    ])
                    
                    error_details = {
                        'error_type': type(e).__name__,
                        'error_message': error_message,
                        'input_text': test_case['input'].get('user_text', 'N/A'),
                        'lexical_item': lexical_item,
                        'category': category,
                        'is_critical': is_critical_error
                    }
                    
                    if (i + 1) % 20 == 0:
                        error_icon = "🔥" if is_critical_error else "❌"
                        print(f"   {error_icon} Test {i+1} Error: {lexical_item.upper()} {category} - {str(e)[:50]}...")
                    
                    return {
                        'correct': False,
                        'category': category,
                        'lexical_item': lexical_item,
                        'error': error_message,
                        'error_details': error_details,
                        'execution_error': True,
                        'critical_error': is_critical_error
                    }
        
        # Create tasks for all test cases, pairing with dataset items if available
        tasks = []
        dataset_items_available = 0
        if langfuse_dataset:
            dataset_items_available = len(langfuse_dataset.items)
            print(f"📊 Dataset items available: {dataset_items_available}")
        
        for i, test_case in enumerate(test_cases):
            dataset_item = None
            if langfuse_dataset and i < len(langfuse_dataset.items):
                dataset_item = langfuse_dataset.items[i]
                # Debug: check if test case input matches dataset item input
                if dataset_item.input != test_case["input"]:
                    print(f"⚠️  Input mismatch at index {i}: dataset vs test case")
            tasks.append(evaluate_case_with_semaphore(i, test_case, dataset_item))
        
        print(f"🎯 Created {len(tasks)} evaluation tasks ({dataset_items_available} with Langfuse tracking)")
        
        # Run all test cases concurrently
        print(f"🚀 Running {len(tasks)} test cases concurrently...")
        results = await asyncio.gather(*tasks)
        
        # Calculate Langfuse upload statistics
        total_langfuse_uploads = sum(1 for r in results if r.get('langfuse_uploaded', False))
        failed_langfuse_uploads = len(results) - total_langfuse_uploads
        
        print(f"📊 Langfuse Upload Summary:")
        print(f"   ✅ Successfully uploaded: {total_langfuse_uploads}/{len(results)}")
        if failed_langfuse_uploads > 0:
            print(f"   ❌ Failed uploads: {failed_langfuse_uploads}")
        
        # Flush Langfuse client if available
        if self.langfuse_client:
            try:
                print("📤 Flushing results to Langfuse...")
                self.langfuse_client.flush()
            except Exception as e:
                print(f"⚠️  Error flushing to Langfuse: {e}")
        
        # Compile comprehensive summary
        summary = self._compile_master_summary(results, run_name)
        return summary


    async def _evaluate_single_case(self, test_case: Dict[str, Any], dataset_item=None, run_name: str = "") -> Dict[str, Any]:
        """Evaluate a single test case."""
        input_data = test_case["input"]
        expected = test_case["expected_output"]
        metadata = test_case["metadata"]
        
        # Use dataset.run() context if available
        if dataset_item:
            try:
                # Run within dataset context for proper Langfuse tracking
                with dataset_item.run(
                    run_name=run_name,
                    run_description=f"ContextEvaluator evaluation of {metadata.get('lexical_item', 'unknown')}",
                    run_metadata={
                        "evaluator": "ContextEvaluator",
                        "lexical_item": metadata.get("lexical_item", "unknown"),
                        "category": metadata.get("category", "unknown")
                    }
                ) as root_span:
                    # Run the evaluator
                    result = await self.evaluator.evaluate_usage(
                        user_text=input_data["user_text"],
                        lexical_item=input_data["phrasal_verb"],  # Keep backward compatibility
                        lexical_item_definition=input_data["phrasal_verb_definition"],
                        scenario=input_data["scenario"],
                        lexical_item_examples=input_data.get("phrasal_verb_examples", []),
                        character=input_data.get("character")
                    )
                    
                    # Check accuracy
                    used_correctly_match = result["used_correctly"] == expected["used_correctly"]
                    used_verb_match = result["used_verb"] == expected["used_verb"]
                    overall_correct = used_correctly_match and used_verb_match
                    
                    # Check feedback accuracy if applicable
                    feedback_match = None
                    if not expected["used_correctly"] and expected.get("expected_feedback"):
                        actual_feedback = result.get("feedback", "")
                        
                        # Simple feedback matching (could be enhanced with semantic similarity)
                        feedback_match = len(actual_feedback) > 0 and any(
                            key_word in actual_feedback.lower() 
                            for key_word in ["wrong", "incorrect", "try", "instead", "error", "should"]
                        )
                    
                    # Score the trace with evaluation results
                    root_span.score_trace(
                        name="overall_correct",
                        value=1.0 if overall_correct else 0.0,
                        comment=f"Used correctly: {used_correctly_match}, Used verb: {used_verb_match}"
                    )
                    
                    if feedback_match is not None:
                        root_span.score_trace(
                            name="feedback_quality",
                            value=1.0 if feedback_match else 0.0,
                            comment="Feedback provided helpful correction"
                        )
            except Exception as langfuse_error:
                print(f"⚠️  Langfuse dataset run failed for {metadata.get('lexical_item', 'unknown')} {metadata.get('category', 'unknown')}: {langfuse_error}")
                # Fall back to running without Langfuse tracking
                result = await self.evaluator.evaluate_usage(
                    user_text=input_data["user_text"],
                    lexical_item=input_data["phrasal_verb"],  # Keep backward compatibility
                    lexical_item_definition=input_data["phrasal_verb_definition"],
                    scenario=input_data["scenario"],
                    lexical_item_examples=input_data.get("phrasal_verb_examples", []),
                    character=input_data.get("character")
                )
                
                # Check accuracy
                used_correctly_match = result["used_correctly"] == expected["used_correctly"]
                used_verb_match = result["used_verb"] == expected["used_verb"]
                overall_correct = used_correctly_match and used_verb_match
                
                # Check feedback accuracy if applicable
                feedback_match = None
                if not expected["used_correctly"] and expected.get("expected_feedback"):
                    actual_feedback = result.get("feedback", "")
                    
                    # Simple feedback matching (could be enhanced with semantic similarity)
                    feedback_match = len(actual_feedback) > 0 and any(
                        key_word in actual_feedback.lower() 
                        for key_word in ["wrong", "incorrect", "try", "instead", "error", "should"]
                    )
        else:
            # Run without Langfuse tracking
            result = await self.evaluator.evaluate_usage(
                user_text=input_data["user_text"],
                lexical_item=input_data["phrasal_verb"],  # Keep backward compatibility
                lexical_item_definition=input_data["phrasal_verb_definition"],
                scenario=input_data["scenario"],
                lexical_item_examples=input_data.get("phrasal_verb_examples", []),
                character=input_data.get("character")
            )
            
            # Check accuracy
            used_correctly_match = result["used_correctly"] == expected["used_correctly"]
            used_verb_match = result["used_verb"] == expected["used_verb"]
            overall_correct = used_correctly_match and used_verb_match
            
            # Check feedback accuracy if applicable
            feedback_match = None
            if not expected["used_correctly"] and expected.get("expected_feedback"):
                actual_feedback = result.get("feedback", "")
                
                # Simple feedback matching (could be enhanced with semantic similarity)
                feedback_match = len(actual_feedback) > 0 and any(
                    key_word in actual_feedback.lower() 
                    for key_word in ["wrong", "incorrect", "try", "instead", "error", "should"]
                )
        
        # Determine if Langfuse upload was successful
        langfuse_uploaded = dataset_item is not None
        if dataset_item:
            # Check if we fell back to non-Langfuse evaluation (would be in locals)
            langfuse_uploaded = 'langfuse_error' not in locals()
        
        evaluation_result = {
            "input_text": input_data["user_text"],
            "lexical_item": metadata.get("lexical_item", "unknown"),
            "category": metadata.get("category", "unknown"),
            "source_dataset": metadata.get("source_dataset", "unknown"),
            "expected": {
                "used_correctly": expected["used_correctly"],
                "used_verb": expected["used_verb"],
                "feedback": expected.get("expected_feedback", "")
            },
            "actual": {
                "used_correctly": result["used_correctly"],
                "used_verb": result["used_verb"],
                "feedback": result.get("feedback", "")
            },
            "evaluator_response": result,
            "correct": overall_correct,
            "difficulty": metadata.get("difficulty", "unknown"),
            "scenario_character": metadata.get("scenario_character", "unknown"),
            "langfuse_uploaded": langfuse_uploaded
        }
        
        if feedback_match is not None:
            evaluation_result["feedback_match"] = feedback_match
            
        return evaluation_result

    def _compile_master_summary(self, results: List[Dict[str, Any]], run_name: str) -> Dict[str, Any]:
        """Compile comprehensive summary for master dataset evaluation."""
        total_tests = len(results)
        correct_tests = sum(1 for r in results if r.get('correct', False))
        execution_errors = [r for r in results if r.get('execution_error', False)]
        critical_errors = [r for r in results if r.get('critical_error', False)]
        
        # Group by lexical item
        lexical_item_stats = {}
        for result in results:
            lexical_item = result.get('lexical_item', 'unknown')
            if lexical_item not in lexical_item_stats:
                lexical_item_stats[lexical_item] = {"total": 0, "correct": 0, "errors": 0, "categories": {}}
            
            lexical_item_stats[lexical_item]["total"] += 1
            if result.get('correct', False):
                lexical_item_stats[lexical_item]["correct"] += 1
            if result.get('execution_error', False):
                lexical_item_stats[lexical_item]["errors"] += 1
            
            # Track categories within each lexical item
            category = result.get('category', 'unknown')
            if category not in lexical_item_stats[lexical_item]["categories"]:
                lexical_item_stats[lexical_item]["categories"][category] = {"total": 0, "correct": 0, "errors": 0}
            
            lexical_item_stats[lexical_item]["categories"][category]["total"] += 1
            if result.get('correct', False):
                lexical_item_stats[lexical_item]["categories"][category]["correct"] += 1
            if result.get('execution_error', False):
                lexical_item_stats[lexical_item]["categories"][category]["errors"] += 1
        
        # Calculate accuracy per lexical item
        for lexical_item in lexical_item_stats:
            stats = lexical_item_stats[lexical_item]
            stats["accuracy"] = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
            
            # Calculate category accuracy within each lexical item
            for category in stats["categories"]:
                cat_stats = stats["categories"][category]
                cat_stats["accuracy"] = cat_stats["correct"] / cat_stats["total"] if cat_stats["total"] > 0 else 0.0
        
        # Overall category breakdown (across all lexical items)
        category_totals = {}
        for result in results:
            category = result.get('category', 'unknown')
            if category not in category_totals:
                category_totals[category] = {"total": 0, "correct": 0, "errors": 0}
            
            category_totals[category]["total"] += 1
            if result.get('correct', False):
                category_totals[category]["correct"] += 1
            if result.get('execution_error', False):
                category_totals[category]["errors"] += 1
        
        # Calculate overall category accuracy
        for category in category_totals:
            stats = category_totals[category]
            stats["accuracy"] = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
        
        # Failed cases
        failed_cases = [r for r in results if not r.get('correct', False)]
        
        return {
            "run_name": run_name,
            "overall_accuracy": correct_tests / total_tests if total_tests > 0 else 0.0,
            "total_tests": total_tests,
            "correct_tests": correct_tests,
            "failed_tests": len(failed_cases),
            "execution_errors": len(execution_errors),
            "critical_errors": len(critical_errors),
            "lexical_items_tested": len(lexical_item_stats),
            "lexical_item_breakdown": lexical_item_stats,
            "category_breakdown": category_totals,
            "failed_cases": failed_cases,  # Include all failed cases for detailed analysis
            "execution_error_cases": execution_errors,  # Include all execution errors
            "critical_error_cases": critical_errors  # Include all critical errors
        }

    def print_master_summary(self, summary: Dict[str, Any]) -> None:
        """Print comprehensive summary of master dataset evaluation."""
        print("\n" + "="*100)
        print("📊 MASTER DATASET EVALUATION RESULTS")
        print("="*100)
        
        # CRITICAL ERRORS - Show at the very top with maximum prominence
        if summary.get('critical_errors', 0) > 0:
            print("\n" + "🔥" * 100)
            print("🚨🚨🚨 CRITICAL SYSTEM ERRORS DETECTED 🚨🚨🚨")
            print("🔥" * 100)
            print(f"💥 {summary['critical_errors']} CRITICAL ERRORS occurred during evaluation!")
            print("💥 These are likely JSON parsing, API, or connection issues that need immediate attention!")
            print("💥 See detailed analysis at the bottom of this report!")
            print("🔥" * 100)
        
        # Overall Results
        print(f"\n📈 Overall Accuracy: {summary['overall_accuracy']:.1%} ({summary['correct_tests']}/{summary['total_tests']})")
        print(f"🎯 Lexical Items Tested: {summary['lexical_items_tested']}")
        print(f"📋 Run Name: {summary['run_name']}")
        
        # Show execution errors prominently if any
        if summary.get('execution_errors', 0) > 0:
            print(f"🚨 EXECUTION ERRORS: {summary['execution_errors']} tests failed to execute properly")
            if summary.get('critical_errors', 0) > 0:
                print(f"   └── Including {summary['critical_errors']} CRITICAL system errors (see below)")
        
        if summary['overall_accuracy'] >= 0.8:
            print("✅ PASS: Overall accuracy meets 80% threshold")
        else:
            print("❌ FAIL: Overall accuracy below 80% threshold")
        
        # Detailed Results by Lexical Item
        print(f"\n📋 DETAILED RESULTS BY LEXICAL ITEM:")
        print("-" * 100)
        for item, stats in summary['lexical_item_breakdown'].items():
            error_info = f" [🚨 {stats.get('errors', 0)} errors]" if stats.get('errors', 0) > 0 else ""
            print(f"\n🔸 {item.upper()} - Overall: {stats['accuracy']:.1%} ({stats['correct']}/{stats['total']}){error_info}")
            
            # Show category breakdown within each lexical item
            if 'categories' in stats:
                print(f"   Category Breakdown:")
                for category, cat_stats in stats['categories'].items():
                    status_icon = "✅" if cat_stats['accuracy'] >= 0.8 else "⚠️" if cat_stats['accuracy'] >= 0.6 else "❌"
                    error_suffix = f" [🚨{cat_stats.get('errors', 0)}]" if cat_stats.get('errors', 0) > 0 else ""
                    print(f"   {status_icon} {category:15} {cat_stats['accuracy']:6.1%} ({cat_stats['correct']}/{cat_stats['total']}){error_suffix}")
        
        # Overall Category Performance
        print(f"\n📋 OVERALL CATEGORY PERFORMANCE:")
        print("-" * 100)
        for category, stats in summary['category_breakdown'].items():
            status_icon = "✅" if stats['accuracy'] >= 0.8 else "⚠️" if stats['accuracy'] >= 0.6 else "❌"
            error_suffix = f" [🚨{stats.get('errors', 0)}]" if stats.get('errors', 0) > 0 else ""
            print(f"{status_icon} {category:20} {stats['accuracy']:6.1%} ({stats['correct']}/{stats['total']}){error_suffix}")
        
        # Detailed Failure Analysis
        if summary['failed_tests'] > 0:
            print(f"\n❌ DETAILED FAILURE ANALYSIS ({summary['failed_tests']} total failures):")
            print("=" * 100)
            
            # Group failures by lexical item and category
            failure_groups = {}
            for failure in summary['failed_cases']:
                lexical_item = failure['lexical_item']
                category = failure['category']
                key = f"{lexical_item}_{category}"
                
                if key not in failure_groups:
                    failure_groups[key] = []
                failure_groups[key].append(failure)
            
            for group_key, failures in failure_groups.items():
                lexical_item, category = group_key.split('_', 1)
                print(f"\n🔸 {lexical_item.upper()} - {category.upper()} ({len(failures)} failures):")
                
                for i, failure in enumerate(failures[:5]):  # Show up to 5 per group
                    print(f"\n   Failure {i+1}:")
                    print(f"   📝 Input: {failure['input_text']}")
                    print(f"   🎯 Expected: used_correctly={failure['expected']['used_correctly']}, used_verb={failure['expected']['used_verb']}")
                    print(f"   🤖 Actual:   used_correctly={failure['actual']['used_correctly']}, used_verb={failure['actual']['used_verb']}")
                    
                    # Show feedback comparison if applicable
                    if failure['expected'].get('feedback') or failure['actual'].get('feedback'):
                        print(f"   💬 Expected Feedback: {failure['expected'].get('feedback', 'None')}")
                        print(f"   💬 Actual Feedback:   {failure['actual'].get('feedback', 'None')}")
                    
                    # Show difficulty and other metadata
                    if 'difficulty' in failure:
                        print(f"   📊 Difficulty: {failure['difficulty']}")
                    
                    if i < len(failures) - 1:
                        print("   " + "-" * 60)
                
                if len(failures) > 5:
                    print(f"   ... and {len(failures) - 5} more failures in this category")
        
        # Summary recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        print("-" * 100)
        
        # Identify problematic categories
        problem_categories = [cat for cat, stats in summary['category_breakdown'].items() if stats['accuracy'] < 0.7]
        if problem_categories:
            print(f"🔧 Focus on improving these categories: {', '.join(problem_categories)}")
        
        # Identify problematic lexical items
        problem_items = [item for item, stats in summary['lexical_item_breakdown'].items() if stats['accuracy'] < 0.7]
        if problem_items:
            print(f"🔧 Focus on improving these lexical items: {', '.join(problem_items)}")
        
        if not problem_categories and not problem_items:
            print("🎉 All categories and lexical items performing well!")
        
        # CRITICAL ERROR ANALYSIS - Show first with maximum prominence
        if summary.get('critical_errors', 0) > 0:
            print("\n" + "🔥" * 100)
            print("🚨🚨🚨 CRITICAL SYSTEM ERROR DETAILED ANALYSIS 🚨🚨🚨")
            print("🔥" * 100)
            print("💥 These errors indicate serious system issues that prevent proper evaluation!")
            print("💥 Priority: FIX THESE FIRST before analyzing other results!")
            print("🔥" * 100)
            
            critical_cases = summary.get('critical_error_cases', [])
            critical_groups = {}
            
            # Group critical errors by type and lexical item
            for error_case in critical_cases:
                error_details = error_case.get('error_details', {})
                error_type = error_details.get('error_type', 'UnknownError')
                error_message = error_details.get('error_message', '')
                lexical_item = error_details.get('lexical_item', 'unknown')
                
                # Create more specific grouping for critical errors
                if 'json' in error_message.lower() or 'parse' in error_message.lower():
                    key = f"{lexical_item}_JSON_PARSING_ERROR"
                elif 'timeout' in error_message.lower() or 'connection' in error_message.lower():
                    key = f"{lexical_item}_CONNECTION_ERROR"
                elif 'api' in error_message.lower() or 'rate' in error_message.lower():
                    key = f"{lexical_item}_API_ERROR"
                else:
                    key = f"{lexical_item}_{error_type}"
                
                if key not in critical_groups:
                    critical_groups[key] = []
                critical_groups[key].append(error_case)
            
            for group_key, errors in critical_groups.items():
                parts = group_key.split('_')
                lexical_item = parts[0]
                error_category = '_'.join(parts[1:])
                
                print(f"\n🔥 {lexical_item.upper()} - {error_category} ({len(errors)} occurrences)")
                print("=" * 80)
                
                for i, error in enumerate(errors[:2]):  # Show up to 2 per critical group
                    error_details = error.get('error_details', {})
                    print(f"\n   💥 Critical Error {i+1}:")
                    print(f"   📝 Input Text: {error_details.get('input_text', 'N/A')}")
                    print(f"   🏷️  Test Category: {error_details.get('category', 'unknown')}")
                    print(f"   🚨 Error Type: {error_details.get('error_type', 'UnknownError')}")
                    print(f"   💀 Full Error Message:")
                    print(f"      {error_details.get('error_message', 'No message')}")
                    
                    # Add specific recommendations based on error type
                    if 'json' in error_details.get('error_message', '').lower():
                        print(f"   🔧 RECOMMENDATION: Check LLM response format - likely malformed JSON output")
                    elif 'timeout' in error_details.get('error_message', '').lower():
                        print(f"   🔧 RECOMMENDATION: Check API connectivity and increase timeout settings")
                    elif 'rate' in error_details.get('error_message', '').lower():
                        print(f"   🔧 RECOMMENDATION: Implement rate limiting or check API quota")
                    
                    if i < len(errors) - 1:
                        print("   " + "─" * 70)
                
                if len(errors) > 2:
                    print(f"\n   ⚠️  ... and {len(errors) - 2} more {error_category} critical errors")
                    print(f"   💡 Consider fixing the pattern above to resolve all {len(errors)} cases")
            
            print("\n" + "🔥" * 100)
            print("🚨 END CRITICAL ERROR ANALYSIS - PLEASE ADDRESS THESE ISSUES IMMEDIATELY! 🚨")
            print("🔥" * 100)
        
        # Regular Execution Error Analysis
        if summary.get('execution_errors', 0) > 0 and summary.get('execution_errors', 0) > summary.get('critical_errors', 0):
            print(f"\n🚨 EXECUTION ERROR ANALYSIS ({summary['execution_errors']} total errors):")
            print("=" * 100)
            
            error_cases = summary.get('execution_error_cases', [])
            error_groups = {}
            
            # Group errors by type and lexical item
            for error_case in error_cases:
                error_details = error_case.get('error_details', {})
                error_type = error_details.get('error_type', 'UnknownError')
                lexical_item = error_details.get('lexical_item', 'unknown')
                key = f"{lexical_item}_{error_type}"
                
                if key not in error_groups:
                    error_groups[key] = []
                error_groups[key].append(error_case)
            
            for group_key, errors in error_groups.items():
                lexical_item, error_type = group_key.split('_', 1)
                print(f"\n🔸 {lexical_item.upper()} - {error_type} ({len(errors)} occurrences):")
                
                for i, error in enumerate(errors[:3]):  # Show up to 3 per group
                    error_details = error.get('error_details', {})
                    print(f"\n   Error {i+1}:")
                    print(f"   📝 Input: {error_details.get('input_text', 'N/A')}")
                    print(f"   🏷️  Category: {error_details.get('category', 'unknown')}")
                    print(f"   🚨 Error Type: {error_details.get('error_type', 'UnknownError')}")
                    print(f"   💥 Error Message: {error_details.get('error_message', 'No message')}")
                    
                    if i < len(errors) - 1:
                        print("   " + "-" * 60)
                
                if len(errors) > 3:
                    print(f"   ... and {len(errors) - 3} more {error_type} errors")
        
        # Final Summary Statistics
        successful_runs = summary['total_tests'] - summary.get('execution_errors', 0)
        success_rate = (successful_runs / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
        
        print(f"\n📊 FINAL EXECUTION SUMMARY:")
        print("-" * 100)
        print(f"✅ Successful Test Executions: {successful_runs}/{summary['total_tests']} ({success_rate:.1f}%)")
        print(f"❌ Failed Test Executions: {summary.get('execution_errors', 0)}/{summary['total_tests']}")
        if summary.get('critical_errors', 0) > 0:
            print(f"🔥 Critical System Errors: {summary['critical_errors']}/{summary['total_tests']} (NEEDS IMMEDIATE ATTENTION)")
        
        if not self.langfuse_client:
            print(f"\n📊 Running in LOCAL MODE - no data uploaded to Langfuse")
        else:
            print(f"\n🔗 Check your Langfuse dashboard for detailed dataset run results")
        
        print("="*100)


async def main():
    """Run master dataset evaluation."""
    try:
        runner = MasterDatasetEvaluationRunner()
        
        # Run master dataset evaluation
        summary = await runner.run_master_dataset_evaluation()
        
        # Print results
        runner.print_master_summary(summary)
        
        # Determine exit code
        if summary['overall_accuracy'] >= 0.8:
            print("🎉 Master dataset evaluation completed successfully!")
            return 0
        else:
            print("🔧 Some tests failed - review results above")
            return 1
            
    except Exception as e:
        print(f"❌ Error running master dataset evaluation: {e}")
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))