def rank_dishes(reviews):
    if not reviews:
        return 0

    return round(
        sum([r["rating"] for r in reviews]) / len(reviews), 2
    )