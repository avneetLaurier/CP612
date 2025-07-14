import random
import source_data.load_file as load_file

class BTreePerformanceTests:
    EXACT_SEARCH_TESTS = 100
    RANGE_SEARCH_TESTS = 100
    RANGE_SEARCH_WIDTH = 20
    VISIT_COST_UNIT = 5

    def __init__(self, b_tree, key_list):
        self.b_tree = b_tree
        self.key_list = sorted(key_list)

    def run_test(self, search_func, keys, description):
        print(f'\n[Test] {description} ({len(keys)} keys)')
        total_visits = 0
        total_comparisons = 0
        total_results = 0

        for key in keys:
            self.b_tree.reset_visit_counts()
            results = search_func(key)
            total_visits += self.b_tree.get_total_visits()
            total_comparisons += self.b_tree.get_total_comparisons()
            total_results += len(results)

        avg_visits = total_visits / len(keys)
        avg_comparisons = total_comparisons / len(keys)
        avg_results = total_results / len(keys)
        avg_cost = avg_comparisons + avg_visits * self.VISIT_COST_UNIT

        print(f'Total node visits: {total_visits}')
        print(f'Total comparisons: {total_comparisons}')
        print(f'Average node visits per search: {avg_visits:.1f}')
        print(f'Average comparisons per search: {avg_comparisons:.1f}')
        print(f'Average results per search: {avg_results:.1f}')
        print(f'Aggregate cost per search: {avg_cost:.1f}')

        return {
            f'{description.lower().replace(" ", "_")}_avg_visits': avg_visits,
            f'{description.lower().replace(" ", "_")}_avg_comparisons': avg_comparisons,
            f'{description.lower().replace(" ", "_")}_avg_results': avg_results,
            f'{description.lower().replace(" ", "_")}_avg_cost': avg_cost
        }

    def test_exact_search_first_match(self):
        test_keys = random.choices(self.key_list, k=self.EXACT_SEARCH_TESTS)
        return self.run_test(self._search_first_match, test_keys, "Exact Search First Match Only")

    def _search_first_match(self, key):
        result = self.b_tree.search_first_match(key)
        return [result] if result else []

    def test_exact_search_all_matches(self):
        test_keys = random.choices(self.key_list, k=self.EXACT_SEARCH_TESTS)
        return self.run_test(self._search_all_matches, test_keys, "Exact Search All Matches")

    def _search_all_matches(self, key):
        return self.b_tree.search_all_matches(key)

    def test_range_search(self):
        ranges = []
        for _ in range(self.RANGE_SEARCH_TESTS):
            start = random.randint(0, len(self.key_list) - self.RANGE_SEARCH_WIDTH - 1)
            ranges.append((self.key_list[start], self.key_list[start + self.RANGE_SEARCH_WIDTH - 1]))

        total_visits = 0
        total_comparisons = 0
        total_results = 0

        for min_key, max_key in ranges:
            self.b_tree.reset_visit_counts()
            results = self.b_tree.range_search(min_key, max_key)
            total_visits += self.b_tree.get_total_visits()
            total_comparisons += self.b_tree.get_total_comparisons()
            total_results += len(results)

            print(f'Range {min_key} to {max_key}: {len(results)} matches, {self.b_tree.get_total_visits()} visits, {self.b_tree.get_total_comparisons()} comparisons')

        avg_visits = total_visits / self.RANGE_SEARCH_TESTS
        avg_comparisons = total_comparisons / self.RANGE_SEARCH_TESTS
        avg_results = total_results / self.RANGE_SEARCH_TESTS
        avg_cost = avg_comparisons + avg_visits * self.VISIT_COST_UNIT

        print(f'Average keys per range: {avg_results:.1f}')
        print(f'Average node visits per range: {avg_visits:.1f}')
        print(f'Average comparisons per range: {avg_comparisons:.1f}')
        print(f'Aggregate cost per range: {avg_cost:.1f}')

        return {
            'range_search_avg_visits': avg_visits,
            'range_search_avg_comparisons': avg_comparisons,
            'range_search_avg_results': avg_results,
            'range_search_avg_cost': avg_cost
        }

    def test_composite_key_search(self):
        print('\n[Test] Composite Key Search')
        combined_results = {}
        composite_key = random.choice(self.key_list)
        parts = composite_key.split(' - ', 1)
        key_1_sample = parts[0]
        key_2_sample = parts[1] if len(parts) > 1 else ''

        def search_full(_): 
            return self.b_tree.search_composite(key_1=key_1_sample, key_2=key_2_sample)
        results_full = self.run_test(search_full, [None], "Composite Search Full Key")
        combined_results.update(results_full)

        def search_key1(_): 
            return self.b_tree.search_composite(key_1=key_1_sample)
        results_key1 = self.run_test(search_key1, [None], "Composite Search First Key")
        combined_results.update(results_key1)

        def search_key2(_): 
            return self.b_tree.search_composite(key_2=key_2_sample)
        results_key2 = self.run_test(search_key2, [None], "Composite Search Second Key")
        combined_results.update(results_key2)

        return combined_results




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
        results.update(self.test_range_search())

        return results
