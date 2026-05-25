class ElasticClient:

    def filter_reviews(self, reviews, dish):
        filtered = []

        for r in reviews:
            if dish in r["text"].lower():
                filtered.append(r)

        return filtered