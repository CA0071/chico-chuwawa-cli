"""
Persistent chat history using SQLite
Stores and retrieves conversation history
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import os


class ChatHistory:
    """Manage persistent chat history"""
    
    def __init__(self):
        # Use same config directory as API config
        if os.name == 'nt':
            config_dir = Path(os.environ.get('APPDATA', '')) / 'ChicoChuwawa-CLI'
        else:
            config_dir = Path.home() / '.config' / 'chico-cli'
        
        config_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = config_dir / 'chat_history.db'
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title TEXT,
                provider TEXT,
                model TEXT
            )
        ''')
        
        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        # Create builder markers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS markers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                marker_type TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_session(self, provider: str, model: str, title: Optional[str] = None) -> int:
        """
        Create a new chat session
        
        Returns:
            Session ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if not title:
            title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        cursor.execute(
            'INSERT INTO sessions (title, provider, model) VALUES (?, ?, ?)',
            (title, provider, model)
        )
        session_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return session_id
    
    def add_message(self, session_id: int, role: str, content: str):
        """Add a message to a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
            (session_id, role, content)
        )
        
        conn.commit()
        conn.close()
    
    def get_session_messages(self, session_id: int) -> List[Dict]:
        """Get all messages for a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY timestamp',
            (session_id,)
        )
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'role': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return messages
    
    def list_sessions(self, limit: int = 10) -> List[Dict]:
        """List recent sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id, title, provider, model, created_at FROM sessions ORDER BY created_at DESC LIMIT ?',
            (limit,)
        )
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'id': row[0],
                'title': row[1],
                'provider': row[2],
                'model': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        return sessions
    
    def add_marker(self, session_id: int, marker_type: str, content: str):
        """Add a builder marker to a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO markers (session_id, marker_type, content) VALUES (?, ?, ?)',
            (session_id, marker_type, content)
        )
        
        conn.commit()
        conn.close()
    
    def get_session_markers(self, session_id: int) -> List[Dict]:
        """Get all markers for a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT marker_type, content, timestamp FROM markers WHERE session_id = ? ORDER BY timestamp',
            (session_id,)
        )
        
        markers = []
        for row in cursor.fetchall():
            markers.append({
                'type': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return markers
    
    def delete_session(self, session_id: int):
        """Delete a session and all its messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
        cursor.execute('DELETE FROM markers WHERE session_id = ?', (session_id,))
        cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
        
        conn.commit()
        conn.close()
    
    def search_messages(self, query: str, limit: int = 20) -> List[Dict]:
        """Search messages by content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.session_id, s.title, m.role, m.content, m.timestamp
            FROM messages m
            JOIN sessions s ON m.session_id = s.id
            WHERE m.content LIKE ?
            ORDER BY m.timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'session_id': row[0],
                'session_title': row[1],
                'role': row[2],
                'content': row[3],
                'timestamp': row[4]
            })
        
        conn.close()
        return results
