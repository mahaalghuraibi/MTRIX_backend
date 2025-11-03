from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from datetime import date

from ..models import Ticket, WorkLog, Reaction, Profile

User = get_user_model()

class MTRIXModelsTest(TestCase):
    def setUp(self):
    # ------------------------------------------------------------------------------------------------------------
        # Users & Profiles
        self.user = User.objects.create_user(username='mha', password='12345')
        self.profile = Profile.objects.create(user=self.user, role='Staff')

    # ------------------------------------------------------------------------------------------------------------
        # Tickets
        self.ticket1 = Ticket.objects.create(
            title='Broken AC',
            description='AC not cooling in Ward B',
            status='Open',
            user=self.user,
        )
        self.ticket2 = Ticket.objects.create(
            title='Printer Jam',
            description='Paper jam in Admin Office',
            status='InProgress',
            user=self.user,
        )

    # ------------------------------------------------------------------------------------------------------------
        # WorkLogs 
        self.wl1 = WorkLog.objects.create(
            date=date(2025, 1, 10), type='F', note='Replaced capacitor',
            technician_id=101, ticket=self.ticket1
        )
        self.wl2 = WorkLog.objects.create(
            date=date(2024, 12, 25), type='C', note='Checked filters',
            technician_id=101, ticket=self.ticket1
        )
        self.wl3 = WorkLog.objects.create(
            date=date(2024, 6, 1), type='R', note='Replaced belt',
            technician_id=102, ticket=self.ticket2
        )

    # ------------------------------------------------------------------------------------------------------------
        # Reactions
        self.reaction1 = Reaction.objects.create(ticket=self.ticket1, staff_id=201, score=2)
        self.reaction2 = Reaction.objects.create(ticket=self.ticket1, staff_id=202, score=3)
        self.reaction3 = Reaction.objects.create(ticket=self.ticket2, staff_id=203, score=1)

    # ------------------------------------------------------------------------------------------------------------
    # Creation & __str__
    def test_user_create(self):
        self.assertEqual(str(self.user), 'mha')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'Profile for mha (Staff)')

    def test_ticket_str(self):
        self.assertEqual(str(self.ticket1), 'Broken AC')
        self.assertEqual(str(self.ticket2), 'Printer Jam')

    def test_reaction_str(self):
        expected = f"T{self.ticket1.id} • S201 • 2"
        self.assertEqual(str(self.reaction1), expected)

    # ------------------------------------------------------------------------------------------------------------
    # Relationships
    def test_ticket_user_relationship(self):
        self.assertEqual(self.ticket1.user.username, 'mha')
        self.assertEqual(self.ticket2.user, self.user)

    def test_ticket_worklogs_relationship(self):
        self.assertEqual(self.ticket1.worklogs.count(), 2)
        self.assertIn(self.wl1, self.ticket1.worklogs.all())
        self.assertIn(self.wl2, self.ticket1.worklogs.all())
        self.assertEqual(self.ticket2.worklogs.count(), 1)
        self.assertIn(self.wl3, self.ticket2.worklogs.all())

    def test_ticket_reactions_relationship(self):
        self.assertEqual(self.ticket1.reactions.count(), 2)
        self.assertIn(self.reaction1, self.ticket1.reactions.all())
        self.assertIn(self.reaction2, self.ticket1.reactions.all())
        self.assertEqual(self.ticket2.reactions.count(), 1)
        self.assertIn(self.reaction3, self.ticket2.reactions.all())

    def test_profile_one_to_one(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.user.profile, self.profile)

    # ------------------------------------------------------------------------------------------------------------
    # Model Methods / Ordering
    def test_worklog_ordering_desc_by_date(self):
        logs = list(self.ticket1.worklogs.all())
        self.assertEqual(logs[0].date, date(2025, 1, 10))
        self.assertEqual(logs[1].date, date(2024, 12, 25))

    # ------------------------------------------------------------------------------------------------------------
    # Choices sanity
    def test_worklog_type_choices(self):
        self.assertIn(self.wl1.type, dict(WorkLog.TYPE_CHOICES))
        self.assertIn(self.wl2.type, dict(WorkLog.TYPE_CHOICES))

    def test_reaction_score_choices(self):
        self.assertIn(self.reaction1.score, dict(Reaction.SCORE_CHOICES))
        self.assertIn(self.reaction2.score, dict(Reaction.SCORE_CHOICES))
        self.assertIn(self.reaction3.score, dict(Reaction.SCORE_CHOICES))

    # ------------------------------------------------------------------------------------------------------------
    # Cascade Deletions
    def test_deleting_ticket_cascades_to_worklogs_and_reactions(self):
        self.ticket1.delete()
        self.assertFalse(WorkLog.objects.filter(id__in=[self.wl1.id, self.wl2.id]).exists())
        self.assertFalse(Reaction.objects.filter(id__in=[self.reaction1.id, self.reaction2.id]).exists())
        self.assertTrue(WorkLog.objects.filter(id=self.wl3.id).exists())
        self.assertTrue(Reaction.objects.filter(id=self.reaction3.id).exists())

    def test_deleting_user_cascades_all_owned_tickets_and_dependents(self):
        self.user.delete()
        self.assertEqual(Ticket.objects.count(), 0)
        self.assertEqual(WorkLog.objects.count(), 0)
        self.assertEqual(Reaction.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)

    # ------------------------------------------------------------------------------------------------------------
    # OneToOne uniqueness
    def test_profile_uniqueness_one_to_one(self):
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=self.user, role='Admin')
