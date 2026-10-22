CREATE TABLE IF NOT EXISTS operators (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'OPERATOR',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6),

    PRIMARY KEY (id),
    UNIQUE KEY uq_operators_email (email),

    CONSTRAINT chk_operators_role
        CHECK (role IN ('OPERATOR', 'SUPERVISOR', 'ADMIN'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS emergency_messages (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    message_text TEXT NOT NULL,
    location_text VARCHAR(500) NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'NEW',
    priority VARCHAR(30) NOT NULL DEFAULT 'UNCLASSIFIED',
    category VARCHAR(100) NULL,

    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6),

    PRIMARY KEY (id),

    KEY idx_messages_status_created (status, created_at),
    KEY idx_messages_priority_created (priority, created_at),
    KEY idx_messages_created (created_at),

    CONSTRAINT chk_messages_status
        CHECK (status IN (
            'NEW', 'IN_REVIEW', 'IN_PROGRESS',
            'RESOLVED', 'CLOSED'
        )),

    CONSTRAINT chk_messages_priority
        CHECK (priority IN (
            'UNCLASSIFIED', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL'
        ))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS message_events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    message_id BIGINT UNSIGNED NOT NULL,
    actor_id BIGINT UNSIGNED NULL,

    event_type VARCHAR(50) NOT NULL,
    old_value VARCHAR(500) NULL,
    new_value VARCHAR(500) NULL,
    details TEXT NULL,

    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    PRIMARY KEY (id),

    KEY idx_events_message_created (message_id, created_at),
    KEY idx_events_actor_created (actor_id, created_at),

    CONSTRAINT fk_events_message
        FOREIGN KEY (message_id)
        REFERENCES emergency_messages (id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_events_actor
        FOREIGN KEY (actor_id)
        REFERENCES operators (id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;