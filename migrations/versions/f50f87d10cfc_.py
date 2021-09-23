"""empty message

Revision ID: f50f87d10cfc
Revises: 
Create Date: 2021-09-23 10:04:59.550486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f50f87d10cfc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bedroom_count', sa.Integer(), nullable=False),
    sa.Column('bathroom_count', sa.Integer(), nullable=False),
    sa.Column('rounded_sqft_area', sa.Integer(), nullable=False),
    sa.Column('rent_amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('profile_url', sa.String(length=511), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=100), nullable=True),
    sa.Column('linkedin_url', sa.String(length=255), nullable=True),
    sa.Column('twitter_url', sa.String(length=255), nullable=True),
    sa.Column('company_name', sa.String(length=255), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('modified_by', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('modified_time', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('contents', sa.Text(length=100000), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('modified_by', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('modified_time', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['modified_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('majorcity', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('state', sa.String(length=255), nullable=True),
    sa.Column('fips_code', sa.String(length=255), nullable=True),
    sa.Column('zipcode', sa.String(length=255), nullable=True),
    sa.Column('usage_code', sa.String(length=255), nullable=True),
    sa.Column('building_sqft_area', sa.Integer(), nullable=True),
    sa.Column('gross_sqft_area', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('street', sa.String(length=255), nullable=True),
    sa.Column('housenumber', sa.String(length=255), nullable=True),
    sa.Column('bd_rms', sa.String(length=255), nullable=True),
    sa.Column('bt_rms', sa.String(length=255), nullable=True),
    sa.Column('photos', sa.String(length=1011), nullable=True),
    sa.Column('market_price', sa.Integer(), nullable=True),
    sa.Column('listed', sa.Boolean(), nullable=False),
    sa.Column('cherre_id', sa.String(length=255), nullable=False),
    sa.Column('ann_mortgage_cost', sa.Integer(), nullable=True),
    sa.Column('estimated_rent', sa.Integer(), nullable=True),
    sa.Column('cap_rate', sa.Float(), nullable=True),
    sa.Column('yield_rate', sa.Float(), nullable=True),
    sa.Column('lasso_score', sa.Float(), nullable=True),
    sa.Column('lasso_property', sa.Float(), nullable=True),
    sa.Column('lasso_economics', sa.Float(), nullable=True),
    sa.Column('lasso_location', sa.Float(), nullable=True),
    sa.Column('lasso_macro', sa.Float(), nullable=True),
    sa.Column('hoa_fee', sa.Float(), nullable=True),
    sa.Column('hoa_rent', sa.Float(), nullable=True),
    sa.Column('est_property_tax', sa.Float(), nullable=True),
    sa.Column('est_insurance', sa.Float(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('modified_by', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('modified_time', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['modified_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cherre_id')
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('color', sa.String(length=7), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('modified_by', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('modified_time', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['modified_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property_model',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('project_oneyear', sa.Float(), nullable=False),
    sa.Column('project_twoyear', sa.Float(), nullable=False),
    sa.Column('project_fiveyear', sa.Float(), nullable=False),
    sa.Column('threemonth_corr', sa.Float(), nullable=False),
    sa.Column('sixmonth_corr', sa.Float(), nullable=False),
    sa.Column('lower_series', sa.String(length=511), nullable=True),
    sa.Column('median_series', sa.String(length=511), nullable=True),
    sa.Column('upper_series', sa.String(length=511), nullable=True),
    sa.Column('model_metrics', sa.String(length=1023), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property_portfolio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('portfolio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team_portfolio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('portfolio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_team',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('modified_by', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('modified_time', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['modified_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_team')
    op.drop_table('team_portfolio')
    op.drop_table('property_portfolio')
    op.drop_table('property_model')
    op.drop_table('team')
    op.drop_table('property')
    op.drop_table('document')
    op.drop_table('user')
    op.drop_table('rent')
    op.drop_table('portfolio')
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###
