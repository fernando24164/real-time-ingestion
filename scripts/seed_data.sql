-- Publishers
INSERT INTO publishers (id, name, website, founded_year) VALUES
(1, 'Nintendo', 'https://www.nintendo.com', 1889),
(2, 'SEGA', 'https://www.sega.com', 1960),
(3, 'Konami', 'https://www.konami.com', 1969),
(4, 'Capcom', 'https://www.capcom.com', 1979);

-- Genres
INSERT INTO genres (id, name, description) VALUES
(1, 'Platform', 'Games where the main challenge is jumping between platforms'),
(2, 'RPG', 'Role-playing games with character development and storytelling'),
(3, 'Fighting', 'Combat-focused games with character versus character battles'),
(4, 'Action-Adventure', 'Games combining action and adventure elements');

-- Games
INSERT INTO games (
    id, title, description, price, release_date, publisher_id, 
    platform, stock, is_digital, is_active, region, 
    condition_rating, has_original_box, has_manual, is_rare, 
    collector_value, serial_number, special_edition
) VALUES
(1, 'Super Mario Bros. 3', 'Classic Nintendo platformer', 149.99, '1988-10-23', 1, 
    'NES', 5, false, true, 'NTSC_US', 
    9, true, true, true, 
    299.99, 'NES-QW-USA', false),
(2, 'Sonic the Hedgehog', 'SEGA''s speedster mascot', 89.99, '1991-06-23', 2, 
    'GENESIS', 3, false, true, 'NTSC_US', 
    8, true, true, false, 
    129.99, 'GEN-001-USA', false),
(3, 'Castlevania: Symphony of the Night', 'Revolutionary Metroidvania', 199.99, '1997-03-20', 3, 
    'PS1', 2, true, true, 'NTSC_US', 
    9, true, true, true, 
    399.99, 'SLUS-00067', true),
(4, 'Street Fighter II', 'Legendary fighting game', 79.99, '1991-02-06', 4, 
    'SNES', 4, false, true, 'NTSC_US', 
    7, true, false, false, 
    149.99, 'SNS-S2-USA', false);

-- Game-Genre relationships
INSERT INTO game_genre (game_id, genre_id) VALUES
(1, 1),  -- Mario - Platform
(2, 1),  -- Sonic - Platform
(3, 2),  -- Castlevania - RPG
(3, 4),  -- Castlevania - Action-Adventure
(4, 3);  -- Street Fighter - Fighting

-- Users
INSERT INTO users (id, username, email, hashed_password, is_active, created_at, updated_at) VALUES
(1, 'retrogamer', 'retro@example.com', 'hashed_password_1', true, NOW() - INTERVAL '1 year', NOW() - INTERVAL '1 year'),
(2, 'collector', 'collector@example.com', 'hashed_password_2', true, NOW() - INTERVAL '6 months', NOW() - INTERVAL '6 months'),
(3, 'casual_player', 'casual@example.com', 'hashed_password_3', true, NOW() - INTERVAL '1 month', NOW() - INTERVAL '1 month');

-- Reviews
INSERT INTO reviews (id, game_id, user_id, rating, comment, created_at) VALUES
(1, 1, 1, 5, 'Best Mario game ever!', NOW()),
(2, 2, 1, 4, 'Classic SEGA gameplay', NOW()),
(3, 3, 2, 5, 'A masterpiece of game design', NOW()),
(4, 4, 3, 4, 'Great fighting game', NOW());

-- Orders
INSERT INTO orders (id, user_id, status, total_amount, created_at, updated_at) VALUES
(1, 1, 'DELIVERED', 239.98, NOW() - INTERVAL '30 days', NOW() - INTERVAL '30 days'),
(2, 2, 'PAID', 199.99, NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days');

-- Order Items
INSERT INTO order_items (id, order_id, game_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 149.99),
(2, 1, 2, 1, 89.99),
(3, 2, 3, 1, 199.99);

-- Carts
INSERT INTO carts (id, user_id, created_at, updated_at) VALUES
(1, 3, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day');

-- Cart Items
INSERT INTO cart_items (id, cart_id, game_id, quantity) VALUES
(1, 1, 4, 1);

-- Web Events
INSERT INTO web_events (
    id, user_id, game_id, event_type, session_id,
    time_spent, referrer_page, platform, search_query,
    filters_applied, timestamp
) VALUES
(1, 1, 1, 'VIEW', 'session_1', 
    300, '/games', 'Web', NULL,
    '{"platform": "NES"}', NOW() - INTERVAL '1 hour'),
(2, 1, 1, 'ADD_TO_CART', 'session_1', 
    60, '/games/1', 'Web', NULL,
    NULL, NOW() - INTERVAL '55 minutes'),
(3, 2, 3, 'VIEW', 'session_2', 
    240, '/search', 'Mobile', 'castlevania',
    '{"platform": "PS1"}', NOW() - INTERVAL '30 minutes'),
(4, 3, 4, 'WISHLIST', 'session_3', 
    120, '/games/featured', 'Web', NULL,
    NULL, NOW() - INTERVAL '15 minutes');

-- Reset sequence values
SELECT setval('publishers_id_seq', (SELECT MAX(id) FROM publishers));
SELECT setval('genres_id_seq', (SELECT MAX(id) FROM genres));
SELECT setval('games_id_seq', (SELECT MAX(id) FROM games));
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('reviews_id_seq', (SELECT MAX(id) FROM reviews));
SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));
SELECT setval('order_items_id_seq', (SELECT MAX(id) FROM order_items));
SELECT setval('carts_id_seq', (SELECT MAX(id) FROM carts));
SELECT setval('cart_items_id_seq', (SELECT MAX(id) FROM cart_items));
SELECT setval('web_events_id_seq', (SELECT MAX(id) FROM web_events));