class Journal:
    def __init__(self,journal_id,title):
        self.journal_id = journal_id
        self.title = title


class User:
    def __init__(self,user_id,name,role):
        self.user_id = user_id
        self.name = name
        self.role = role


class JournalAccess:
    def __init__(self,access_id,journal,user):
        self.access_id = access_id
        self.journal = journal
        self.user = user


class JournalAccessPortal:
    def __init__(self):
        self.journals = {}
        self.users = {}
        self.access_records = {}
        self.access_count = 1

    def add_journal(self,journal_id,title):
        if journal_id not in self.journals:
            self.journals[journal_id] = Journal(journal_id,title)

    def add_user(self,user_id,name,role):
        if user_id not in self.users:
            self.users[user_id] = User(user_id,name,role)

    def provide_journal_access(self,journal_id,user_id):
        if journal_id in self.journals and user_id in self.users:
            access = JournalAccess(self.access_count,self.journals[journal_id],self.users[user_id])
            self.access_records[self.access_count] = access
            self.access_count += 1
            return access
        else:
            if journal_id not in self.journals:
                raise ValueError("Journal ID does not exist.")
            if user_id not in self.users:
                raise ValueError("User ID does not exist.")

    def get_access_record(self,access_id):
        if access_id in self.access_records:
            return self.access_records[access_id]
        else:
            raise KeyError("Access Record not found")

    def remove_access_record(self,access_id):
        if access_id in self.access_records:
            del self.access_records[access_id]
        else:
            raise KeyError("Access Record not found")

    def monitor_access_usage(self,user_id):
        accesses_by_user = [access for access in self.access_records.values() if access.user.user_id == user_id]
        return accesses_by_user


# Unit Tests using the unittest framework
import unittest

class TestJournalAccessPortal(unittest.TestCase):
    def setUp(self):
        self.portal = JournalAccessPortal()
        self.portal.add_journal("j101","Journal of Python")
        self.portal.add_user("u101","Alice","Student")

    def test_journal_access(self):
        access = self.portal.provide_journal_access("j101","u101")
        self.assertIsNotNone(access)
        self.assertEqual(access.journal.title,"Journal of Python")

    def test_remove_access(self):
        access = self.portal.provide_journal_access("j101","u101")
        self.portal.remove_access_record(access.access_id)
        with self.assertRaises(KeyError):
            self.portal.get_access_record(access.access_id)

    def test_monitor_usage(self):
        self.portal.provide_journal_access("j101","u101")
        self.portal.provide_journal_access("j101","u101")
        monitor = self.portal.monitor_access_usage("u101")
        self.assertEqual(len(monitor),2)


if __name__ == '__main__':
    unittest.main()
