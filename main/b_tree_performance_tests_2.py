import random
import source_data.load_file as load_file

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
#            'total_visits_exact_first': test_total_visits
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
#            'total_visits_exact_all': test_total_visits,
#            'total_matches_exact_all': total_matches,
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
            'avg_visits_exact_opt': avg_visits,
#            'total_visits_exact_opt': test_total_visits
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
#            'total_visits_range': total_visits,
            'avg_keys_per_range': avg_results,
#            'total_keys_found_range': total_results
        }

    def test_find_all_merchant_ids(self):
        if 'Merchant ID' not in self.b_tree.name:
            print('[SKIP] Tree does not use Merchant ID as a key.')
            return {}
        print(f'\n[Test] Find All Records for All Merchant IDs')
        merchant_ids = load_file.unique_values.get_merchant_id()
        total_visits = 0
        total_results = 0
        for merchant_id in merchant_ids:
            self.b_tree.reset_visit_counts()
            matches = [x for x in self.b_tree.inorder_traverse() if str(x) == str(merchant_id)]
            visit_count = self.b_tree.get_total_visits()
            total_visits += visit_count
            total_results += len(matches)
            print(f'Merchant ID {merchant_id}: {len(matches)} matches, {visit_count} visits')
        avg_visits = total_visits / len(merchant_ids)
        avg_results = total_results / len(merchant_ids)
        print(f'Average matches per Merchant ID: {avg_results:.1f}')
        print(f'Average node visits per Merchant ID: {avg_visits:.1f}')
        return {
            'avg_visits_merchant_id': avg_visits,
#            'total_visits_merchant_id': total_visits,
#            'total_matches_merchant_id': total_results,
            'avg_keys_merchant_id': avg_results
        }

    def test_find_all_category_ids(self):
        if 'Category ID' not in self.b_tree.name:
            print('[SKIP] Tree does not use Category ID as a key.')
            return {}
        print(f'\n[Test] Find All Records for All Category IDs')
        category_ids = load_file.unique_values.get_category_id()
        total_visits = 0
        total_results = 0
        for category_id in category_ids:
            self.b_tree.reset_visit_counts()
            matches = [x for x in self.b_tree.inorder_traverse() if str(x) == str(category_id)]
            visit_count = self.b_tree.get_total_visits()
            total_visits += visit_count
            total_results += len(matches)
            print(f'Category ID {category_id}: {len(matches)} matches, {visit_count} visits')
        avg_visits = total_visits / len(category_ids)
        avg_results = total_results / len(category_ids)
        print(f'Average matches per Category ID: {avg_results:.1f}')
        print(f'Average node visits per Category ID: {avg_visits:.1f}')
        return {
            'avg_visits_category_id': avg_visits,
#            'total_visits_category_id': total_visits,
#            'total_matches_category_id': total_results,
            'avg_keys_category_id': avg_results
        }

    def test_find_all_random_cluster_ids(self, num_samples=20):
        if 'Cluster ID' not in self.b_tree.name:
            print('[SKIP] Tree does not use Cluster ID as a key.')
            return {}
        print(f'\n[Test] Find All Records for {num_samples} Random Cluster IDs')
        all_ids = load_file.unique_values.get_cluster_id()
        cluster_ids = random.sample(all_ids, k=min(num_samples, len(all_ids)))
        total_visits = 0
        total_results = 0
        for cluster_id in cluster_ids:
            self.b_tree.reset_visit_counts()
            matches = [x for x in self.b_tree.inorder_traverse() if str(x) == str(cluster_id)]
            visit_count = self.b_tree.get_total_visits()
            total_visits += visit_count
            total_results += len(matches)
            print(f'Cluster ID {cluster_id}: {len(matches)} matches, {visit_count} visits')
        avg_visits = total_visits / len(cluster_ids)
        avg_results = total_results / len(cluster_ids)
        print(f'Average matches per Cluster ID: {avg_results:.1f}')
        print(f'Average node visits per Cluster ID: {avg_visits:.1f}')
        return {
            'avg_visits_cluster_id': avg_visits,
#            'total_visits_cluster_id': total_visits,
#            'total_matches_cluster_id': total_results,
            'avg_keys_cluster_id': avg_results
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
        results.update(self.test_exact_search_optimized())
        results.update(self.test_range_search())
        results.update(self.test_find_all_merchant_ids())
        results.update(self.test_find_all_category_ids())
        results.update(self.test_find_all_random_cluster_ids(num_samples=20))

        return results
