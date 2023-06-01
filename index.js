const express = require('express');
const cors = require('cors');
const parser = require('./parse');

const app = express();

app.use(express.json({limit: '50mb'}))
app.use(cors());


app.post('/parse', (req, res) => {
    const { xml } = req.body;
    try{
        const decoded = Buffer.from(xml, 'base64').toString()
        const parsed = parser(decoded);
        res.status(200).json({parsed});
    }catch(e){
        res.status(500).json({error: e.message});
    }

})

app.listen(5000, () => {
    console.log(`Server is running on port 5000`)
})