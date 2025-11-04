import dotenv from "dotenv";

dotenv.config();

const url = `https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey=${process.env.TOMORROW_API_KEY}`;
const options = {
  method: 'GET',
  headers: {accept: 'application/json', 'accept-encoding': 'deflate, gzip, br'}
};

fetch(url, options)
  .then(res => res.json())
  .then(json => console.log(json))
  .catch(err => console.error(err));