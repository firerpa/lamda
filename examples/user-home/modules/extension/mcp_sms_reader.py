# Copyright 2025 rev1si0n (lamda.devel@gmail.com). All rights reserved.
#
# Distributed under MIT license.
# See file LICENSE for detail or copy at https://opensource.org/licenses/MIT
#
# ===================================================================
# MCP for reading local SMS messages. 用于读取本机短信的 MCP 扩展
# ===================================================================
#
import json
import sqlite3
from lamda.mcp import mcp, Annotated, TextContent
from lamda.extensions import BaseMcpExtension

db_path = "/data/data/com.android.providers.telephony/databases/mmssms.db"

class SmsMcpExtension(BaseMcpExtension):
    route = "/sms/mcp/"
    name = "sms-reader-extension"
    version = "1.0"
    @mcp("tool", description="""Reads the SMS database using SQL statements in SQLite syntax; read-only, no write operations allowed.
    The database is standard android mmssms.db, you should always learn the tables or table structure if needed.""")
    def read_sms_database_by_sql(self, ctx, sql: Annotated[str, "A raw SQL (SQLite) query string for read-only operations."]):
        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA query_only")
        try:
            items = db.execute(sql)
            results = json.dumps([dict(row) for row in items.fetchall()])
        finally:
            db.close()
        return TextContent(text=results)