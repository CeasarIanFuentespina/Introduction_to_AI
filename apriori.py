
"""
Apriori Algorithm
=================
The Apriori algorithm is used for association rule mining in transaction databases.
"""

from collections import defaultdict
from itertools import combinations


def get_support(itemset, transactions):
    """Calculate support for an itemset."""
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)


def generate_candidates(frequent_itemsets, k):
    """Generate candidate k-itemsets from frequent (k-1)-itemsets."""
    candidates = []
    n = len(frequent_itemsets)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Union of two itemsets
            union = frequent_itemsets[i] | frequent_itemsets[j]
            
            if len(union) == k:
                # Check if all (k-1) subsets are frequent
                valid = True
                for item in union:
                    subset = union - {item}
                    if subset not in frequent_itemsets:
                        valid = False
                        break
                
                if valid and union not in candidates:
                    candidates.append(union)
    
    return candidates


def apriori(transactions, min_support):
    """Run Apriori algorithm."""
    n = len(transactions)
    min_count = int(min_support * n)
    
    # Get all unique items
    all_items = set()
    for t in transactions:
        all_items.update(t)
    
    # Find frequent 1-itemsets
    item_counts = defaultdict(int)
    for t in transactions:
        for item in t:
            item_counts[item] += 1
    
    frequent = []
    current = [frozenset([item]) for item, count in item_counts.items() if count >= min_count]
    frequent.extend(current)
    
    k = 2
    while current:
        # Generate candidates
        candidates = generate_candidates([set(fs) for fs in current], k)
        
        if not candidates:
            break
        
        # Count support
        counts = defaultdict(int)
        for t in transactions:
            for c in candidates:
                if c.issubset(t):
                    counts[frozenset(c)] += 1
        
        # Keep frequent
        current = [fs for fs, count in counts.items() if count >= min_count]
        frequent.extend(current)
        
        k += 1
    
    return [set(fs) for fs in frequent]


# ==================== EXAMPLE 1: Grocery Store ====================
print("=" * 60)
print("EXAMPLE 1: Grocery Store Transactions")
print("=" * 60)

transactions1 = [
    {'milk', 'bread', 'eggs'},
    {'bread', 'butter'},
    {'milk', 'bread', 'butter', 'eggs'},
    {'bread', 'eggs'},
    {'milk', 'eggs'}
]

print(f"\nTransaction Database: {len(transactions1)} transactions")
for i, t in enumerate(transactions1):
    print(f"  T{i+1}: {set(t)}")

min_support1 = 0.4
print(f"\nMinimum Support: {min_support1} ({int(min_support1 * len(transactions1))} transactions)")

frequent_itemsets1 = apriori(transactions1, min_support1)

print(f"\nFrequent Itemsets ({len(frequent_itemsets1)} found):")
for itemset in sorted(frequent_itemsets1, key=lambda x: (len(x), sorted(x))):
    support = get_support(itemset, transactions1)
    print(f"  {set(itemset)}: support = {support:.2f}")

print("\n" + "=" * 60)
print("EXAMPLE 2: Online Shopping Cart")
print("=" * 60)

transactions2 = [
    {'laptop', 'mouse', 'keyboard'},
    {'laptop', 'mouse'},
    {'laptop', 'keyboard', 'monitor'},
    {'mouse', 'keyboard', 'USB'},
    {'laptop', 'monitor', 'keyboard'},
    {'laptop', 'mouse', 'keyboard', 'USB'},
    {'monitor', 'USB'},
    {'laptop', 'keyboard'}
]

print(f"\nTransaction Database: {len(transactions2)} transactions")
for i, t in enumerate(transactions2):
    print(f"  T{i+1}: {set(t)}")

min_support2 = 0.375
print(f"\nMinimum Support: {min_support2} ({int(min_support2 * len(transactions2))} transactions)")

frequent_itemsets2 = apriori(transactions2, min_support2)

print(f"\nFrequent Itemsets ({len(frequent_itemsets2)} found):")
for itemset in sorted(frequent_itemsets2, key=lambda x: (len(x), sorted(x))):
    support = get_support(itemset, transactions2)
    print(f"  {set(itemset)}: support = {support:.2f}")

print("\n" + "=" * 60)
print("APRORI ALGORITHM EXAMPLES COMPLETE")
print("=" * 60)

