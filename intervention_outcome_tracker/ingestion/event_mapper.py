class EventMapper:
    def by_user_id(self, records):
        return {record["user_id"]: record for record in records}
