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
INSERT INTO users (id, username, email, hashed_password, is_active, created_at) VALUES
(1, 'retrogamer', 'retro@example.com', 'hashed_password_1', true, NOW() - INTERVAL '1 year'),
(2, 'collector', 'collector@example.com', 'hashed_password_2', true, NOW() - INTERVAL '6 months'),
(3, 'casual_player', 'casual@example.com', 'hashed_password_3', true, NOW() - INTERVAL '1 month');

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
    user_id, game_id, event_type, session_id,
    time_spent, referrer_page, platform, search_query,
    filters_applied, timestamp
) VALUES
-- User 1 (retrogamer) - Shows interest in Nintendo and classic games
(1, 1, 'VIEW', 'session_1a', 180, '/games', 'Web', NULL, '{"platform": "NES"}', NOW() - INTERVAL '3 days'),
(1, 1, 'ADD_TO_CART', 'session_1a', 45, '/games/1', 'Web', NULL, NULL, NOW() - INTERVAL '3 days'),
(1, 1, 'PURCHASE', 'session_1a', 120, '/cart', 'Web', NULL, NULL, NOW() - INTERVAL '3 days'),
(1, NULL, 'VIEW', 'session_1b', 90, '/search', 'Web', 'mario', '{"publisher": "Nintendo"}', NOW() - INTERVAL '2 days 12 hours'),
(1, 4, 'VIEW', 'session_1b', 240, '/games/4', 'Web', NULL, NULL, NOW() - INTERVAL '2 days 11 hours'),
(1, 4, 'WISHLIST', 'session_1b', 30, '/games/4', 'Web', NULL, NULL, NOW() - INTERVAL '2 days 11 hours'),
(1, NULL, 'VIEW', 'session_1c', 120, '/games', 'Mobile', NULL, '{"platform": "SNES"}', NOW() - INTERVAL '2 days'),
(1, 2, 'VIEW', 'session_1c', 150, '/games/2', 'Mobile', NULL, NULL, NOW() - INTERVAL '2 days'),
(1, 2, 'REVIEW', 'session_1c', 300, '/games/2/review', 'Mobile', NULL, NULL, NOW() - INTERVAL '2 days'),
(1, NULL, 'VIEW', 'session_1d', 60, '/search', 'Web', 'castlevania', NULL, NOW() - INTERVAL '1 day'),
(1, 3, 'VIEW', 'session_1d', 180, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '1 day'),
(1, 3, 'ADD_TO_CART', 'session_1d', 45, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '1 day'),
(1, 3, 'REMOVE_FROM_CART', 'session_1d', 30, '/cart', 'Web', NULL, NULL, NOW() - INTERVAL '1 day'),
(1, NULL, 'VIEW', 'session_1e', 90, '/games/featured', 'Web', NULL, '{"is_rare": true}', NOW() - INTERVAL '12 hours'),
(1, 1, 'VIEW', 'session_1e', 120, '/games/1', 'Web', NULL, NULL, NOW() - INTERVAL '12 hours'),
(1, 4, 'VIEW', 'session_1e', 150, '/games/4', 'Web', NULL, NULL, NOW() - INTERVAL '11 hours'),
-- User 2 (collector) - Focuses on rare and valuable games
(2, NULL, 'VIEW', 'session_2a', 120, '/search', 'Web', NULL, '{"is_rare": true}', NOW() - INTERVAL '5 days'),
(2, 3, 'VIEW', 'session_2a', 300, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '5 days'),
(2, 3, 'WISHLIST', 'session_2a', 30, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '5 days'),
(2, NULL, 'VIEW', 'session_2b', 180, '/games', 'Mobile', NULL, '{"has_original_box": true}', NOW() - INTERVAL '4 days'),
(2, 1, 'VIEW', 'session_2b', 240, '/games/1', 'Mobile', NULL, NULL, NOW() - INTERVAL '4 days'),
(2, 1, 'ADD_TO_CART', 'session_2b', 60, '/games/1', 'Mobile', NULL, NULL, NOW() - INTERVAL '4 days'),
(2, NULL, 'VIEW', 'session_2c', 90, '/search', 'Web', 'rare games', '{"condition_rating": "9"}', NOW() - INTERVAL '3 days'),
(2, 3, 'VIEW', 'session_2c', 180, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '3 days'),
(2, 3, 'ADD_TO_CART', 'session_2c', 45, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '3 days'),
(2, 3, 'PURCHASE', 'session_2c', 120, '/cart', 'Web', NULL, NULL, NOW() - INTERVAL '3 days'),
(2, NULL, 'VIEW', 'session_2d', 150, '/games/featured', 'Web', NULL, '{"special_edition": true}', NOW() - INTERVAL '2 days'),
(2, 4, 'VIEW', 'session_2d', 210, '/games/4', 'Web', NULL, NULL, NOW() - INTERVAL '2 days'),
(2, NULL, 'VIEW', 'session_2e', 120, '/search', 'Mobile', 'symphony of the night', NULL, NOW() - INTERVAL '1 day'),
(2, 3, 'VIEW', 'session_2e', 180, '/games/3', 'Mobile', NULL, NULL, NOW() - INTERVAL '1 day'),
(2, 3, 'REVIEW', 'session_2e', 300, '/games/3/review', 'Mobile', NULL, NULL, NOW() - INTERVAL '1 day'),
(2, NULL, 'VIEW', 'session_2f', 90, '/games', 'Web', NULL, '{"platform": "PS1"}', NOW() - INTERVAL '6 hours'),
(2, 3, 'VIEW', 'session_2f', 150, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '6 hours'),
-- User 3 (casual_player) - Browses various games, price-sensitive
(3, NULL, 'VIEW', 'session_3a', 60, '/games/featured', 'Mobile', NULL, NULL, NOW() - INTERVAL '7 days'),
(3, 4, 'VIEW', 'session_3a', 120, '/games/4', 'Mobile', NULL, NULL, NOW() - INTERVAL '7 days'),
(3, 4, 'WISHLIST', 'session_3a', 30, '/games/4', 'Mobile', NULL, NULL, NOW() - INTERVAL '7 days'),
(3, NULL, 'VIEW', 'session_3b', 90, '/search', 'Web', NULL, '{"price_under": "100"}', NOW() - INTERVAL '6 days'),
(3, 2, 'VIEW', 'session_3b', 150, '/games/2', 'Web', NULL, NULL, NOW() - INTERVAL '6 days'),
(3, 2, 'ADD_TO_CART', 'session_3b', 45, '/games/2', 'Web', NULL, NULL, NOW() - INTERVAL '6 days'),
(3, 2, 'REMOVE_FROM_CART', 'session_3b', 30, '/cart', 'Web', NULL, NULL, NOW() - INTERVAL '6 days'),
(3, NULL, 'VIEW', 'session_3c', 120, '/games', 'Mobile', NULL, '{"platform": "SNES"}', NOW() - INTERVAL '5 days'),
(3, 4, 'VIEW', 'session_3c', 180, '/games/4', 'Mobile', NULL, NULL, NOW() - INTERVAL '5 days'),
(3, 4, 'ADD_TO_CART', 'session_3c', 45, '/games/4', 'Mobile', NULL, NULL, NOW() - INTERVAL '5 days'),
(3, NULL, 'VIEW', 'session_3d', 90, '/search', 'Web', 'mario', NULL, NOW() - INTERVAL '4 days'),
(3, 1, 'VIEW', 'session_3d', 120, '/games/1', 'Web', NULL, NULL, NOW() - INTERVAL '4 days'),
(3, NULL, 'VIEW', 'session_3e', 60, '/games/featured', 'Web', NULL, '{"is_digital": true}', NOW() - INTERVAL '3 days'),
(3, 3, 'VIEW', 'session_3e', 150, '/games/3', 'Web', NULL, NULL, NOW() - INTERVAL '3 days'),
(3, NULL, 'VIEW', 'session_3f', 90, '/search', 'Mobile', 'fighting games', NULL, NOW() - INTERVAL '2 days'),
(3, 4, 'VIEW', 'session_3f', 180, '/games/4', 'Mobile', NULL, NULL, NOW() - INTERVAL '2 days'),
(3, 4, 'REVIEW', 'session_3f', 240, '/games/4/review', 'Mobile', NULL, NULL, NOW() - INTERVAL '2 days'),
(3, NULL, 'VIEW', 'session_3g', 120, '/games', 'Web', NULL, '{"platform": "GENESIS"}', NOW() - INTERVAL '1 day'),
(3, 2, 'VIEW', 'session_3g', 150, '/games/2', 'Web', NULL, NULL, NOW() - INTERVAL '1 day'),
(3, 2, 'WISHLIST', 'session_3g', 30, '/games/2', 'Web', NULL, NULL, NOW() - INTERVAL '1 day');

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
