import os

class Migration:
    def __init__(self, db):
        self.db = db

    def make_migration(self, migration_name, script=None):
        if not os.path.exists('migrations'):
            os.makedirs('migrations')
        with open(f'migrations/{migration_name}.py', 'w') as file:
            if script:
                file.write(script)
            else:
                file.write(f"""
def migrate(db):
    # Add your migration logic here
    pass
                """)

    def apply_migrations(self):
        migration_files = sorted(os.listdir('migrations'))
        for migration in migration_files:
            if migration.endswith('.py'):
                module_name = f'migrations.{migration[:-3]}'
                migration_module = __import__(module_name, fromlist=['migrate'])
                if hasattr(migration_module, 'migrate'):
                    migration_module.migrate(self.db)