-- Disable foreign key checks to avoid foreign key issues when inserting data
SET foreign_key_checks = 0;

-- Insert users (20 visitors, 5 helpers, 2 admins)
-- 20 visitors
INSERT INTO users (username, password_hash, email, first_name, last_name, location, profile_image, role, status)
VALUES
('visitor1', '$2b$12$eiHxx8IeVILH2NBYzmyoRuR0HYGWWpuOasLWaS4E8ZzVh/pxCTGNy', 'visitor1@example.com', 'John', 'Doe', 'Auckland', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor2', '$2b$12$GckwtXOweYzfeKPMdYLSI.ypMvDGw75p5Yt9d067y7ksUadXWzkUy', 'visitor2@example.com', 'Jane', 'Smith', 'Wellington', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor3', '$2b$12$oYiGM6cRAHTdRdoPkVn.p.Y5hndY9E1uvyigcwdxZbWQ2As1TnUqq', 'visitor3@example.com', 'Mark', 'Johnson', 'Christchurch', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor4', '$2b$12$Z6QTiwAtDItFd3oh5Zxz0eRmK24/UQPXR30XSJ9KYbc0zi5nWvopy', 'visitor4@example.com', 'Emma', 'Brown', 'Dunedin', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor5', '$2b$12$ExZs2nmn5MQipgXgPIKCfeqezzvYkBhARj2dfDAuSfbUHZA0GJEzy', 'visitor5@example.com', 'Liam', 'Williams', 'Hamilton', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor6', '$2b$12$GAY7G2nBNNJsEYydzhaCQOjEJn4CM3KM0ZM4wtJyIeK.UnkIm.MXW', 'visitor6@example.com', 'Olivia', 'Jones', 'Napier', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor7', '$2b$12$eH8EweSZfkFAL/5FvhRv3ubDI/utiKdvGd8E9IbqekygGu5gKlwHO', 'visitor7@example.com', 'Noah', 'Miller', 'Tauranga', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor8', '$2b$12$VWcC27KKRG2wCB3UNfBPT.c7e7PurftEPWwY3yejCFKS7eDBd1I3.', 'visitor8@example.com', 'Sophia', 'Davis', 'Queenstown', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor9', '$2b$12$LQKs5o15oMMt3W2ergeF0.mpmOfNHqPEtNq9ZxoR1cNxNTyr.8MAe', 'visitor9@example.com', 'Ethan', 'Garcia', 'Palmerston North', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor10', '$2b$12$NJ42BhfUGINACzQFuwizTeD4R2ob0eU5c9qYaeX2u5397WhqwNmAa', 'visitor10@example.com', 'Isabella', 'Rodriguez', 'Whangarei', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor11', '$2b$12$kZb0X2/Wf39ucsMmIlWGEOS/sfCZODU9ZK5Q8Xm9e2uXT/Xz2I1Ui', 'visitor11@example.com', 'Mason', 'Martinez', 'New Plymouth', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor12', '$2b$12$Z2VacbsnT0HpLHhkNnKfI.FxLZfkcLTjrYSlEtblA9AK2nUSJ/NgO', 'visitor12@example.com', 'Ava', 'Hernandez', 'Nelson', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor13', '$2b$12$CXXF29OCF9eN63HuejcUoOIkvxLn5VqG6P8tJB1RHMotU7GQ3uGA6', 'visitor13@example.com', 'James', 'Lopez', 'Invercargill', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor14', '$2b$12$9TdJFEpNk5S5.9RtaYczquOU4agA8kmBRHCH9QcfNHvLgG9008Kwa', 'visitor14@example.com', 'Charlotte', 'Gonzalez', 'Blenheim', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor15', '$2b$12$fi4ncM2IKdg8NEsM9WRg5Ow8lKxBh1DDCMLxd8yYt3mcPyUxlH.eu', 'visitor15@example.com', 'Benjamin', 'Perez', 'Timaru', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor16', '$2b$12$.XDVCmNY.U4PUGMrfAmY6O.NTxZbi7wyeSej7DSaEwyeV7XjM5bAO', 'visitor16@example.com', 'Amelia', 'Wilson', 'Greymouth', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor17', '$2b$12$lDh5UgaOMrww4O66OYU1N.ALeBnJ6lOAIDgKW7rFCj8bxySun/sKq', 'visitor17@example.com', 'Lucas', 'Anderson', 'Masterton', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor18', '$2b$12$VUHM.72Os.CEeLMZsWfE/u4LG4rCp36Rp8VplYmKicfkGZ1uVb1Ym', 'visitor18@example.com', 'Mia', 'Thomas', 'Gisborne', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor19', '$2b$12$GydSpWeDAfWEzIjWqqVRZ.00KWZ9WKL7qcWemAnGzY8F.8/S3TuYi', 'visitor19@example.com', 'Alexander', 'Taylor', 'Rotorua', '/static/images/default_profile_image.jpg', 'visitor', 'active'),
('visitor20', '$2b$12$Pe/lRVgPuXE7NG8WqamCze//BQcNCI7OSXXhxVGl94MXAtMhT.F3i', 'visitor20@example.com', 'Harper', 'Moore', 'Kaitaia', '/static/images/default_profile_image.jpg', 'visitor', 'active');

