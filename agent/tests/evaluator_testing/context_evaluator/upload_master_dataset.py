#!/usr/bin/env python3
"""
Upload a single master dataset combining all lexical items to Langfuse.
Creates one comprehensive dataset instead of separate datasets per lexical item.
"""

import json
import os
import asyncio
from typing import List, Dict, Any
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env.local")

from langfuse import Langfuse


class MasterDatasetUploader:
    """Upload all lexical items into a single master dataset on Langfuse."""
    
    def __init__(self, delay_between_requests: float = 0.1):
        # Check for Langfuse credentials
        required_vars = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {missing_vars}")
            raise ValueError(f"Missing Langfuse credentials: {missing_vars}")
        
        # Initialize Langfuse client
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        )
        
        self.delay = delay_between_requests
        print(f"✅ Connected to Langfuse (rate limit delay: {delay_between_requests}s)")

    def load_all_test_cases(self) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Load all test cases from the single combined JSON file."""
        filename = "all_lexical_items_comprehensive_test_cases.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Combined dataset file not found: {filename}. Please run generate_all_lexical_items_dataset.py first.")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📁 Loaded combined dataset with {data['total_cases']} test cases")
        
        # Extract test cases and add enhanced metadata for Langfuse
        all_test_cases = []
        for test_case in data["test_cases"]:
            lexical_item = test_case["metadata"]["lexical_item"]
            # Convert uppercase lexical_item to lowercase with spaces to match JSON keys
            lexical_item_key = lexical_item.lower()
            lexical_item_data = data["lexical_items"][lexical_item_key]
            
            enhanced_case = {
                "input": test_case["input"],
                "expected_output": test_case["expected_output"],
                "metadata": {
                    **test_case["metadata"],
                    "source_dataset": lexical_item.replace(' ', '_').lower(),
                    "evaluator": "ContextEvaluator",
                    "scenario_character": lexical_item_data["scenario_info"]["character"],
                    "scenario_role": lexical_item_data["scenario_info"]["role"],
                    "lexical_item_definition": lexical_item_data["scenario_info"]["definition"]
                }
            }
            all_test_cases.append(enhanced_case)
        
        # Build combined metadata from the loaded data
        combined_metadata = {
            "lexical_items": [],
            "total_cases_by_item": {},
            "category_breakdown": data["category_breakdown"],
            "difficulty_breakdown": data["difficulty_breakdown"]
        }
        
        # Extract lexical items info
        for lexical_item, item_data in data["lexical_items"].items():
            combined_metadata["lexical_items"].append({
                "lexical_item": lexical_item,
                "definition": item_data["scenario_info"]["definition"],
                "character": item_data["scenario_info"]["character"], 
                "role": item_data["scenario_info"]["role"],
                "cases": item_data["total_cases"]
            })
            combined_metadata["total_cases_by_item"][lexical_item] = item_data["total_cases"]
            print(f"📁 {item_data['total_cases']} test cases for {lexical_item.upper()}")
        
        print(f"🎯 Total: {len(all_test_cases)} test cases across {len(combined_metadata['lexical_items'])} lexical items")
        return all_test_cases, combined_metadata

    async def create_master_dataset(self, combined_metadata: Dict[str, Any]) -> str:
        """Create the master dataset in Langfuse."""
        dataset_name = "context-evaluator-master-comprehensive"
        
        # Create comprehensive description
        lexical_items_str = ", ".join([item["lexical_item"].upper() for item in combined_metadata["lexical_items"]])
        total_cases = sum(combined_metadata["total_cases_by_item"].values())
        
        description = f"""ContextEvaluator Master Comprehensive Dataset

This dataset combines test cases for all lexical items: {lexical_items_str}

📊 Dataset Statistics:
• Total test cases: {total_cases}
• Lexical items: {len(combined_metadata['lexical_items'])}
• Categories: {list(combined_metadata['category_breakdown'].keys())}
• Difficulty levels: {list(combined_metadata['difficulty_breakdown'].keys())}

