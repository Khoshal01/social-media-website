const express = require('express');
const bcrypt = require('bcryptjs');
const User = require('../userModel'); // Import User model
const router = express.Router();

// User Sign-Up Route
router.post('/signup', async (req, res) => {
  const { username, email, passwordHash } = req.body;

  // Check if username or email is already taken
  const existingUser = await User.findOne({ $or: [{ email }, { username }] });
  if (existingUser) {
    return res.status(400).json({ message: 'Username or Email already exists' });
  }

  try {
    // Create new user with hashed password
    const newUser = new User({
      username,
      email,
      passwordHash,
    });
    
    await newUser.save(); // Save to database

    res.status(201).json({
      message: 'User registered successfully',
      user: {
        username: newUser.username,
        email: newUser.email,
      },
    });
  } catch (error) {
    console.error('Error registering user:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;
