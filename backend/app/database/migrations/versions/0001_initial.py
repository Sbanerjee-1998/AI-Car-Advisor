"""Create the initial application tables."""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=120), nullable=False), sa.Column("email_normalized", sa.String(length=320), nullable=False), sa.Column("password_hash", sa.String(length=512), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("email_normalized"))
    op.create_index("ix_users_email_normalized", "users", ["email_normalized"], unique=False)
    op.create_table("conversations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(length=160), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_conversations_user_id", "conversations", ["user_id"], unique=False)
    op.create_table("auth_sessions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("token_hash", sa.String(length=128), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False), sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True), sa.UniqueConstraint("token_hash"))
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"], unique=False)
    op.create_index("ix_auth_sessions_token_hash", "auth_sessions", ["token_hash"], unique=False)
    op.create_table("messages", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False), sa.Column("role", sa.String(length=16), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"], unique=False)
    op.create_table("conversation_preferences", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False), sa.Column("budget_min_inr", sa.Numeric(14, 2), nullable=True), sa.Column("budget_max_inr", sa.Numeric(14, 2), nullable=True), sa.Column("fuel_type", sa.String(length=24), nullable=True), sa.Column("body_type", sa.String(length=32), nullable=True), sa.Column("seating_capacity", sa.Integer(), nullable=True), sa.Column("transmission", sa.String(length=24), nullable=True), sa.Column("daily_distance_km", sa.Numeric(12, 2), nullable=True), sa.Column("usage_notes", sa.String(length=500), nullable=True), sa.Column("unresolved_question", sa.String(length=500), nullable=True), sa.Column("recent_vehicle_ids", sa.JSON(), nullable=True), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("conversation_id"))
    op.create_table("favourites", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("vehicle_id", sa.String(length=120), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("user_id", "vehicle_id", name="uq_favourite_user_vehicle"))
    op.create_index("ix_favourites_user_id", "favourites", ["user_id"], unique=False)
    op.create_index("ix_favourites_vehicle_id", "favourites", ["vehicle_id"], unique=False)


def downgrade() -> None:
    op.drop_table("favourites")
    op.drop_table("conversation_preferences")
    op.drop_index("ix_messages_conversation_id", table_name="messages")
    op.drop_table("messages")
    op.drop_index("ix_auth_sessions_token_hash", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_user_id", table_name="auth_sessions")
    op.drop_table("auth_sessions")
    op.drop_index("ix_conversations_user_id", table_name="conversations")
    op.drop_table("conversations")
    op.drop_index("ix_users_email_normalized", table_name="users")
    op.drop_table("users")
