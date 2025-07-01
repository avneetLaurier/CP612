import random

class BTreePerformanceTests:
    # Constants for number of test cycles
    EXACT_SEARCH_TESTS = 10
    RANGE_SEARCH_TESTS = 10
    RANGE_SEARCH_WIDTH = 20
    
    def __init__(self, b_tree, key_list):
        self.b_tree = b_tree
        self.key_list = sorted(key_list)

    def test_exact_search_first_match(self):
        test_count = self.EXACT_SEARCH_TESTS
        print(f'\n[Test] Exact Search – First Match Only ({test_count} random keys)')  
        self.b_tree.reset_visit_counts()
        test_keys = random.choices(self.key_list, k=test_count)
        for key in test_keys:
            self.b_tree.search(key)
        test_total_visits = self.b_tree.get_total_visits()
        avg_visits = test_total_visits / test_count
        print(f'Total node visits: {test_total_visits}')
        print(f'Average node visits per search: {avg_visits:.1f}')
        return {
            'avg_visits_exact_first': avg_visits,
            'total_visits_exact_first': test_total_visits
        }

    def test_exact_search_all_matches(self):
        test_count = self.EXACT_SEARCH_TESTS
        print(f'\n[Test] Exact Search – All Matches ({test_count} random keys)')  
        self.b_tree.reset_visit_counts()
        test_keys = random.choices(self.key_list, k=test_count)
        total_matches = 0
        for key in test_keys:
            matches = [x for x in self.b_tree.inorder_traverse() if x == key]
            total_matches += len(matches)
        test_total_visits = self.b_tree.get_total_visits()
        avg_matches = total_matches / test_count
        avg_visits = test_total_visits / test_count
        print(f'Total node visits: {test_total_visits}')
        print(f'Total matches found: {total_matches}')
        print(f'Average matches per search: {avg_matches:.1f}')
        print(f'Average node visits per search: {avg_visits:.1f}')
        return {
            'avg_visits_exact_all': avg_visits,
            'total_visits_exact_all': test_total_visits,
            'total_matches_exact_all': total_matches,
            'avg_matches_exact_all': avg_matches
        }

    def test_exact_search_optimized(self):
        test_count = self.EXACT_SEARCH_TESTS
        print(f'\n[Test] Exact Search – Optimized ({test_count} random keys)')
        self.b_tree.reset_visit_counts()
        test_keys = random.choices(self.key_list, k=test_count)
        for key in test_keys:
            self.b_tree.search_all_matches_sorted(key)
        test_total_visits = self.b_tree.get_total_visits()
        avg_visits = test_total_visits / test_count
        print(f'Total node visits (optimized): {test_total_visits}')
        print(f'Average node visits per search (optimized): {avg_visits:.1f}')
        return {
            'avg_visits_exact_first_opt': avg_visits,
            'total_visits_exact_first_opt': test_total_visits
        }

    def test_range_search(self):
        range_count = self.RANGE_SEARCH_TESTS
        range_width = self.RANGE_SEARCH_WIDTH
        print(f'\n[Test] Range Search – {range_count} random ranges of {range_width} keys')
        
        total_visits = 0
        total_results = 0

        for i in range(range_count):
            self.b_tree.reset_visit_counts()
            start_index = random.randint(0, len(self.key_list) - range_width - 1)
            key_min = self.key_list[start_index]
            key_max = self.key_list[start_index + range_width - 1]
            results = []
            for candidate in self.b_tree.inorder_traverse():
                if key_min <= candidate <= key_max:
                    results.append(candidate)
            visit_count = self.b_tree.get_total_visits()
            total_visits += visit_count
            total_results += len(results)
            print(f'Range {key_min} to {key_max}: {len(results)} matches, {visit_count} visits')

        avg_results = total_results / range_count
        avg_visits = total_visits / range_count
        print(f'Total keys found across all ranges: {total_results}')
        print(f'Average keys per range: {avg_results:.1f}')
        print(f'Average node visits per range: {avg_visits:.1f}')
        return {
            'avg_visits_range': avg_visits,
            'total_visits_range': total_visits,
            'avg_keys_per_range': avg_results,
            'total_keys_found_range': total_results
        }

    def test_all(self):
        print('\n--- Performance Test ---')
        print(f'Tree Name: {self.b_tree.name}')
        print(f'Min Degree (t): {self.b_tree.tree}')
        print(f'Sorted Input: {self.b_tree.sorted}')
        print(f'Height: {self.b_tree.get_height()}')
        print(f'Total Keys: {len(self.key_list)}')

        results = {
            'tree_name': self.b_tree.name,
            'min_deg': self.b_tree.tree,
            'sorted': self.b_tree.sorted,
            'height': self.b_tree.get_height(),
            'total_keys': len(self.key_list),
            'num_nodes': self.b_tree.node_count
        }

        results.update(self.test_exact_search_first_match())
        results.update(self.test_exact_search_all_matches())
        results.update(self.test_exact_search_optimized())  #added new search assumes sorted
        results.update(self.test_range_search())
        return results
