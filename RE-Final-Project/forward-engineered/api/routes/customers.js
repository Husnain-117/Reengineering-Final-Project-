const express = require('express');
const Customer = require('../models/customer');

const router = express.Router();

router.get('/', async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const skip = parseInt(req.query.skip || '0', 10);
    const phone = req.query.phone;
    const filter = {};
    if (phone) filter.phone = phone;
    const items = await Customer.find(filter).sort({ phone: 1 }).skip(skip).limit(limit).lean();
    const count = await Customer.countDocuments(filter);
    res.json({ items, count });
  } catch (e) {
    next(e);
  }
});

module.exports = router;