-- 5 helpers
INSERT INTO users (username, password_hash, email, first_name, last_name, location, profile_image, role, status)
VALUES
('helper1', '$2b$12$0ZsJITJiTS724KCyithvlucNezhFXnGIhjupSXhDSL01Cw5gGb71u', 'helper1@example.com', 'William', 'Jackson', 'Auckland', '/static/images/default_profile_image.jpg', 'helper', 'active'),
('helper2', '$2b$12$6N/6rDetrMZwOU2b.yC2tO8CupyR6OnR0cSBf156vPv9HSJAIS/2a', 'helper2@example.com', 'Eleanor', 'White', 'Wellington', '/static/images/default_profile_image.jpg', 'helper', 'active'),
('helper3', '$2b$12$T5ufRj4tQZUtQeRyP3H/iO8pBwZL1nFX71VixunhiJHj0qTc0dvyG', 'helper3@example.com', 'Daniel', 'Clark', 'Christchurch', '/static/images/default_profile_image.jpg', 'helper', 'active'),
('helper4', '$2b$12$yPyvOASLDNcSFnheVZft8.69iOjQSLF0MkjmpS3Nrlen6RBiyYpwy', 'helper4@example.com', 'Grace', 'Lewis', 'Dunedin', '/static/images/default_profile_image.jpg', 'helper', 'active'),
('helper5', '$2b$12$Vp.2ujviUbDHYwbnSrmKGuul6kS5DY5yJAp018PD8zlG8pwMEEY8e', 'helper5@example.com', 'Henry', 'Walker', 'Hamilton', '/static/images/default_profile_image.jpg', 'helper', 'active');

-- 2 admins
INSERT INTO users (username, password_hash, email, first_name, last_name, location, profile_image, role, status)
VALUES
('admin1', '$2b$12$auDQU3jr4DrVrojDrkRaU.PrZDMOP0Sv2NuxeVHBzi68HnjUNKBT.', 'admin1@example.com', 'Olivia', 'Scott', 'Auckland', '/static/images/default_profile_image.jpg', 'admin', 'active'),
('admin2', '$2b$12$QwHh1lIaqfPszjrk.9aMWesyLVSJ5It7SZYXchGMxSAVAvkbie1/S', 'admin2@example.com', 'Jack', 'Adams', 'Wellington', '/static/images/default_profile_image.jpg', 'admin', 'active');

