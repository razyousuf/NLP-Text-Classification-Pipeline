class SchemaConfig:
    def __init__(self, schema: dict):
        self.schema = schema

    def get_dataset_key(self, role: str) -> str:
        """Returns actual dataset key like 'raw_data' for role like 'raw'"""
        return self.schema["datasets"][role]

    def get_drop_columns(self, role: str) -> list:
        key = self.get_dataset_key(role)
        return self.schema.get("drop_columns", {}).get(key, [])

    def get_target_column(self, role: str) -> str:
        key = self.get_dataset_key(role)
        return self.schema.get("targets", {}).get(key, [None])[0]

    def get_all_roles(self) -> list:
        return list(self.schema.get("datasets", {}).keys())

    def get_column_groups(self, role: str) -> dict:
        key = self.get_dataset_key(role)
        return self.schema.get("column_groups", {}).get(key, {})