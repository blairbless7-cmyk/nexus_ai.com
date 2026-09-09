from sqlalchemy import Column, String, Numeric, Integer, Text, TIMESTAMP, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid, enum

# Add these enums to your existing init_db.py TYPES
# contract_status: add 'disputed' - you had typo 'disverted'
# new: job_status, escrow_status

# NEW TABLE: jobs posted by clients
"""
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES users(id),
      title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
          budget_usd NUMERIC(10,2),
            required_skills TEXT[] NOT NULL,
              status VARCHAR(20) DEFAULT 'open', -- open, in_progress, closed
                created_at TIMESTAMP DEFAULT NOW()
                );
                """

                # NEW TABLE: contracts - links job + talent
                """
                CREATE TABLE contracts (
                  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    job_id UUID REFERENCES jobs(id),
                      client_id UUID REFERENCES users(id),
                        talent_id UUID REFERENCES users(id),
                          gross_amount_usd NUMERIC(10,2) NOT NULL,
                            platform_fee_percent INT DEFAULT 10,
                              status contract_status DEFAULT 'draft',
                                escrow_stripe_payment_intent_id VARCHAR(255),
                                  created_at TIMESTAMP DEFAULT NOW()
                                  );
                                  """

                                  # NEW TABLE: escrow_ledger for audit
                                  """
                                  CREATE TABLE escrow_ledger (
                                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                      contract_id UUID REFERENCES contracts(id),
                                        amount_total_cents INT NOT NULL,
                                          fee_cents INT NOT NULL,
                                            payout_cents INT NOT NULL,
                                              stripe_transfer_id VARCHAR(255),
                                                released_at TIMESTAMP
                                                );
                                                """

                                                # NEW TABLE: messages
                                                """
                                                CREATE TABLE messages (
                                                  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                                    contract_id UUID REFERENCES contracts(id),
                                                      sender_id UUID REFERENCES users(id),
                                                        body TEXT NOT NULL,
                                                          created_at TIMESTAMP DEFAULT NOW()
                                                          );
                                                          """

                                                          # NEW TABLE: reviews
                                                          """
                                                          CREATE TABLE reviews (
                                                            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                                              contract_id UUID REFERENCES contracts(id),
                                                                reviewer_id UUID REFERENCES users(id),
                                                                  rating INT CHECK (rating >=1 AND rating <=5),
                                                                    comment TEXT,
                                                                      created_at TIMESTAMP DEFAULT NOW()
                                                                      );
                                                                      """