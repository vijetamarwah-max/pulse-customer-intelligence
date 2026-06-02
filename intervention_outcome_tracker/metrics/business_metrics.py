class BusinessMetrics:
    def incremental_revenue(self, records):
        return round(sum(record["incremental_value"] for record in records), 3)
