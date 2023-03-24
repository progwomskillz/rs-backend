from .base_repository import BaseRepository


class PollsRepository(BaseRepository):
    def __init__(
        self, scheme, username, password, host, port, db_name, collection_name,
        translator, stats_translator
    ):
        family_tag_search_pipeline = self.__generate_tag_search_pipeline(
            "family", 25, "lt"
        )
        health_tag_search_pipeline = self.__generate_tag_search_pipeline(
            "health", 18, "gt"
        )
        self.calc_summary_pipeline = [
            {
                "$addFields": {
                    "summary": {
                        "$reduce": {
                            "input": "$feedbacks", 
                            "initialValue": {
                                "family": {
                                    "count": 0
                                }, 
                                "health": {
                                    "count": 0
                                }, 
                                "unknown": {
                                    "count": 0
                                }
                            }, 
                            "in": {
                                "family": {
                                    "count": {
                                        "$add": [
                                            "$$value.family.count", {
                                                "$cond": [
                                                    family_tag_search_pipeline,
                                                    1,
                                                    0
                                                ]
                                            }
                                        ]
                                    }
                                }, 
                                "health": {
                                    "count": {
                                        "$add": [
                                            "$$value.health.count", {
                                                "$cond": [
                                                    health_tag_search_pipeline,
                                                    1,
                                                    0
                                                ]
                                            }
                                        ]
                                    }
                                }, 
                                "unknown": {
                                    "count": {
                                        "$add": [
                                            "$$value.unknown.count", {
                                                "$cond": [
                                                    {
                                                        "$or": [
                                                            family_tag_search_pipeline,
                                                            health_tag_search_pipeline
                                                        ]
                                                    },
                                                    0,
                                                    1
                                                ]
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "summary": {
                        "$objectToArray": "$summary"
                    }
                }
            },
            {
                "$addFields": {
                    "summary": {
                        "$map": {
                            "input": "$summary", 
                            "as": "stats", 
                            "in": {
                                "title": "$$stats.k", 
                                "count": "$$stats.v.count", 
                                "percentage": {
                                    "$multiply": [
                                        100,
                                        {
                                            "$divide": [
                                                "$$stats.v.count",
                                                {
                                                    "$size": "$feedbacks"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        ]
        default_pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": {
                    "path": "$user"
                }
            },
            *self.calc_summary_pipeline
        ]
        super().__init__(
            scheme, username, password, host, port, db_name, collection_name,
            translator, default_pipeline
        )
        self.stats_translator = stats_translator

    def get_page(self, user_id, page, page_size):
        pipeline = []
        if user_id:
            pipeline.append(
                {"$match": {"user._id": self._to_object_id(user_id)}}
            )
        return self._get_page(pipeline, page, page_size)

    def get_summary(self):
        cursor = list(self.collection.aggregate([
            {
                "$unwind": {
                    "path": "$feedbacks"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "feedbacks": {
                        "$push": "$feedbacks"
                    }
                }
            },
            *self.calc_summary_pipeline
        ]))
        if not cursor:
            return []
        return [
            self.stats_translator.from_document(stats)
            for stats in cursor[0].get("summary", [])
        ]

    def __generate_tag_search_pipeline(self, tag, age, age_cond):
        return {
            "$and": [
                {
                    "$regexFind": {
                        "input": "$$this.bothers", 
                        "regex": f"{tag}", 
                        "options": "i"
                    }
                },
                {f"${age_cond}": ["$$this.age", age]}
            ]
        }
