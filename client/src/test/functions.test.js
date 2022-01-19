import { assert } from 'chai';
import fetch from 'node-fetch';

/*
    Change lockfile test command to /node_modules/../mocha instead of mocha ... ?
*/

describe('Test functions', () => {
    it('Convex hull', (done) => {
        const data = {
            points: 'geom',
            table: 'nyc_subway_stations'
        };
          
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        assert.doesNotThrow(() => {
            fetch('http://localhost:5000/convex', options)
            .then(res => res.json())
            .then(json => { 
                assert.isNotEmpty(json.body);
                console.log(json.body)
                done();
            }, done);
        });
    });
});

// ..
