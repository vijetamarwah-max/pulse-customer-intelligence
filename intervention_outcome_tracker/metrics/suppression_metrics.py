class SuppressionMetrics:
    def total_suppressed(self, records):
        return len(
            [
                record
                for record in records
                if record["recommendation"] == "suppress"
                and record.get("group") == "PULSE"
            ]
        )