-- Insert issues (20 issues with realistic problem descriptions)
INSERT INTO issues (user_id, summary, description, status)
VALUES
(1, 'Tent collapsed due to wind', 'My tent collapsed during a strong wind last night. Need help securing it properly.', 'new'),
(2, 'Water pump stopped working', 'The campsite water pump has stopped functioning, and we have no water for washing or drinking.', 'open'),
(3, 'Lost item near campsite', 'I lost my phone near the campsite. Can someone help me find it?', 'new'),
(4, 'Loud noise from nearby group', 'The group next to me is being very noisy late at night, disturbing everyone.', 'resolved'),
(5, 'Wild animal sighting near tent', 'A wild animal was spotted near our tent, and we feel unsafe. What should we do?', 'stalled'),
(6, 'Campsite has no proper lighting', 'The campsite is poorly lit at night, making it difficult to walk around safely.', 'new'),
(7, 'Waterlogged campsite', 'The campsite is flooded after heavy rain, and the tent area is completely soaked.', 'open'),
(8, 'Need more firewood', 'We are running out of firewood, and there is no nearby store for more supplies.', 'resolved'),
(9, 'Broken toilet facilities', 'The toilet facilities are dirty and one of the toilets is broken.', 'stalled'),
(10, 'No Wi-Fi access at campsite', 'There is no internet or Wi-Fi service at the campsite. How can we access the internet?', 'resolved'),
(11, 'Campsite check-in issues', 'I am unable to check-in because my booking does not appear in the system.', 'new'),
(12, 'Noise from nearby road', 'There is a lot of noise coming from the nearby road, making it hard to sleep.', 'open'),
(13, 'Poor mobile phone reception', 'I am having trouble getting a signal for my phone at the campsite.', 'new'),
(14, 'Campfire restrictions unclear', 'The campfire rules are unclear, and I don’t know if we’re allowed to have one tonight.', 'resolved'),
(15, 'Inadequate restroom facilities', 'There are not enough restrooms for the number of people at the campsite.', 'stalled'),
(16, 'No trash bins near campsite', 'There are no trash bins near the campsite, and litter is piling up.', 'new'),
(17, 'Issue with campsite booking system', 'The online booking system didn’t let me select a spot properly. Please assist.', 'open'),
(18, 'Misplaced reservation confirmation', 'I lost the reservation email, and I need confirmation of my booking for tomorrow.', 'new'),
(19, 'Damaged hiking trail signage', 'The trail signs for the hiking routes are damaged or missing, making navigation difficult.', 'stalled'),
(20, 'Overbooked campsites', 'The campsite seems to be overbooked, and my family does not have a designated spot.', 'resolved');

-- Insert comments (20 comments related to issues)
INSERT INTO comments (issue_id, user_id, content)
VALUES
(2, 2, 'Is there a recent power issue causing the water pump to malfunction? It might need an electrical check.'),
(2, 3, 'We have had similar water pump issues before, and staff usually addresses them promptly. Please be patient.'),
(2, 4, 'I noticed the pump is out of order. Have you reported it to the site staff?'),
(2, 5, 'That sounds frustrating! Maybe try using the backup water source near the entrance of the campsite.'),
(2, 10, 'Some campsites provide emergency water buckets. You could check if there is a backup water source available.'),
(3, 6, 'We will help you find it! Please describe where you were last, and we can check the area together.'),
(3, 7, 'I found a phone near the north tent area. Could it be yours?'),
(4, 8, 'I’ve experienced the same issue. I complained to the staff, and they moved the group to a quieter spot.'),
(5, 9, 'Contact the rangers about the animal sighting. They can help ensure the campsite is safe for everyone.'),
(7, 11, 'I think the campsite has some drainage issues. Maybe they need to improve water runoff channels.'),
(8, 12, 'The store is a bit far, but the staff usually provides more firewood if you ask them in advance.'),
(9, 13, 'It’s important that the toilets are maintained. Try reporting this issue immediately to the camp office.'),
(10, 14, 'The Wi-Fi can be unreliable due to signal issues, but there is a hotspot in the office you can use.'),
(11, 15, 'Check-in can be tricky sometimes. Try calling the office directly to confirm your booking.'),
(12, 16, 'It’s very loud near the road. You can ask for a quieter site away from the main path.'),
(13, 17, 'Try walking to a higher spot or near the entrance. Reception can be patchy.'),
(14, 18, 'They should clarify the campfire policy, but I believe it’s allowed as long as you stay within the fire pits provided.'),
(15, 19, 'We’ve had the same issue! It’s annoying when there’s a shortage of restrooms, especially during peak season.'),
(16, 20, 'I suggest contacting the staff for additional trash bins. They should handle it.'),
(17, 21, 'The booking system is often slow. Try calling to confirm your spot or booking issues directly.'),
(18, 22, 'If you lost your confirmation email, check the spam folder or request a new confirmation from the staff.'),
(19, 23, 'The trail signage is definitely an issue. Let’s notify the staff so they can fix it.'),
(20, 24, 'That’s unfortunate! Hopefully, they can resolve the overbooking issue soon.');

-- Enable foreign key checks
SET foreign_key_checks = 1;
