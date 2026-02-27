import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.services.conversation_service import ConversationService


class ConversationServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_add_message_rejects_invalid_role(self):
        conversation = ConversationService.create_conversation(self.db)

        with self.assertRaises(ValueError):
            ConversationService.add_message(self.db, conversation, "system", "invalid role content")

    def test_add_first_user_message_sets_title(self):
        conversation = ConversationService.create_conversation(self.db)

        ConversationService.add_message(self.db, conversation, "user", "What is an iron condor?")
        reloaded = ConversationService.get_conversation(self.db, conversation.id)

        self.assertEqual(reloaded.title, "What is an iron condor?")

