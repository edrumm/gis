import { assert } from 'chai';
import fetch from 'node-fetch';

/*
    Change lockfile test command to /node_modules/../mocha instead of mocha ... ?
*/

describe('Test route', () => {
    it('Performs convex hull', (done) => {
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
            fetch('http://localhost:5000/test', options)
            .then(res => res.json())
            .then(json => { 
                assert.isTrue(json.body.includes('POLYGON'));
                done();
            }, done);
        });
    });
});

// ..
