import aiosqlite

DB = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            ip TEXT,
            port INTEGER,
            token TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            server_id INTEGER,
            type TEXT,
            message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        await db.commit()
        