📋 Test Case Breakdown by Lexical Item:"""

        for item_info in combined_metadata["lexical_items"]:
            description += f"""
• {item_info['lexical_item'].upper()}: {item_info['cases']} cases
  - Definition: {item_info['definition']}
  - Character: {item_info['character']} ({item_info['role']})"""

        description += f"""

📋 Category Distribution:"""
        for category, count in combined_metadata["category_breakdown"].items():
            description += f"""
• {category}: {count} cases"""

        description += """

🎯 Purpose: Comprehensive evaluation of ContextEvaluator across multiple lexical items
🔧 Generated for: Multi-lexical-item accuracy testing with expected feedback evaluation
📅 Created: 2025-08-29"""

        try:
            dataset = await asyncio.to_thread(
                self.langfuse.create_dataset,
                name=dataset_name,
                description=description.strip()
            )
            print(f"✅ Created master dataset: {dataset_name}")
            return dataset_name
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"⚠️  Master dataset already exists: {dataset_name}")
                return dataset_name
            else:
                raise

    async def upload_single_case_async(self, dataset_name: str, test_case: Dict[str, Any], 
                                      case_index: int, max_retries: int = 5) -> bool:
        """Upload a single test case with improved retry logic asynchronously."""
        
        for attempt in range(max_retries):
            try:
                # Run the synchronous Langfuse call in a thread
                await asyncio.to_thread(
                    self.langfuse.create_dataset_item,
                    dataset_name=dataset_name,
                    input=test_case["input"],
                    expected_output=test_case["expected_output"],
                    metadata=test_case["metadata"]
                )
                if attempt > 0:  # Log successful retry
                    print(f"✅ Case {case_index+1} uploaded successfully on attempt {attempt+1}")
                return True
                
            except Exception as e:
                error_str = str(e).lower()
                # Print detailed error information
                print(f"🚨 Error on case {case_index+1} (attempt {attempt+1}): {e}")
                
                # Standard exponential backoff for all retryable errors
                if any(code in error_str for code in ["429", "503", "502", "500", "timeout"]) and attempt < max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s, 8s, 16s (with jitter)
                    base_wait = 2 ** attempt
                    jitter = base_wait * 0.1 * (0.5 - __import__('random').random())  # ±10% jitter
                    wait_time = min(base_wait + jitter, 60)  # Cap at 60 seconds
                    
                    error_type = "Rate limit" if "429" in error_str else "Server error"
                    print(f"⏱️  {error_type} on case {case_index+1} (attempt {attempt+1}), waiting {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)
                    continue
                elif attempt == max_retries - 1:
                    print(f"❌ Failed to upload case {case_index+1} after {max_retries} attempts:")
                    print(f"   Full error: {e}")
                    print(f"   Error type: {type(e).__name__}")
                    return False
                else:
                    # For other non-retryable errors, minimal wait and retry
                    print(f"   Non-retryable error, retrying in 0.5 seconds...")
                    await asyncio.sleep(0.5)
                    continue
        
        return False

    async def upload_all_cases_async(self, dataset_name: str, test_cases: List[Dict[str, Any]]) -> int:
        """Upload all test cases using optimal batching strategy: 100 requests/minute in batches of 5."""
        
        print(f"🚀 Uploading {len(test_cases)} test cases to master dataset...")
        print(f"⚡ Using optimal batching: 100 requests/minute in batches of 5 parallel uploads")
        
        uploaded_count = 0
        failed_cases = []
        batch_size = 5
        requests_per_minute = 100
        
        # Process in batches of 5, with 100 requests per minute limit
        for batch_start in range(0, len(test_cases), batch_size):
            batch_end = min(batch_start + batch_size, len(test_cases))
            batch = test_cases[batch_start:batch_end]
            
            # Create semaphore for this batch
            semaphore = asyncio.Semaphore(batch_size)
            
            async def upload_with_semaphore(i: int, test_case: Dict[str, Any]) -> bool:
                async with semaphore:
                    return await self.upload_single_case_async(dataset_name, test_case, batch_start + i)
            
            # Upload this batch in parallel
            batch_tasks = [
                upload_with_semaphore(i, test_case) 
                for i, test_case in enumerate(batch)
            ]
            
            batch_results = await asyncio.gather(*batch_tasks)
            
            # Count results
            batch_successes = sum(1 for result in batch_results if result)
            uploaded_count += batch_successes
            
            for i, success in enumerate(batch_results):
                if not success:
                    failed_cases.append(batch_start + i + 1)
            
            # Progress update
            print(f"📊 Progress: {batch_end}/{len(test_cases)} cases processed ({uploaded_count} successful)")
            
            # Check if we need to wait for rate limit reset
            requests_made = batch_end
            if requests_made % requests_per_minute == 0 and batch_end < len(test_cases):
                print(f"⏱️  Completed {requests_made} requests. Waiting 60 seconds for rate limit reset...")
                await asyncio.sleep(60)
            elif batch_end < len(test_cases):
                # Small delay between batches to avoid overwhelming the server
                await asyncio.sleep(0.1)
        
        failed_count = len(test_cases) - uploaded_count
        
        print(f"🎉 Master dataset upload complete: {uploaded_count}/{len(test_cases)} cases uploaded")
        if failed_count > 0:
            print(f"⚠️  {failed_count} cases failed to upload: {failed_cases[:10]}" + 
                  (f" (and {len(failed_cases) - 10} more)" if len(failed_cases) > 10 else ""))
            
        return uploaded_count

    async def upload_master_dataset_async(self) -> Dict[str, Any]:
        """Upload the complete master dataset."""
        print("🚀 Creating master dataset combining all lexical items...")
        
        # Load all test cases
        test_cases, combined_metadata = self.load_all_test_cases()
        
        if not test_cases:
            raise FileNotFoundError("No test cases found. Please generate datasets first.")
        
        # Create master dataset
        dataset_name = await self.create_master_dataset(combined_metadata)
        await asyncio.sleep(self.delay)
        
        # Upload all test cases
        uploaded_count = await self.upload_all_cases_async(dataset_name, test_cases)
        
        return {
            "dataset_name": dataset_name,
            "total_cases": len(test_cases),
            "uploaded_cases": uploaded_count,
            "lexical_items": [item["lexical_item"] for item in combined_metadata["lexical_items"]],
            "metadata": combined_metadata
        }

    def upload_master_dataset(self) -> Dict[str, Any]:
        """Upload master dataset (sync wrapper)."""
        return asyncio.run(self.upload_master_dataset_async())


async def main():
    """Upload master dataset combining all lexical items."""
    try:
        uploader = MasterDatasetUploader(delay_between_requests=0.5)
        
        # Upload master dataset
        result = await uploader.upload_master_dataset_async()
        
        print(f"\n📊 MASTER DATASET UPLOAD SUMMARY")
        print("="*60)
        print(f"📋 Dataset Name: {result['dataset_name']}")
        print(f"📈 Total Cases: {result['uploaded_cases']}/{result['total_cases']}")
        print(f"🎯 Lexical Items: {', '.join([item.upper() for item in result['lexical_items']])}")
        
        # Show breakdown by lexical item
        print(f"\n📋 Cases by Lexical Item:")
        for item_info in result["metadata"]["lexical_items"]:
            print(f"   {item_info['lexical_item'].upper():12} {item_info['cases']} cases")
        
        # Show category breakdown
        print(f"\n📋 Cases by Category:")
        for category, count in result["metadata"]["category_breakdown"].items():
            print(f"   {category:15} {count} cases")
        
        if result['uploaded_cases'] >= result['total_cases'] * 0.9:  # 90% success rate
            print(f"\n🎉 Master dataset upload successful!")
            print(f"✅ Ready for comprehensive evaluation across all lexical items")
            return 0
        else:
            print(f"\n⚠️  Partial upload. Check rate limits and retry if needed.")
            return 1
        
    except Exception as e:
        print(f"❌ Error uploading master dataset: {e}")
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))