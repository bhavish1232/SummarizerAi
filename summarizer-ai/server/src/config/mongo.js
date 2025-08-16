const mongoose = require('mongoose');
const url = process.env.MONGO_URL || 'mongodb://127.0.0.1:27017/summary_ai';
mongoose.connect(url);
mongoose.connection.on('connected', () => console.log('Mongo connected'));
mongoose.connection.on('error', (e) => console.error('Mongo error', e));
