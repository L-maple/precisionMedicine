
def get_body(disease, disease_boost, gene, gene_boost, gender, gender_boost, age, age_boost):
    clinical_body = {
        "query": {
            "bool": {
                "should": [
                {
                    "match": {
                        "content": {
                            "query": disease,
                            "boost": disease_boost
                        }
                    }
                },
                {
                    "match": {
                        "content": {
                            "query": gene,
                            "boost": gene_boost
                        }
                    }
                },
                {
                    "bool": {
                        "should": [
                        {
                            "match": {
                                "gender": {
                                    "query": gender,
                                    "boost": gender_boost
                                }
                            }
                        },
                        {
                            "match": {
                                "gender": {
                                    "query": "all",
                                    "boost": gender_boost
                                }
                            }
                        }
                        ]
                    }
                },
                {
                    "bool": {
                        "must": [
                        {
                            "range": {
                                "min_age": {
                                    "lte": age,
                                    "boost": age_boost
                                }
                            }
                        },
                        {
                            "range": {
                                "max_age": {
                                    "gte": age,
                                    "boost": age_boost
                                }
                            }
                        }
                        ]
                    }
                }
                ]
            }
        }
    }
    return clinical_body




