class Constants():
    @property
    def pipelines(self):
        return Pipelines()


class Pipelines():
    @property
    def users(self):
        return UsersPipelines()

    @property
    def polls(self):
        return PollsPipelines()

    @property
    def revise_requests(self):
        return ReviseRequestsPipelines()


class UsersPipelines():
    @property
    def default(self):
        return []


class PollsPipelines():
    @property
    def default(self):
        return [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user",
                    "pipeline": constants.pipelines.users.default
                }
            },
            {
                "$unwind": {
                    "path": "$user"
                }
            },
            *self.calc_summary
        ]

    @property
    def calc_summary(self):
        def generate_tag_search_pipeline(tag, age, age_cond):
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
        family_tag_search_pipeline = generate_tag_search_pipeline(
            "family", 25, "lt"
        )
        health_tag_search_pipeline = generate_tag_search_pipeline(
            "health", 18, "gt"
        )
        return [
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


class ReviseRequestsPipelines():
    @property
    def default(self):
        return [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user",
                    "pipeline": constants.pipelines.users.default
                }
            },
            {
                "$unwind": {
                    "path": "$user"
                }
            },
            {
                "$lookup": {
                    "from": "polls",
                    "localField": "poll_id",
                    "foreignField": "_id",
                    "as": "poll",
                    "pipeline": constants.pipelines.polls.default
                }
            },
            {
                "$unwind": {
                    "path": "$poll"
                }
            }
        ]


constants = Constants()
