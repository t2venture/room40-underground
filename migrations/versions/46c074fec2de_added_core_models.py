"""added core models

Revision ID: 46c074fec2de
Revises: 
Create Date: 2021-04-08 20:26:49.731492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46c074fec2de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('priority', sa.String(length=255), nullable=False),
    sa.Column('due', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assessment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quarter', sa.String(length=255), nullable=False),
    sa.Column('assessment_field_1', sa.String(length=255), nullable=False),
    sa.Column('assessment_field_1_des', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=2500), nullable=False),
    sa.Column('website', sa.String(length=255), nullable=False),
    sa.Column('crunchbase', sa.String(length=255), nullable=True),
    sa.Column('pitchbook', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('crunchbase'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('pitchbook'),
    sa.UniqueConstraint('website')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('link', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('notes', sa.String(length=2500), nullable=False),
    sa.Column('event_type', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.Column('isThesis', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=100), nullable=True),
    sa.Column('linkedin_url', sa.String(length=255), nullable=False),
    sa.Column('twitter_url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('linkedin_url'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('twitter_url'),
    sa.UniqueConstraint('username')
    )
    op.create_table('vote',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vote_field_1', sa.String(length=255), nullable=False),
    sa.Column('vote_field_1_des', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_activity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activity.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_assessment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('assessment_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assessment_id'], ['assessment.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stage', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('post_money', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('initial_vote_id', sa.Integer(), nullable=True),
    sa.Column('final_vote_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['final_vote_id'], ['vote.id'], ),
    sa.ForeignKeyConstraint(['initial_vote_id'], ['vote.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_participant',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deal_event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('deal_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deal_id'], ['deal.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deal_investor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('deal_id', sa.Integer(), nullable=True),
    sa.Column('investor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deal_id'], ['deal.id'], ),
    sa.ForeignKeyConstraint(['investor_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deal_note',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('deal_id', sa.Integer(), nullable=True),
    sa.Column('note_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deal_id'], ['deal.id'], ),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deal_note')
    op.drop_table('deal_investor')
    op.drop_table('deal_event')
    op.drop_table('user_company')
    op.drop_table('event_participant')
    op.drop_table('deal')
    op.drop_table('company_assessment')
    op.drop_table('company_activity')
    op.drop_table('vote')
    op.drop_table('user')
    op.drop_table('note')
    op.drop_table('event')
    op.drop_table('company')
    op.drop_table('blacklist_tokens')
    op.drop_table('assessment')
    op.drop_table('activity')
    # ### end Alembic commands ###
